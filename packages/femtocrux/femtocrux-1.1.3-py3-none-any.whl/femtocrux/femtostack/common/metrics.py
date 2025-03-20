import numpy as np
import tabulate
from collections import defaultdict
from typing import List, Union, Dict

PREFIXES = {
    1e-15: "f",
    1e-12: "p",
    1e-9: "n",
    1e-6: "µ",
    1e-3: "m",
    1: "",
    1e3: "k",
    1e6: "M",
    1e9: "G",
}


def to_sci(x):
    """Convert a float to a scientific-prefix formatted string

    e.g. 0.004531 -> '4.531 m'
    """
    ks = np.array(list(PREFIXES.keys()))
    ks_cut = ks[ks <= np.abs(x)]
    if len(ks_cut) > 0:
        k = np.max(ks[ks <= x])
        pref = PREFIXES[k]
        x = x / k
        return f"{x:.3g} {pref}"
    else:
        return f"{x:.3g} "


def _merge_dicts(dicts: List[dict]):
    """Merges list of dicts into dict of lists"""
    output = defaultdict(list)
    for d in dicts:
        for k, v in d.items():
            output[k].append(v)
    for k, v in output.items():
        if isinstance(v[0], dict):
            output[k] = _merge_dicts(v)
    return dict(output)


ALLOWED_KEYS = [
    "Dynamic Energy/Frame (J)",
    "Total Energy/Frame (J)",
    "Latency (s)",
    "Static Energy/Frame (J)",
    "Memory",
    "Frames Simulated",
    "Power (W)",
]


class SimMetrics:
    """
    Object storing hardware simulator metrics.

    Arguments:
        metrics (list[dict] or dict[list]): measured metrics per batch
            from simulator
        dt (float, optional): total duration of the simulation, in seconds.
            If not provided, will use the total active time of the sim, but this will
            overlook the time spent sleeping.

    Attributes:
        total_energy: average total energy in Joules
        total_active_time: average time spent processing in seconds
        latency_per_frame: active time divided by the number of processed
            input frames
        power: average power consumption, in Watts

        metrics: detailed metrics dictionary

    """

    def __init__(
        self,
        metrics: Union[List[Dict[str, float]], Dict[str, List[float]]],
        dt=None,
        reduction_mode: str = "mean",
    ):
        if isinstance(metrics, list):
            metrics = _merge_dicts(metrics)

        for k in list(metrics.keys()):
            if k not in ALLOWED_KEYS:
                metrics.pop(k)

        self.metrics = metrics
        self.dt = dt

        self.reduction_mode = reduction_mode
        if reduction_mode == "mean":
            self.reduce = np.mean
        elif reduction_mode == "sum":
            self.reduce = np.sum

    @property
    def num_frames(self):
        return self.reduce(self.metrics["Frames Simulated"])

    @property
    def total_energy(self):
        return self.reduce(self.metrics["Total Energy/Frame (J)"]) * self.num_frames

    @property
    def total_dynamic_energy(self):
        return self.reduce(self.metrics["Dynamic Energy/Frame (J)"]) * self.num_frames

    @property
    def total_static_energy(self):
        return self.reduce(self.metrics["Static Energy/Frame (J)"]) * self.num_frames

    @property
    def total_active_time(self):
        return self.reduce(self.metrics["Latency (s)"]) * self.num_frames

    @property
    def latency(self):
        return self.reduce(self.metrics["Latency (s)"])

    @property
    def total_time(self):
        if self.dt is not None:
            dt = self.dt * self.metrics["Frames Simulated"][0]
            return max(dt, self.total_active_time)
        else:
            return self.total_active_time

    @property
    def power(self):
        return self.reduce(self.metrics["Power (W)"])

    def performance_report(self):
        report = [
            ["total energy", f"{to_sci(self.total_energy)}J"],
            ["total dynamic energy", f"{to_sci(self.total_dynamic_energy)}J"],
            ["total static energy", f"{to_sci(self.total_static_energy)}J"],
            ["power", f"{to_sci(self.power)}W"],
            ["total active time", f"{to_sci(self.total_active_time)}s"],
            ["total time", f"{to_sci(self.total_time)}s"],
            ["latency/frame", f"{to_sci(self.latency)}s"],
        ]
        output = tabulate.tabulate(report)
        return output

    def memory_report(self):
        mem = self.metrics["Memory"]

        out = {}
        for mem_type in ["Data Mem", "Instr Mem", "Table Mem"]:
            k = f"{mem_type} (B)"
            out[mem_type] = {
                "Used": int(mem["Used"][k][0]),
                "Capacity": int(mem["Capacity"][k][0]),
            }

        full_names = {
            "Data Mem": "Data Memory",
            "Instr Mem": "Instruction Memory",
            "Table Mem": "Table Memory",
        }

        report = [["Memory Type", "Used", "Capacity", "Percentage"]]
        for key, name in full_names.items():
            used = out[key]["Used"]
            cap = out[key]["Capacity"]
            pct = 100 * used / cap
            report.append([name, f"{to_sci(used)}B", f"{to_sci(cap)}B", f"{pct:.1f}%"])
        return tabulate.tabulate(report, headers="firstrow")

    def __repr__(self):
        perf = self.performance_report()
        mem = self.memory_report()
        output = f"Behavioral Simulator Metrics, {self.reduction_mode} over batches"
        output += f"\n\n{perf}"
        output += f"\n\n{mem}"

        output = ("-" * 60 + "\n") + output + ("\n" + "-" * 60)
        return output
