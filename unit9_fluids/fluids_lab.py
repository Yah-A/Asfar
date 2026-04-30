"""Fluid statics and dynamics calculators for AP Physics 1 Unit 9."""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

RHO_WATER = 1000.0


def _fmt(value: float, unit: str) -> str:
    if abs(value) >= 1e4 or (abs(value) > 0 and abs(value) < 1e-3):
        return f"{value:.3e} {unit}"
    return f"{value:.4f} {unit}"


def _write_output(data: Dict[str, float], output: Optional[str]) -> None:
    if not output:
        return
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".csv":
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            for key, value in data.items():
                writer.writerow([key, value])
    else:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _read_csv_pairs(path: str) -> Tuple[List[float], List[float]]:
    with open(path, newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.reader(handle) if row]
    if not rows:
        raise ValueError("CSV file is empty")
    if all(item.replace(".", "", 1).replace("-", "", 1).isdigit() for item in rows[0]):
        data = rows
    else:
        data = rows[1:]
    x_vals: List[float] = []
    y_vals: List[float] = []
    for row in data:
        if len(row) < 2:
            raise ValueError("CSV rows must have at least two columns")
        x_vals.append(float(row[0]))
        y_vals.append(float(row[1]))
    return x_vals, y_vals


def _area(radius: float) -> float:
    return math.pi * radius**2


@dataclass
class DensityResult:
    density: float

    def summary(self) -> str:
        return f"rho = {_fmt(self.density, 'kg/m^3')}"


def density(mass: float, volume: float) -> DensityResult:
    return DensityResult(mass / volume)


@dataclass
class PressureResult:
    pressure: float

    def summary(self) -> str:
        return f"P = {_fmt(self.pressure, 'Pa')}"


def pressure_force(force: float, area: float) -> PressureResult:
    return PressureResult(force / area)


@dataclass
class HydrostaticResult:
    gauge_pressure: float
    absolute_pressure: float

    def summary(self) -> str:
        return "\n".join(
            [
                f"P_gauge = {_fmt(self.gauge_pressure, 'Pa')}",
                f"P_abs = {_fmt(self.absolute_pressure, 'Pa')}",
            ]
        )


def hydrostatic_pressure(
    density: float, depth: float, g: float, reference_pressure: float
) -> HydrostaticResult:
    gauge = density * g * depth
    absolute = reference_pressure + gauge
    return HydrostaticResult(gauge, absolute)


@dataclass
class BuoyantResult:
    buoyant_force: float
    apparent_weight: float
    displaced_volume: float

    def summary(self) -> str:
        return "\n".join(
            [
                f"F_b = {_fmt(self.buoyant_force, 'N')}",
                f"W_app = {_fmt(self.apparent_weight, 'N')}",
                f"V_disp = {_fmt(self.displaced_volume, 'm^3')}",
            ]
        )


def buoyant_force(
    density: float,
    displaced_volume: float,
    object_mass: float,
    g: float,
) -> BuoyantResult:
    force = density * displaced_volume * g
    apparent_weight = object_mass * g - force
    return BuoyantResult(force, apparent_weight, displaced_volume)


@dataclass
class FloatCheckResult:
    object_density: float
    fluid_density: float
    floats: bool
    fraction_submerged: float

    def summary(self) -> str:
        status = "floats" if self.floats else "sinks"
        return "\n".join(
            [
                f"rho_obj = {_fmt(self.object_density, 'kg/m^3')}",
                f"rho_fluid = {_fmt(self.fluid_density, 'kg/m^3')}",
                f"result = {status}",
                f"fraction_submerged = {self.fraction_submerged:.3f}",
            ]
        )


def float_check(object_density: float, fluid_density: float) -> FloatCheckResult:
    floats = object_density <= fluid_density
    fraction = min(object_density / fluid_density, 1.0)
    return FloatCheckResult(object_density, fluid_density, floats, fraction)


