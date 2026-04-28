"""Rotational systems mini-simulations for AP Physics 1 Unit 6."""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

G = 6.67430e-11


def _fmt(value: float, unit: str) -> str:
    if abs(value) >= 1e4 or (abs(value) > 0 and abs(value) < 1e-3):
        return f"{value:.3e} {unit}"
    return f"{value:.4f} {unit}"


def _write_output(data: Dict[str, float], output: Optional[str]) -> None:
    if not output:
        return
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _parse_list(values: str) -> List[float]:
    try:
        return [float(v.strip()) for v in values.split(",") if v.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("values must be comma-separated numbers") from exc


def _read_csv_pairs(path: str) -> Tuple[List[float], List[float]]:
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        rows = [row for row in reader if row]
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


def _inertia(shape: str, mass: float, radius: float) -> Tuple[float, float]:
    if shape == "disk":
        return 0.5 * mass * radius**2, 0.5
    if shape == "ring":
        return mass * radius**2, 1.0
    if shape == "sphere":
        return 0.4 * mass * radius**2, 0.4
    raise ValueError("shape must be 'disk', 'ring', or 'sphere'")


@dataclass
class RotationalEnergyResult:
    rotational_inertia: float
    rotational_energy: float

    def summary(self) -> str:
        return "\n".join(
            [
                f"I = {_fmt(self.rotational_inertia, 'kg·m^2')}",
                f"K_rot = {_fmt(self.rotational_energy, 'J')}",
            ]
        )


def rotational_energy(mass: float, radius: float, omega: float, shape: str) -> RotationalEnergyResult:
    inertia, _beta = _inertia(shape, mass, radius)
    k_rot = 0.5 * inertia * omega**2
    return RotationalEnergyResult(inertia, k_rot)


@dataclass
class TorqueWorkResult:
    total_work: float
    segment_work: List[float]

    def summary(self) -> str:
        lines = [f"total work = {_fmt(self.total_work, 'J')}"]
        for idx, work in enumerate(self.segment_work, start=1):
            lines.append(f"segment {idx}: {_fmt(work, 'J')}")
        return "\n".join(lines)


def torque_work_table(taus: List[float], angles: List[float]) -> TorqueWorkResult:
    if len(taus) != len(angles):
        raise ValueError("tau and theta lists must be same length")
    if len(taus) < 2:
        raise ValueError("need at least two data points")
    segment_work = []
    total_work = 0.0
    for i in range(1, len(taus)):
        avg_tau = 0.5 * (taus[i] + taus[i - 1])
        dtheta = angles[i] - angles[i - 1]
        work = avg_tau * dtheta
        segment_work.append(work)
        total_work += work
    return TorqueWorkResult(total_work, segment_work)


@dataclass
class AngularMomentumResult:
    angular_momentum: float

    def summary(self) -> str:
        return f"L = {_fmt(self.angular_momentum, 'kg·m^2/s')}"


def angular_momentum_rigid(mass: float, radius: float, omega: float, shape: str) -> AngularMomentumResult:
    inertia, _beta = _inertia(shape, mass, radius)
    return AngularMomentumResult(inertia * omega)


def angular_momentum_particle(
    mass: float, radius: float, speed: float, angle_deg: float
) -> AngularMomentumResult:
    angle = math.radians(angle_deg)
    return AngularMomentumResult(radius * mass * speed * math.sin(angle))


@dataclass
class AngularImpulseResult:
    impulse: float

    def summary(self) -> str:
        return f"angular impulse = {_fmt(self.impulse, 'N·m·s')}"


def angular_impulse_constant(torque: float, duration: float) -> AngularImpulseResult:
    return AngularImpulseResult(torque * duration)


@dataclass
class ConservationResult:
    omega_final: float

    def summary(self) -> str:
        return f"omega_f = {_fmt(self.omega_final, 'rad/s')}"


def conservation_angular_momentum(i_initial: float, omega_initial: float, i_final: float) -> ConservationResult:
    omega_final = omega_initial * i_initial / i_final
    return ConservationResult(omega_final)


@dataclass
class RollingResult:
    inertia: float
    acceleration: Optional[float]
    time: Optional[float]
    linear_speed: float
    angular_speed: float
    energy_split: Dict[str, float]

    def summary(self) -> str:
        parts = [
            f"I = {_fmt(self.inertia, 'kg·m^2')}",
            f"v_cm = {_fmt(self.linear_speed, 'm/s')}",
            f"omega = {_fmt(self.angular_speed, 'rad/s')}",
            f"K_trans = {_fmt(self.energy_split['translation'], 'J')}",
            f"K_rot = {_fmt(self.energy_split['rotation'], 'J')}",
        ]
        if self.acceleration is not None:
            parts.insert(1, f"a_cm = {_fmt(self.acceleration, 'm/s^2')}")
        if self.time is not None:
            parts.insert(2, f"t = {_fmt(self.time, 's')}")
        return "\n".join(parts)


def rolling_without_slip(
    mass: float,
    radius: float,
    shape: str,
    incline_deg: Optional[float],
    length: Optional[float],
    height: Optional[float],
    g: float,
) -> RollingResult:
    inertia, beta = _inertia(shape, mass, radius)
    if height is None:
        if length is None or incline_deg is None:
            raise ValueError("provide height or both length and incline_deg")
        height = length * math.sin(math.radians(incline_deg))
    v = math.sqrt(2 * g * height / (1 + beta))
    omega = v / radius
    k_trans = 0.5 * mass * v**2
    k_rot = 0.5 * inertia * omega**2
    acceleration = None
    time = None
    if incline_deg is not None:
        acceleration = g * math.sin(math.radians(incline_deg)) / (1 + beta)
        if length is not None and acceleration > 0:
            time = math.sqrt(2 * length / acceleration)
    return RollingResult(
        inertia=inertia,
        acceleration=acceleration,
        time=time,
        linear_speed=v,
        angular_speed=omega,
        energy_split={"translation": k_trans, "rotation": k_rot},
    )


@dataclass
class OrbitResult:
    orbital_speed: float
    angular_momentum: float
    kinetic_energy: float
    potential_energy: float
    total_energy: float
    period: float

    def summary(self) -> str:
        lines = [
            f"v_orbit = {_fmt(self.orbital_speed, 'm/s')}",
            f"L = {_fmt(self.angular_momentum, 'kg·m^2/s')}",
            f"K = {_fmt(self.kinetic_energy, 'J')}",
            f"U = {_fmt(self.potential_energy, 'J')}",
            f"E = {_fmt(self.total_energy, 'J')}",
            f"T = {_fmt(self.period, 's')}",
        ]
        return "\n".join(lines)


def circular_orbit(mass_central: float, radius: float, mass_satellite: float) -> OrbitResult:
    orbital_speed = math.sqrt(G * mass_central / radius)
    angular_momentum = mass_satellite * orbital_speed * radius
    kinetic_energy = 0.5 * mass_satellite * orbital_speed**2
    potential_energy = -G * mass_central * mass_satellite / radius
    total_energy = kinetic_energy + potential_energy
    period = 2 * math.pi * radius / orbital_speed
    return OrbitResult(
        orbital_speed=orbital_speed,
        angular_momentum=angular_momentum,
        kinetic_energy=kinetic_energy,
        potential_energy=potential_energy,
        total_energy=total_energy,
        period=period,
    )


@dataclass
class EllipticalOrbitResult:
    periapsis_speed: float
    apoapsis_speed: float
    angular_momentum: float
    total_energy: float
    period: float

    def summary(self) -> str:
        return "\n".join(
            [
                f"v_periapsis = {_fmt(self.periapsis_speed, 'm/s')}",
                f"v_apoapsis = {_fmt(self.apoapsis_speed, 'm/s')}",
                f"L = {_fmt(self.angular_momentum, 'kg·m^2/s')}",
                f"E = {_fmt(self.total_energy, 'J')}",
                f"T = {_fmt(self.period, 's')}",
            ]
        )


def elliptical_orbit(
    mass_central: float, mass_satellite: float, periapsis: float, apoapsis: float
) -> EllipticalOrbitResult:
    semi_major = 0.5 * (periapsis + apoapsis)
    v_periapsis = math.sqrt(G * mass_central * (2 / periapsis - 1 / semi_major))
    v_apoapsis = math.sqrt(G * mass_central * (2 / apoapsis - 1 / semi_major))
    angular_momentum = mass_satellite * periapsis * v_periapsis
    total_energy = -G * mass_central * mass_satellite / (2 * semi_major)
    period = 2 * math.pi * math.sqrt(semi_major**3 / (G * mass_central))
    return EllipticalOrbitResult(
        periapsis_speed=v_periapsis,
        apoapsis_speed=v_apoapsis,
        angular_momentum=angular_momentum,
        total_energy=total_energy,
        period=period,
    )


def escape_velocity(mass_central: float, radius: float) -> float:
    return math.sqrt(2 * G * mass_central / radius)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unit 6 rotational system calculators")
    subparsers = parser.add_subparsers(dest="command", required=True)

    energy_parser = subparsers.add_parser("rotational-energy", help="Rotational kinetic energy")
    energy_parser.add_argument("--mass", type=float, required=True)
    energy_parser.add_argument("--radius", type=float, required=True)
    energy_parser.add_argument("--omega", type=float, required=True)
    energy_parser.add_argument("--shape", choices=("disk", "ring", "sphere"), default="disk")
    energy_parser.add_argument("--output")

    torque_parser = subparsers.add_parser("torque-work", help="Work from torque vs angle data")
    torque_parser.add_argument("--tau", type=_parse_list)
    torque_parser.add_argument("--theta", type=_parse_list)
    torque_parser.add_argument("--torque", type=float)
    torque_parser.add_argument("--angle", type=float)
    torque_parser.add_argument("--data-file")
    torque_parser.add_argument("--output")

    momentum_parser = subparsers.add_parser("angular-momentum", help="Angular momentum")
    momentum_parser.add_argument("--mass", type=float, required=True)
    momentum_parser.add_argument("--radius", type=float, required=True)
    momentum_parser.add_argument("--omega", type=float)
    momentum_parser.add_argument("--speed", type=float)
    momentum_parser.add_argument("--angle-deg", type=float, default=90)
    momentum_parser.add_argument(
        "--mode", choices=("rigid", "particle"), default="rigid"
    )
    momentum_parser.add_argument("--shape", choices=("disk", "ring", "sphere"), default="disk")
    momentum_parser.add_argument("--output")

    impulse_parser = subparsers.add_parser("angular-impulse", help="Angular impulse")
    impulse_parser.add_argument("--torque", type=float)
    impulse_parser.add_argument("--time", type=float)
    impulse_parser.add_argument("--data-file")
    impulse_parser.add_argument("--output")

    conservation_parser = subparsers.add_parser("conservation", help="Conservation of L")
    conservation_parser.add_argument("--I1", type=float, required=True)
    conservation_parser.add_argument("--omega1", type=float, required=True)
    conservation_parser.add_argument("--I2", type=float, required=True)
    conservation_parser.add_argument("--output")

    rolling_parser = subparsers.add_parser("rolling", help="Rolling without slipping")
    rolling_parser.add_argument("--mass", type=float, required=True)
    rolling_parser.add_argument("--radius", type=float, required=True)
    rolling_parser.add_argument("--shape", choices=("disk", "ring", "sphere"), default="disk")
    rolling_parser.add_argument("--incline-deg", type=float)
    rolling_parser.add_argument("--length", type=float)
    rolling_parser.add_argument("--height", type=float)
    rolling_parser.add_argument("--g", type=float, default=9.81)
    rolling_parser.add_argument("--output")

    orbit_parser = subparsers.add_parser("orbit", help="Orbit calculator")
    orbit_parser.add_argument("--type", choices=("circular", "elliptical"), required=True)
    orbit_parser.add_argument("--central-mass", type=float, required=True)
    orbit_parser.add_argument("--radius", type=float)
    orbit_parser.add_argument("--periapsis", type=float)
    orbit_parser.add_argument("--apoapsis", type=float)
    orbit_parser.add_argument("--sat-mass", type=float, required=True)
    orbit_parser.add_argument("--output")

    escape_parser = subparsers.add_parser("escape", help="Escape velocity calculator")
    escape_parser.add_argument("--central-mass", type=float, required=True)
    escape_parser.add_argument("--radius", type=float, required=True)
    escape_parser.add_argument("--output")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "rotational-energy":
        result = rotational_energy(args.mass, args.radius, args.omega, args.shape)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "torque-work":
        if args.data_file:
            angles, taus = _read_csv_pairs(args.data_file)
            result = torque_work_table(taus, angles)
        elif args.torque is not None and args.angle is not None:
            result = TorqueWorkResult(args.torque * args.angle, [])
        elif args.tau and args.theta:
            result = torque_work_table(args.tau, args.theta)
        else:
            raise SystemExit(
                "Provide --torque/--angle, --tau/--theta lists, or --data-file"
            )
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "angular-momentum":
        if args.mode == "rigid":
            if args.omega is None:
                raise SystemExit("rigid mode requires --omega")
            result = angular_momentum_rigid(args.mass, args.radius, args.omega, args.shape)
        else:
            if args.speed is None:
                raise SystemExit("particle mode requires --speed")
            result = angular_momentum_particle(
                args.mass, args.radius, args.speed, args.angle_deg
            )
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "angular-impulse":
        if args.data_file:
            times, taus = _read_csv_pairs(args.data_file)
            result = torque_work_table(taus, times)
            impulse = AngularImpulseResult(result.total_work)
        elif args.torque is not None and args.time is not None:
            impulse = angular_impulse_constant(args.torque, args.time)
        else:
            raise SystemExit("Provide --torque/--time or --data-file")
        print(impulse.summary())
        _write_output(asdict(impulse), args.output)
    elif args.command == "conservation":
        result = conservation_angular_momentum(args.I1, args.omega1, args.I2)
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "rolling":
        result = rolling_without_slip(
            args.mass,
            args.radius,
            args.shape,
            args.incline_deg,
            args.length,
            args.height,
            args.g,
        )
        print(result.summary())
        _write_output(asdict(result), args.output)
    elif args.command == "orbit":
        if args.type == "circular":
            if args.radius is None:
                raise SystemExit("circular orbit requires --radius")
            result = circular_orbit(args.central_mass, args.radius, args.sat_mass)
            print(result.summary())
            _write_output(asdict(result), args.output)
        else:
            if args.periapsis is None or args.apoapsis is None:
                raise SystemExit("elliptical orbit requires --periapsis and --apoapsis")
            result = elliptical_orbit(
                args.central_mass, args.sat_mass, args.periapsis, args.apoapsis
            )
            print(result.summary())
            _write_output(asdict(result), args.output)
    elif args.command == "escape":
        v = escape_velocity(args.central_mass, args.radius)
        print(f"v_escape = {_fmt(v, 'm/s')}")
        _write_output({"v_escape": v}, args.output)


if __name__ == "__main__":
    main()
