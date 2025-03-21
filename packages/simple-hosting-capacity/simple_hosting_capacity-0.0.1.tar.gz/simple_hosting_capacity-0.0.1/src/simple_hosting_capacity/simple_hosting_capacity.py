from pathlib import Path

from loguru import logger

import pandas as pd
import opendssdirect as dss


def cmd(command):
    dss.Text.Command(command)
    return dss.Text.Result()


class HostingCapacity:
    def __init__(
        self,
        model: str | Path,
        pv_size_increment_kw_lv: float = 100,
        pv_size_increment_kw_hv: float = 200,
        feeder_head_voltage: float = 1.035,
        load_power_factor: float = 0.95,
        ac_dc_ratio: float = 1.0,
        load_mult: float = 1,
        load_model: int = 1.0,
    ):
        self.pv_size_increment_kw_lv = pv_size_increment_kw_lv
        self.pv_size_increment_kw_hv = pv_size_increment_kw_hv
        self.feeder_head_voltage = feeder_head_voltage
        self.load_power_factor = load_power_factor
        self.ac_dc_ratio = ac_dc_ratio
        self.load_model = load_model
        self.load_mult = load_mult
        self.model = model

        self.over_voltage_limit = 1.05

    def run(self, export_path: Path):
        cmd(f'redirect "{str(self.model)}"')

        cmd(f"edit vsource.source pu={self.feeder_head_voltage}")
        cmd(f"batchedit load..* mode={self.load_model} pf={self.load_power_factor}")
        cmd(f"set loadmult={self.load_mult}")

        cmd("solve")

        self.buses = dss.Circuit.AllBusNames()
        # self.buses.reverse()
        data = []
        for i, bus in enumerate(self.buses):
            logger.info(f"Percentage complete: {i / len(self.buses) * 100}")
            dss.Circuit.SetActiveBus(bus)
            bus_name = dss.Bus.Name()
            nodes = dss.Bus.Nodes()
            kv_base = dss.Bus.kVBase()
            pv_kva = self.add_pv_system(bus_name, nodes, kv_base)
            data.append({"bus": bus_name, "pv_penetration": pv_kva})

        data = pd.DataFrame(data)
        data.to_csv(export_path)
        logger.info(f"CSV export path: {export_path}")
        return export_path

    def add_pv_system(self, bus_name, nodes, kv_base):
        self.voltage_violation = False
        self.pv_size_increment_kw = (
            self.pv_size_increment_kw_lv
            if kv_base < 1.0
            else self.pv_size_increment_kw_hv
        )
        self.thermal_violation = False
        nodes_str = ".".join([str(n) for n in nodes])
        kv = kv_base if len(nodes) == 1 else kv_base * 1.732
        pv_kva = self.pv_size_increment_kw
        i = 0
        while not self.voltage_violation and not self.thermal_violation:
            if i == 0:
                cmd(
                    f"New PVSystem.pv_{bus_name} bus={bus_name}.{nodes_str}  phases={len(nodes)} kv={kv} kva={pv_kva} pf=1.0 irradiance=1.0 Pmpp={pv_kva * self.ac_dc_ratio}"
                )
            else:
                cmd(
                    f"Edit PVSystem.pv_{bus_name} bus={bus_name}.{nodes_str}  phases={len(nodes)} kv={kv} kva={pv_kva} pf=1.0 irradiance=1.0 Pmpp={pv_kva * self.ac_dc_ratio}"
                )
            cmd("solve")
            self.voltage_violation, self.thermal_violation = self.check_for_violations()

            pv_kva += self.pv_size_increment_kw
            i += 1

            if i == 10000:
                break

        cmd(
            f"Edit PVSystem.pv_{bus_name} bus={bus_name}.{nodes_str}  phases={len(nodes)} kv={kv} kva={pv_kva} pf=1.0 irradiance=1.0 Pmpp={pv_kva * self.ac_dc_ratio} enabled=false"
        )
        return pv_kva - self.pv_size_increment_kw

    def check_for_violations(self):
        v_pu = dss.Circuit.AllBusMagPu()
        thermal_violation = False
        if max(v_pu) > self.over_voltage_limit:
            voltage_violation = True
        else:
            voltage_violation = False

        line = dss.Lines.First()
        while line:
            current = dss.CktElement.CurrentsMagAng()
            rating_current = dss.CktElement.NormalAmps()
            max_current = max([abs(x) for x in current[::2]])
            if max_current / rating_current > 1:
                thermal_violation = True
                break
            line = dss.Lines.Next()

        tr = dss.Transformers.First()
        while tr:
            current = dss.CktElement.CurrentsMagAng()
            current = current[: int(len(current) / 2)]
            rating_current = dss.CktElement.NormalAmps()
            max_current = max([abs(x) for x in current[::2]])

            thermal_usage = max_current / rating_current
            if thermal_usage > 1:
                thermal_violation = True
                break
            tr = dss.Transformers.Next()

        return voltage_violation, thermal_violation