@dataclass
class ContinuityResult:
    flow_rate: float
    velocity_2: float

    def summary(self) -> str:
        return "\n".join(
            [
                f"Q = {_fmt(self.flow_rate, 'm^3/s')}",
                f"v2 = {_fmt(self.velocity_2, 'm/s')}",
            ]
        )


def continuity(area1: float, velocity1: float, area2: float) -> ContinuityResult:
    flow_rate = area1 * velocity1
    velocity2 = flow_rate / area2
    return ContinuityResult(flow_rate, velocity2)


@dataclass
class BernoulliResult:
    pressure2: float
    velocity2: float

    def summary(self) -> str:
        return "\n".join(
            [
                f"P2 = {_fmt(self.pressure2, 'Pa')}",
                f"v2 = {_fmt(self.velocity2, 'm/s')}",
            ]
        )


def bernoulli_pressure(
    density: float,
    pressure1: float,
    velocity1: float,
    height1: float,
    height2: float,
    velocity2: float,
    g: float,
) -> BernoulliResult:
    pressure2 = (
        pressure1
        + 0.5 * density * (velocity1**2 - velocity2**2)
        + density * g * (height1 - height2)
    )
    return BernoulliResult(pressure2, velocity2)


def bernoulli_velocity(
    density: float,
    pressure1: float,
    pressure2: float,
    velocity1: float,
    height1: float,
    height2: float,
    g: float,
) -> BernoulliResult:
    head_term = (pressure1 - pressure2) / density + g * (height1 - height2)
    velocity2_sq = max(velocity1**2 + 2 * head_term, 0.0)
    velocity2 = math.sqrt(velocity2_sq)
    return BernoulliResult(pressure2, velocity2)


@dataclass
class TorricelliResult:
    exit_speed: float

    def summary(self) -> str:
        return f"v_exit = {_fmt(self.exit_speed, 'm/s')}"


def torricelli(height: float, g: float) -> TorricelliResult:
    return TorricelliResult(math.sqrt(2 * g * height))


def _pressure_table(depths: List[float], density: float, g: float, p0: float) -> List[Dict[str, float]]:
    table = []
    for depth in depths:
        gauge = density * g * depth
        table.append({"depth": depth, "gauge_pressure": gauge, "absolute_pressure": p0 + gauge})
    return table


