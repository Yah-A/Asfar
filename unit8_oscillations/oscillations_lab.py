"""Oscillations toolkit for AP Physics 1 Unit 8."""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

G = 9.81


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
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(data.keys())
            writer.writerow(data.values())
    else:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _write_table(headers: List[str], rows: List[List[float]], output: Optional[str]) -> None:
    if not output:
        return
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


@dataclass
class SpringSolveResult:
    period: float
    frequency: float
    omega: float
    mass: float
    spring_constant: float

    def summary(self) -> str:
        return "\n".join(
            [
                f"T = {_fmt(self.period, 's')}",
                f"f = {_fmt(self.frequency, 'Hz')}",
                f"omega = {_fmt(self.omega, 'rad/s')}",
                f"m = {_fmt(self.mass, 'kg')}",
                f"k = {_fmt(self.spring_constant, 'N/m')}",
            ]
        )


def spring_solve(mass: Optional[float], k: Optional[float], period: Optional[float]) -> SpringSolveResult:
    if period is None:
        if mass is None or k is None:
            raise SystemExit("Provide --mass and --k to compute period")
        period = 2 * math.pi * math.sqrt(mass / k)
    if mass is None:
        if k is None:
            raise SystemExit("Provide --k to solve for mass")
        mass = (period / (2 * math.pi)) ** 2 * k
    if k is None:
        k = mass * (2 * math.pi / period) ** 2
    frequency = 1 / period
    omega = 2 * math.pi * frequency
    return SpringSolveResult(period, frequency, omega, mass, k)


@dataclass
class PendulumSolveResult:
    period: float
    frequency: float
    omega: float
    length: float
    g: float

    def summary(self) -> str:
        return "\n".join(
            [
                f"T = {_fmt(self.period, 's')}",
                f"f = {_fmt(self.frequency, 'Hz')}",
                f"omega = {_fmt(self.omega, 'rad/s')}",
                f"L = {_fmt(self.length, 'm')}",
                f"g = {_fmt(self.g, 'm/s^2')}",
            ]
        )


def pendulum_solve(length: Optional[float], period: Optional[float], g: float) -> PendulumSolveResult:
    if period is None:
        if length is None:
            raise SystemExit("Provide --length to compute period")
        period = 2 * math.pi * math.sqrt(length / g)
    if length is None:
        length = (period / (2 * math.pi)) ** 2 * g
    frequency = 1 / period
    omega = 2 * math.pi * frequency
    return PendulumSolveResult(period, frequency, omega, length, g)


@dataclass
class SHMStateResult:
    time: float
    displacement: float
    velocity: float
    acceleration: float

    def summary(self) -> str:
        return "\n".join(
            [
                f"t = {_fmt(self.time, 's')}",
                f"x = {_fmt(self.displacement, 'm')}",
                f"v = {_fmt(self.velocity, 'm/s')}",
                f"a = {_fmt(self.acceleration, 'm/s^2')}",
            ]
        )


def shm_state(amplitude: float, frequency: float, time: float, phase_deg: float) -> SHMStateResult:
    omega = 2 * math.pi * frequency
    phase = math.radians(phase_deg)
    displacement = amplitude * math.cos(omega * time + phase)
    velocity = -amplitude * omega * math.sin(omega * time + phase)
    acceleration = -omega**2 * displacement
    return SHMStateResult(time, displacement, velocity, acceleration)


def shm_series(
    amplitude: float,
    frequency: float,
    start: float,
    stop: float,
    step: float,
    phase_deg: float,
) -> List[SHMStateResult]:
    if step <= 0:
        raise SystemExit("--step must be positive")
    points = []
    time = start
    while time <= stop + 1e-9:
        points.append(shm_state(amplitude, frequency, time, phase_deg))
        time += step
    return points


@dataclass
class SHMEnergyResult:
    kinetic: float
    potential: float
    total: float

    def summary(self) -> str:
        return "\n".join(
            [
                f"K = {_fmt(self.kinetic, 'J')}",
                f"U = {_fmt(self.potential, 'J')}",
                f"E_total = {_fmt(self.total, 'J')}",
            ]
        )


