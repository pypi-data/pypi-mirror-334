from pathlib import Path

from simple_hosting_capacity.simple_hosting_capacity import HostingCapacity
from simple_hosting_capacity.hosting_capacity_plotter import NetworkGraph

BASE_TEST_PATH = Path(__file__).parent
OPENDSS_PATH = BASE_TEST_PATH / "data" / "Master.dss"
TEST_DUMP = BASE_TEST_PATH / "test_dump"


def test_hosting_capacity():
    if not TEST_DUMP.exists():
        TEST_DUMP.mkdir()

    hosting_capacity = HostingCapacity(
        OPENDSS_PATH,
        pv_size_increment_kw_lv=100,
        pv_size_increment_kw_hv=200,
        feeder_head_voltage=1.035,
        load_power_factor=0.95,
        ac_dc_ratio=1,
        load_mult=1,
        load_model=1,
    )
    if not TEST_DUMP.exists():
        TEST_DUMP.mkdir()
    hosting_capacity.run(TEST_DUMP / "test_hosting_capacity.csv")


def test_plotting():
    network_graph = NetworkGraph(
        {
            "voltage_distance_file": TEST_DUMP / "test_voltage_distance.html",
            "heatmap_file": TEST_DUMP / "test_heatmap.html",
            "line_width_dynamic": True,
        },
        OPENDSS_PATH,
        TEST_DUMP / "test_hosting_capacity.csv",
    )
    network_graph.run()