def _save_table_csv(path: str, table: List[Dict[str, float]]) -> None:
    if not table:
        return
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        headers = list(table[0].keys())
        writer.writerow(headers)
        for row in table:
            writer.writerow([row[h] for h in headers])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unit 9 fluids calculator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    density_parser = subparsers.add_parser("density", help="Density from mass and volume")
    density_parser.add_argument("--mass", type=float, required=True)
    density_parser.add_argument("--volume", type=float, required=True)
    density_parser.add_argument("--output")

    pressure_parser = subparsers.add_parser("pressure", help="Pressure from force/area")
    pressure_parser.add_argument("--force", type=float, required=True)
    pressure_parser.add_argument("--area", type=float)
    pressure_parser.add_argument("--radius", type=float)
    pressure_parser.add_argument("--output")

    hydro_parser = subparsers.add_parser("hydrostatic", help="Hydrostatic pressure")
    hydro_parser.add_argument("--density", type=float, default=RHO_WATER)
    hydro_parser.add_argument("--depth", type=float, required=True)
    hydro_parser.add_argument("--g", type=float, default=9.81)
    hydro_parser.add_argument("--p0", type=float, default=101325)
    hydro_parser.add_argument("--output")

    buoy_parser = subparsers.add_parser("buoyant", help="Buoyant force and apparent weight")
    buoy_parser.add_argument("--density", type=float, default=RHO_WATER)
    buoy_parser.add_argument("--volume", type=float, required=True)
    buoy_parser.add_argument("--mass", type=float, required=True)
    buoy_parser.add_argument("--g", type=float, default=9.81)
    buoy_parser.add_argument("--output")

    float_parser = subparsers.add_parser("float-check", help="Check float vs sink")
    float_parser.add_argument("--object-density", type=float, required=True)
    float_parser.add_argument("--fluid-density", type=float, default=RHO_WATER)
    float_parser.add_argument("--output")

    continuity_parser = subparsers.add_parser("continuity", help="Continuity equation")
    continuity_parser.add_argument("--area1", type=float)
    continuity_parser.add_argument("--radius1", type=float)
    continuity_parser.add_argument("--velocity1", type=float, required=True)
    continuity_parser.add_argument("--area2", type=float)
    continuity_parser.add_argument("--radius2", type=float)
    continuity_parser.add_argument("--output")

    bernoulli_parser = subparsers.add_parser("bernoulli", help="Bernoulli between two points")
    bernoulli_parser.add_argument("--density", type=float, default=RHO_WATER)
    bernoulli_parser.add_argument("--pressure1", type=float, required=True)
    bernoulli_parser.add_argument("--pressure2", type=float)
    bernoulli_parser.add_argument("--velocity1", type=float, required=True)
    bernoulli_parser.add_argument("--velocity2", type=float)
    bernoulli_parser.add_argument("--height1", type=float, default=0.0)
    bernoulli_parser.add_argument("--height2", type=float, default=0.0)
    bernoulli_parser.add_argument("--g", type=float, default=9.81)
    bernoulli_parser.add_argument("--output")

    torricelli_parser = subparsers.add_parser("torricelli", help="Torricelli exit speed")
    torricelli_parser.add_argument("--height", type=float, required=True)
    torricelli_parser.add_argument("--g", type=float, default=9.81)
    torricelli_parser.add_argument("--output")

    table_parser = subparsers.add_parser("pressure-table", help="Pressure vs depth table")
    table_parser.add_argument("--depths", type=str, required=True)
    table_parser.add_argument("--density", type=float, default=RHO_WATER)
    table_parser.add_argument("--g", type=float, default=9.81)
    table_parser.add_argument("--p0", type=float, default=101325)
    table_parser.add_argument("--output", required=True)

    return parser


def _parse_depths(depths: str) -> List[float]:
    return [float(value.strip()) for value in depths.split(",") if value.strip()]


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "density":
        result = density(args.mass, args.volume)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "pressure":
        if args.area is None:
            if args.radius is None:
                raise SystemExit("provide --area or --radius")
            area = _area(args.radius)
        else:
            area = args.area
        result = pressure_force(args.force, area)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "hydrostatic":
        result = hydrostatic_pressure(args.density, args.depth, args.g, args.p0)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "buoyant":
        result = buoyant_force(args.density, args.volume, args.mass, args.g)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "float-check":
        result = float_check(args.object_density, args.fluid_density)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "continuity":
        if args.area1 is None:
            if args.radius1 is None:
                raise SystemExit("provide --area1 or --radius1")
            area1 = _area(args.radius1)
        else:
            area1 = args.area1
        if args.area2 is None:
            if args.radius2 is None:
                raise SystemExit("provide --area2 or --radius2")
            area2 = _area(args.radius2)
        else:
            area2 = args.area2
        result = continuity(area1, args.velocity1, area2)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "bernoulli":
        if args.velocity2 is None:
            if args.pressure2 is None:
                raise SystemExit("provide --pressure2 when solving for velocity2")
            result = bernoulli_velocity(
                args.density,
                args.pressure1,
                args.pressure2,
                args.velocity1,
                args.height1,
                args.height2,
                args.g,
            )
        else:
            result = bernoulli_pressure(
                args.density,
                args.pressure1,
                args.velocity1,
                args.height1,
                args.height2,
                args.velocity2,
                args.g,
            )
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "torricelli":
        result = torricelli(args.height, args.g)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "pressure-table":
        depths = _parse_depths(args.depths)
        table = _pressure_table(depths, args.density, args.g, args.p0)
        _save_table_csv(args.output, table)
        print(f"Wrote {len(table)} rows to {args.output}")


if __name__ == "__main__":
    main()