def shm_energy(k: float, amplitude: float, position: float) -> SHMEnergyResult:
    if abs(position) > abs(amplitude):
        raise SystemExit("|position| must be <= amplitude")
    total = 0.5 * k * amplitude**2
    potential = 0.5 * k * position**2
    kinetic = total - potential
    return SHMEnergyResult(kinetic, potential, total)


def shm_energy_table(k: float, amplitude: float, points: int) -> List[SHMEnergyResult]:
    if points < 2:
        raise SystemExit("--points must be at least 2")
    positions = [
        -amplitude + 2 * amplitude * i / (points - 1) for i in range(points)
    ]
    return [shm_energy(k, amplitude, x) for x in positions]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Oscillations toolkit (Unit 8)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    spring_parser = subparsers.add_parser("spring-solve", help="Solve spring oscillator")
    spring_parser.add_argument("--mass", type=float)
    spring_parser.add_argument("--k", type=float)
    spring_parser.add_argument("--period", type=float)
    spring_parser.add_argument("--output")

    pendulum_parser = subparsers.add_parser("pendulum-solve", help="Solve pendulum")
    pendulum_parser.add_argument("--length", type=float)
    pendulum_parser.add_argument("--period", type=float)
    pendulum_parser.add_argument("--g", type=float, default=G)
    pendulum_parser.add_argument("--output")

    shm_parser = subparsers.add_parser("shm-state", help="SHM state or series")
    shm_parser.add_argument("--amplitude", type=float, required=True)
    shm_parser.add_argument("--frequency", type=float)
    shm_parser.add_argument("--period", type=float)
    shm_parser.add_argument("--time", type=float)
    shm_parser.add_argument("--start", type=float)
    shm_parser.add_argument("--stop", type=float)
    shm_parser.add_argument("--step", type=float)
    shm_parser.add_argument("--phase-deg", type=float, default=0.0)
    shm_parser.add_argument("--output")

    energy_parser = subparsers.add_parser("shm-energy", help="SHM energy at position")
    energy_parser.add_argument("--k", type=float, required=True)
    energy_parser.add_argument("--amplitude", type=float, required=True)
    energy_parser.add_argument("--position", type=float, required=True)
    energy_parser.add_argument("--output")

    energy_table_parser = subparsers.add_parser("energy-table", help="Energy table")
    energy_table_parser.add_argument("--k", type=float, required=True)
    energy_table_parser.add_argument("--amplitude", type=float, required=True)
    energy_table_parser.add_argument("--points", type=int, required=True)
    energy_table_parser.add_argument("--output")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "spring-solve":
        result = spring_solve(args.mass, args.k, args.period)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "pendulum-solve":
        result = pendulum_solve(args.length, args.period, args.g)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "shm-state":
        if args.frequency is None and args.period is None:
            raise SystemExit("Provide --frequency or --period")
        if args.frequency is None:
            frequency = 1 / args.period
        else:
            frequency = args.frequency
        if args.time is not None:
            result = shm_state(args.amplitude, frequency, args.time, args.phase_deg)
            print(result.summary())
            _write_output(asdict(result), args.output)
        else:
            if args.start is None or args.stop is None or args.step is None:
                raise SystemExit("Provide --start/--stop/--step for series output")
            series = shm_series(
                args.amplitude,
                frequency,
                args.start,
                args.stop,
                args.step,
                args.phase_deg,
            )
            rows = [
                [p.time, p.displacement, p.velocity, p.acceleration] for p in series
            ]
            _write_table(["time", "x", "v", "a"], rows, args.output)
            for point in series:
                print(point.summary())
                print("---")
    elif args.command == "shm-energy":
        result = shm_energy(args.k, args.amplitude, args.position)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "energy-table":
        results = shm_energy_table(args.k, args.amplitude, args.points)
        rows = []
        for idx, result in enumerate(results):
            position = -args.amplitude + 2 * args.amplitude * idx / (args.points - 1)
            rows.append([position, result.kinetic, result.potential, result.total])
        _write_table(["x", "K", "U", "E_total"], rows, args.output)
        for row in rows:
            print(
                f"x = {_fmt(row[0], 'm')}, K = {_fmt(row[1], 'J')}, "
                f"U = {_fmt(row[2], 'J')}, E = {_fmt(row[3], 'J')}"
            )


if __name__ == "__main__":
    main()
