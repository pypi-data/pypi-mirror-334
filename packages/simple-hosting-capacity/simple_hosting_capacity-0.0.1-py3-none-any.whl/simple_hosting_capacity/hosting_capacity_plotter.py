from bokeh.models import BoxZoomTool, ResetTool, WheelZoomTool, WheelPanTool, SaveTool
from bokeh.plotting import from_networkx
from bokeh.plotting import figure
from bokeh.io import show, save
from pyproj import Transformer
from bokeh.models import (
    StaticLayoutProvider,
    LinearColorMapper,
    ColumnDataSource,
    MultiLine,
    HoverTool,
    Scatter,
    Plot,
)
import opendssdirect as dss
from loguru import logger
import networkx as nx
import pandas as pd


def cmd(command):
    dss.Text.Command(command)
    return dss.Text.Result()


phase_mapping = {
    1: "A",
    2: "B",
    3: "C",
}

phase_color = {
    "A": "red",
    "B": "blue",
    "C": "green",
}


def LongLat_to_EN(long, lat):
    try:
        transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
        easting, northing = transformer.transform(long, lat)
        return easting, northing
    except Exception:
        return None, None


class NetworkGraph:
    def __init__(self, plot_properties, master_dss_file=None, pv_file=None):
        if master_dss_file:
            cmd(f'redirect "{master_dss_file}"')
            cmd("solve")

        self.pv_file = pv_file
        self._settings = plot_properties
        self._dssInstance = dss
        self._dssGraph = nx.DiGraph()

    def run(self):
        self._CreateNodes()
        self._CreatePDEdges()

        self.plot()
        self.plot_voltage_distance()
        return

    def plot_voltage_distance(self):
        graph_renderer = from_networkx(
            self._dssGraph,
            nx.spring_layout,
        )
        # scatter(size=...)
        # graph_renderer.node_renderer.glyph = Circle(
        #     size=0,
        #     )

        graph_renderer.node_renderer.glyph = Scatter(
            size=0,
        )

        graph_renderer.edge_renderer.glyph = MultiLine(line_color="Color")

        fixed_layout_provider = StaticLayoutProvider(graph_layout=self.dist_voltage)
        graph_renderer.layout_provider = fixed_layout_provider
        hoverBus = HoverTool(
            tooltips=[
                ("Name", "@Name"),
                ("Phase", "@Phase"),
                ("Distance", "@Distance"),
                ("Voltage", "@voltage"),
                ("X", "@X"),
                ("Y", "@Y"),
            ]
        )

        plot = Plot(
            width=800,
            height=800,
            tools=[
                BoxZoomTool(),
                ResetTool(),
                WheelPanTool(),
                WheelZoomTool(),
                hoverBus,
                SaveTool(),
            ],
        )

        plot.renderers.append(graph_renderer)
        show(plot)
        save(plot, f"{self._settings['voltage_distance_file']}")

    def plot(self):
        p = figure(
            x_axis_type="mercator",
            y_axis_type="mercator",
        )
        p.add_tile("CartoDB Positron", retina=True)
        nodes_data = []
        Xs = []
        Ys = []
        n_edges = len(self._dssGraph.edges())
        i_edge = 0
        for u, v, _ in self._dssGraph.edges(data=True):
            logger.info(f"Percentage complete: {i_edge / n_edges * 100}")
            try:
                if u.startswith("node_sub/"):
                    self._dssGraph.nodes[u]["X"] = self._dssGraph.nodes[v]["X"]
                    self._dssGraph.nodes[u]["Y"] = self._dssGraph.nodes[v]["Y"]
                elif v.startswith("node_sub/"):
                    self._dssGraph.nodes[v]["X"] = self._dssGraph.nodes[u]["X"]
                    self._dssGraph.nodes[v]["Y"] = self._dssGraph.nodes[u]["Y"]

                N1 = self._dssGraph.nodes[u]
                N2 = self._dssGraph.nodes[v]

                X1, Y1 = LongLat_to_EN(N1["Y"], N1["X"])
                N1["X1"] = X1
                N1["Y1"] = Y1
                X2, Y2 = LongLat_to_EN(N2["Y"], N2["X"])
                N2["X1"] = X2
                N2["Y1"] = Y2

                Xs.append([X1, X2])
                Ys.append([Y1, Y2])

                nodes_data.append(N1)
                nodes_data.append(N2)
            except Exception:
                pass
            i_edge += 1

        nodes_data = pd.DataFrame(nodes_data)
        # nodes_data.to_csv("nodes_data.csv")

        pv_min = min(nodes_data["pv_penetration"].tolist())
        pv_max = max(nodes_data["pv_penetration"].tolist())

        color = LinearColorMapper(palette="Plasma256", low=pv_min, high=pv_max)

        source = ColumnDataSource(data=nodes_data)

        hoverBus = HoverTool(
            tooltips=[
                ("Name", "@Name"),
                ("Distance", "@Distance"),
                ("Max PV capacity [kVA]", "@pv_penetration"),
            ]
        )
        p.add_tools(hoverBus)

        source2 = ColumnDataSource(dict(xs=Xs, ys=Ys))

        glyph = MultiLine(xs="xs", ys="ys", line_color="#000000", line_width=1)
        p.add_glyph(source2, glyph)

        p.circle(
            x="X1",
            y="Y1",
            size=10,
            fill_color={"field": "pv_penetration", "transform": color},
            fill_alpha=0.8,
            line_color=None,
            source=source,
        )

        show(p)
        save(p, f"{self._settings['heatmap_file']}")

    def _CreatePDEdges(self):
        PDElement = self._dssInstance.Circuit.FirstPDElement()

        while PDElement:
            power = self._dssInstance.CktElement.Powers()
            power = power[: int(len(power) / 2)]
            S = [p + 1j * q for p, q in zip(power[0::2], power[1::2])]
            bus_names = self._dssInstance.CktElement.BusNames()
            bus_names = [b + ".1.2.3" if "." not in b else b for b in bus_names]

            phases_from_sum = sum([int(x) for x in bus_names[1].split(".")[1:]])
            phases_to_sum = sum([int(x) for x in bus_names[0].split(".")[1:]])

            if phases_from_sum != 0 and phases_to_sum != 0:
                phases_from = [
                    phase_mapping[int(x)]
                    for x in bus_names[0].split(".")[1:]
                    if x != "0"
                ]
                phases_to = [
                    phase_mapping[int(x)]
                    for x in bus_names[1].split(".")[1:]
                    if x != "0"
                ]

                for phase_from, phase_to, phase_power in zip(phases_from, phases_to, S):
                    ElementData = {
                        "Name": self._dssInstance.CktElement.Name().split(".")[1],
                        "Class": self._dssInstance.CktElement.Name().split(".")[0],
                        "BusFrom": bus_names[0].split(".")[0],
                        "PhasesFrom": phase_from,
                        "BusTo": bus_names[1].split(".")[0],
                        "PhasesTo": phase_to,
                        "Enabled": self._dssInstance.CktElement.Enabled(),
                        "HasSwitchControl": self._dssInstance.CktElement.HasSwitchControl(),
                        "HasVoltControl": self._dssInstance.CktElement.HasVoltControl(),
                        "GUID": self._dssInstance.CktElement.GUID(),
                        "NumConductors": self._dssInstance.CktElement.NumConductors(),
                        "NumControls": self._dssInstance.CktElement.NumControls(),
                        "NumPhases": self._dssInstance.CktElement.NumPhases(),
                        "NumTerminals": self._dssInstance.CktElement.NumTerminals(),
                        "OCPDevType": self._dssInstance.CktElement.NumTerminals(),
                        "IsShunt": self._dssInstance.PDElements.IsShunt(),
                        "NumCustomers": self._dssInstance.PDElements.NumCustomers(),
                        "ParentPDElement": self._dssInstance.PDElements.ParentPDElement(),
                        "SectionID": self._dssInstance.PDElements.SectionID(),
                        "TotalCustomers": self._dssInstance.PDElements.TotalCustomers(),
                        "TotalMiles": self._dssInstance.PDElements.TotalMiles(),
                        "power": abs(phase_power) / 30,
                        "Color": phase_color[phase_from],
                    }
                    from_bus = ElementData["BusFrom"] + "/" + ElementData["PhasesFrom"]
                    to_bus = ElementData["BusTo"] + "/" + ElementData["PhasesTo"]
                    self._dssGraph.add_edge(from_bus, to_bus, **ElementData)

            else:
                pass
            PDElement = self._dssInstance.Circuit.NextPDElement()
        return

    def _CreateNodes(self):
        self.hosting_data = pd.read_csv(self.pv_file, index_col=1)
        hosting_data = self.hosting_data.T
        self.coordinates = {}
        self.dist_voltage = {}
        self.vmin = []
        self.vmax = []
        self.pvpen = []
        Buses = self._dssInstance.Circuit.AllBusNames()

        BusData = {}

        for ii, Bus in enumerate(Buses):
            logger.info(f"Percentage complete: {ii / len(Buses) * 100}")
            bus_data = hosting_data[Bus]
            self._dssInstance.Circuit.SetActiveBus(Bus)
            self.pvpen.append(bus_data["pv_penetration"])
            voltage = self._dssInstance.Bus.puVmagAngle()[::2]
            voltage = [v for v in voltage if v != 0]
            Nodes = self._dssInstance.Bus.Nodes()
            for node, volt in zip(Nodes, voltage):
                BusData = {
                    "Name": self._dssInstance.Bus.Name(),
                    "X": self._dssInstance.Bus.X(),
                    "Y": self._dssInstance.Bus.Y(),
                    "Phase": phase_mapping[node],
                    "voltage": volt,
                    "kVBase": self._dssInstance.Bus.kVBase(),
                    "Zsc0": self._dssInstance.Bus.Zsc0(),
                    "Zsc1": self._dssInstance.Bus.Zsc1(),
                    "TotalMiles": self._dssInstance.Bus.TotalMiles(),
                    "SectionID": self._dssInstance.Bus.SectionID(),
                    "Nodes": self._dssInstance.Bus.Nodes(),
                    "NumNodes": self._dssInstance.Bus.NumNodes(),
                    "N_Customers": self._dssInstance.Bus.N_Customers(),
                    "Distance": self._dssInstance.Bus.Distance(),
                    "Minimum voltage": min(voltage),
                    "Maximum voltage": max(voltage),
                    "pv_penetration": bus_data["pv_penetration"],
                }
                node_name = BusData["Name"] + "/" + BusData["Phase"]
                self.vmin.append(BusData["Minimum voltage"])
                self.vmax.append(BusData["Maximum voltage"])
                self._dssGraph.add_node(node_name, **BusData)
                self.coordinates[node_name] = [BusData["X"], BusData["Y"]]
                self.dist_voltage[node_name] = [BusData["Distance"], BusData["voltage"]]

        return
