"""
hygraph_csv_loader.py

An advanced ETL pipeline for loading large CSV files into HyGraph.
This version uses a generator-based approach (via pandas) to process files
in chunks rather than using Polars slice/collect.
It also supports schema validation, user-defined field mappings
(node_field_map, edge_field_map) and simple time-series columns.

Requires:
    pip install pandas
"""

import os
import pandas as pd
from datetime import datetime
from typing import Optional, Any, Dict, List

from hygraph_core.hygraph import HyGraph
from hygraph_core.constraints import parse_datetime
from hygraph_core.timeseries_operators import TimeSeries, TimeSeriesMetadata

# A far-future date for open-ended intervals
FAR_FUTURE_DATE = datetime(2100, 12, 31, 23, 59, 59)

# (Optional) You may still keep the following schemas for documentation.
NODES_SCHEMA = {
    "id": str,
    "start_time": str,
    "end_time": str,
}

EDGES_SCHEMA = {
    "id": str,
    "source_id": str,
    "target_id": str,
    "start_time": str,
    "end_time": str,
}

class HyGraphCSVLoader:
    """
    A specialized ETL pipeline that can read large CSV files via a chunked, generator-based approach
    using pandas, and then update a HyGraph instance. This loader supports user-defined field mappings
    and simple time-series columns.
    """

    def __init__(
        self,
        hygraph: HyGraph,
        nodes_folder: str,
        edges_folder: str,
        max_rows_per_batch: int = 100_000,
        node_field_map: Dict[str, str] = None,
        edge_field_map: Dict[str, str] = None,
        node_ts_columns: List[str] = None,
        edge_ts_columns: List[str] = None,
    ):
        """
        :param hygraph: An instance of HyGraph where data is loaded.
        :param nodes_folder: Directory containing node CSV files.
        :param edges_folder: Directory containing edge CSV files.
        :param max_rows_per_batch: Number of rows to process per chunk.
        :param node_field_map: Mapping of CSV columns to internal node fields.
                                Example: {"oid": "station_id", "start_time": "start", "end_time": "end"}
        :param edge_field_map: Mapping for edges.
                                Example: {"oid": "id", "source_id": "from", "target_id": "to", "start_time": "start", "end_time": "end"}
        :param node_ts_columns: List of CSV columns to interpret as node time-series data.
        :param edge_ts_columns: List of CSV columns for edge time-series data.
        """
        self.hygraph = hygraph
        self.nodes_folder = nodes_folder
        self.edges_folder = edges_folder
        self.max_rows_per_batch = max_rows_per_batch

        self.node_field_map = node_field_map or {}
        self.edge_field_map = edge_field_map or {}
        self.node_ts_columns = node_ts_columns or []
        self.edge_ts_columns = edge_ts_columns or []

    ########################
    #     MAIN PIPELINE    #
    ########################

    def run_pipeline(self):
        """
        Master pipeline method:
          1. Load all nodes (in chunks)
          2. Load all edges (in chunks)
          3. Finalize pipeline (e.g., display or post-process)
        """
        print("========== Starting ETL Pipeline (with CSV Loader) ==========")
        self.load_all_nodes()
        self.load_all_edges()
        self.finalize_pipeline()
        print("========== ETL Pipeline Complete ==========")

    def finalize_pipeline(self):
        print("\nFinalizing the pipeline... current HyGraph state:")
        # For large graphs, you might not want to call hygraph.display()
        # Instead, show summary info:
        print(f"Nodes loaded: {len(self.hygraph.graph.nodes)}")
        print(f"Edges loaded: {len(self.hygraph.graph.edges)}")
        # You can add further summary or indexing steps here.

    ########################
    #       LOAD NODES     #
    ########################

    def load_all_nodes(self):
        """
        Iterate over all CSV files in the nodes folder.
        Each CSV file’s name (minus .csv) is used as the node label.
        """
        node_files = [f for f in os.listdir(self.nodes_folder) if f.endswith(".csv")]
        for file_name in node_files:
            label = file_name.replace(".csv", "")
            file_path = os.path.join(self.nodes_folder, file_name)
            self.load_nodes_from_csv(file_path, label)

    def load_nodes_from_csv(self, csv_path: str, label: str):
        """
        Process a single CSV file in chunks and update HyGraph nodes.
        """
        print(f"\n[Nodes] Loading from {csv_path} with label={label}")
        # Read CSV in chunks using pandas
        try:
            chunk_iter = pd.read_csv(csv_path, dtype=str, chunksize=self.max_rows_per_batch)
        except Exception as e:
            print(f"[ERROR] Failed to read {csv_path}: {e}")
            return

        batch_idx = 0
        for chunk in chunk_iter:
            batch_idx += 1
            print(f"   -> Processing Node Batch #{batch_idx} with {len(chunk)} rows")
            records = chunk.to_dict(orient='records')
            for row in records:
                self._process_node_record(row, label)

    def _process_node_record(self, row: Dict[str, Any], label: str):
        """
        For each row (a dictionary), create or update a node in HyGraph.
        """
        oid_col = self.node_field_map.get("oid", "id")
        start_col = self.node_field_map.get("start_time", "start_time")
        end_col = self.node_field_map.get("end_time", "end_time")

        external_id = str(row.get(oid_col, "")).strip() or f"node_{hash(str(row))}"
        # Here, we choose not to parse the date (if you want to use the actual date strings later, you may parse them)
        start_time = row.get(start_col, "").strip()
        end_time = row.get(end_col, "").strip()

        # Build remaining properties (ignore ts columns)
        known_cols = {oid_col, start_col, end_col}
        props = {k: v for k, v in row.items() if k not in known_cols and k not in self.node_ts_columns}

        if external_id not in self.hygraph.graph.nodes:
            self.hygraph.add_pgnode(
                oid=external_id,
                label=label,
                start_time=start_time,
                end_time=end_time,
                properties=props
            )
        else:
            existing_node = self.hygraph.graph.nodes[external_id]["data"]
            for kk, vv in props.items():
                existing_node.add_static_property(kk, vv, self.hygraph)

        # Process time-series columns, treating each row’s ts columns as a measurement at 'start_time'
        if self.node_ts_columns:
            self._process_node_time_series_columns(external_id, row, start_time)

    def _process_node_time_series_columns(self, external_id: str, row: Dict[str, Any], timestamp: str):
        """
        Process each time-series column for a node.
        """
        # We assume timestamp is a string that represents the measurement time.
        node_data = self.hygraph.graph.nodes[external_id]["data"]
        for col_name in self.node_ts_columns:
            if col_name not in row:
                continue
            val = row[col_name]
            tsid = f"{external_id}_{col_name}"
            existing_ts = self.hygraph.time_series.get(tsid)
            if not existing_ts:
                metadata = TimeSeriesMetadata(owner_id=external_id, element_type="node")
                new_ts = TimeSeries(
                    tsid=tsid,
                    timestamps=[timestamp],
                    variables=[col_name],
                    data=[[val]],
                    metadata=metadata
                )
                self.hygraph.time_series[tsid] = new_ts
                node_data.add_temporal_property(col_name, new_ts, self.hygraph)
            else:
                if timestamp in existing_ts.data.coords['time'].values:
                    existing_ts.update_value_at_timestamp(timestamp, val, variable_name=col_name)
                else:
                    existing_ts.append_data(timestamp, val)

    ########################
    #       LOAD EDGES     #
    ########################

    def load_all_edges(self):
        """
        Iterate over all CSV files in the edges folder.
        Each CSV file’s name (minus .csv) is used as the edge label.
        """
        edge_files = [f for f in os.listdir(self.edges_folder) if f.endswith(".csv")]
        for file_name in edge_files:
            label = file_name.replace(".csv", "")
            file_path = os.path.join(self.edges_folder, file_name)
            self.load_edges_from_csv(file_path, label)

    def load_edges_from_csv(self, csv_path: str, label: str):
        """
        Process a single CSV file of edges in chunks.
        """
        print(f"\n[Edges] Loading from {csv_path} with label={label}")
        try:
            chunk_iter = pd.read_csv(csv_path, dtype=str, chunksize=self.max_rows_per_batch)
        except Exception as e:
            print(f"[ERROR] Failed to read {csv_path}: {e}")
            return

        batch_idx = 0
        for chunk in chunk_iter:
            batch_idx += 1
            print(f"   -> Processing Edge Batch #{batch_idx} with {len(chunk)} rows")
            records = chunk.to_dict(orient='records')
            for row in records:
                self._process_edge_record(row, label)

    def _process_edge_record(self, row: Dict[str, Any], label: str):
        """
        For each row (a dictionary) in an edge CSV file, create or update an edge in HyGraph.
        """
        oid_col = self.edge_field_map.get("oid", "id")
        src_col = self.edge_field_map.get("source_id", "source_id")
        tgt_col = self.edge_field_map.get("target_id", "target_id")
        st_col = self.edge_field_map.get("start_time", "start_time")
        ed_col = self.edge_field_map.get("end_time", "end_time")

        edge_id = str(row.get(oid_col, "")).strip() or f"edge_{hash(str(row))}"
        source_id = str(row.get(src_col, "")).strip()
        target_id = str(row.get(tgt_col, "")).strip()
        # For edges, we again choose to treat the time columns as strings.
        start_time = row.get(st_col, "").strip()
        end_time = row.get(ed_col, "").strip()

        known_cols = {oid_col, src_col, tgt_col, st_col, ed_col}
        props = {k: v for k, v in row.items() if k not in known_cols and k not in self.edge_ts_columns}

        if source_id not in self.hygraph.graph.nodes:
            print(f"      [WARN] Skipping Edge {edge_id}: Source {source_id} not found.")
            return
        if target_id not in self.hygraph.graph.nodes:
            print(f"      [WARN] Skipping Edge {edge_id}: Target {target_id} not found.")
            return

        existing_edge = None
        for u, v, key, data in self.hygraph.graph.edges(keys=True, data=True):
            if key == edge_id:
                existing_edge = data["data"]
                break

        if not existing_edge:
            self.hygraph.add_pgedge(
                oid=edge_id,
                source=source_id,
                target=target_id,
                label=label,
                start_time=start_time,
                end_time=end_time,
                properties=props
            )
        else:
            for kk, val in props.items():
                existing_edge.add_static_property(kk, val, self.hygraph)

        if self.edge_ts_columns:
            self._process_edge_time_series_columns(edge_id, row, start_time)

    def _process_edge_time_series_columns(self, edge_id: str, row: Dict[str, Any], timestamp: str):
        """
        Process each edge time-series column.
        """
        # Locate the edge object in HyGraph
        edge_data = None
        for u, v, k, edata in self.hygraph.graph.edges(keys=True, data=True):
            if k == edge_id:
                edge_data = edata["data"]
                break
        if not edge_data:
            return

        for col_name in self.edge_ts_columns:
            if col_name not in row:
                continue
            val = row[col_name]
            tsid = f"{edge_id}_{col_name}"
            existing_ts = self.hygraph.time_series.get(tsid)
            if not existing_ts:
                metadata = TimeSeriesMetadata(owner_id=edge_id, element_type="edge")
                new_ts = TimeSeries(
                    tsid=tsid,
                    timestamps=[timestamp],
                    variables=[col_name],
                    data=[[val]],
                    metadata=metadata
                )
                self.hygraph.time_series[tsid] = new_ts
                edge_data.add_temporal_property(col_name, new_ts, self.hygraph)
            else:
                if timestamp in existing_ts.data.coords['time'].values:
                    existing_ts.update_value_at_timestamp(timestamp, val, variable_name=col_name)
                else:
                    existing_ts.append_data(timestamp, val)

    ########################
    #      UTILITIES       #
    ########################

    def _safe_parse_date(self, val: Any, default: Optional[datetime] = None) -> datetime:
        """
        Try to parse a date/datetime from a cell value. Falls back to the default if parsing fails.
        ree
        """
        if not val:
            return default if default else datetime.now()
        if isinstance(val, datetime):
            return val
        parsed = parse_datetime(str(val))
        return parsed if parsed else (default if default else datetime.now())

