from pathlib import Path

import click

from simple_hosting_capacity.simple_hosting_capacity import HostingCapacity
from simple_hosting_capacity.hosting_capacity_plotter import NetworkGraph


@click.argument("model")
@click.option(
    "-l",
    "--pv-size-increment-lv",
    default=100.0,
    help="PV size increment in kVA (for low voltage buses).",
)
@click.option(
    "-h",
    "--pv-size-increment-hv",
    default=200.0,
    help="PV size increment in kVA (for high voltage buses).",
)
@click.option(
    "-f",
    "--feeeder-head-voltage",
    default=1,
    help="Voltage at the head of the feeder in pu.",
)
@click.option("-p", "--load-power-factor", default=1, help="Load power factor.")
@click.option(
    "-a", "--ac-dc-ratio", default=1, help="AC / DC ratio for the PV systems."
)
@click.option("-m", "--load-mult", default=1, help="Load multiplier.")
@click.option(
    "-t",
    "--load-model-type",
    default=1,
    help="Load model type (see OpenDSS documentation).",
)
@click.option("-e", "--export-path", help="Path to export hosting capacity data.")
@click.command()
def run_hosting_capacity(
    model,
    pv_size_increment_lv,
    pv_size_increment_hv,
    feeeder_head_voltage,
    load_power_factor,
    ac_dc_ratio,
    load_mult,
    load_model_type,
    export_path,
):
    """
    Run the hosting capacity calculation.

    This function runs the hosting capacity calculation using the provided arguments and
    exports the results to a CSV file.

    Parameters:
    model (str) - Path to the OpenDSS model file.
    pv_size_increment_lv (float) - PV size increment in kVA for low voltage buses.
    pv_size_increment_hv (float) - PV size increment in kVA for high voltage buses.
    feeeder_head_voltage (float) - Voltage at the head of the feeder in pu.
    load_power_factor (float) - Load power factor.
    ac_dc_ratio (float) - AC / DC ratio for the PV systems.
    load_mult (float) - Load multiplier.
    load_model_type (int) - Load model type (see OpenDSS documentation).
    export_path (str) - Path to export hosting capacity data.
    """

    hosting_capacity = HostingCapacity(
        model=model,
        pv_size_increment_kw_lv=pv_size_increment_lv,
        pv_size_increment_kw_hv=pv_size_increment_hv,
        feeder_head_voltage=feeeder_head_voltage,
        load_power_factor=load_power_factor,
        ac_dc_ratio=ac_dc_ratio,
        load_mult=load_mult,
        load_model=load_model_type,
    )
    hosting_capacity.run(export_path=Path(export_path).with_suffix(".csv"))


@click.argument("model")
@click.option(
    "-p", "--hosting-capacity-csv", help="PV hosting capacity data (csv file)."
)
@click.option("-l", "--line-width-dynamic", default=True, help="Number of greetings.")
@click.option(
    "-v",
    "--voltage-distance-file",
    default="voltage_distance_plot.html",
    help="Path to voltage distance plot export.",
)
@click.option(
    "-h",
    "--heatmap-file",
    default="heatmap_plot.html",
    help="Path to heatmap plot export.",
)
@click.command()
def build_plots(
    model, hosting_capacity_csv, line_width_dynamic, voltage_distance_file, heatmap_file
):
    """
    Build plots for the hosting capacity data.

    This function builds the plots for the hosting capacity data, given the OpenDSS model file and the hosting capacity data.

    Parameters:
    model (str) - Path to the OpenDSS model file.
    hosting_capacity_csv (str) - Path to the hosting capacity data (csv file).
    line_width_dynamic (bool) - Whether to use dynamic line width for the voltage distance plot.
    voltage_distance_file (str) - Path to export the voltage distance plot.
    heatmap_file (str) - Path to export the heatmap plot.
    """
    settings = {
        "line_width_dynamic": line_width_dynamic,
        "voltage_distance_file": Path(voltage_distance_file).with_suffix(".html"),
        "heatmap_file": Path(heatmap_file).with_suffix(".html"),
    }

    network_graph = NetworkGraph(
        settings,
        model,
        hosting_capacity_csv,
    )
    network_graph.run()


@click.group()
def cli():
    """CLI commands"""


cli.add_command(run_hosting_capacity)
cli.add_command(build_plots)
