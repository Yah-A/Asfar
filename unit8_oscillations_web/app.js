const $ = (id) => document.getElementById(id);

const fmt = (value, unit = "") => {
  if (!Number.isFinite(value)) return "—";
  const abs = Math.abs(value);
  const text =
    abs >= 1e4 || (abs > 0 && abs < 1e-3)
      ? value.toExponential(3)
      : value.toFixed(4);
  return unit ? `${text} ${unit}` : text;
};

const state = {
  g: 9.81,
};

function solveSpring({ mass, k, period, frequency }) {
  let m = mass;
  let kVal = k;
  let T = period;

  if (m != null && kVal != null) {
    T = 2 * Math.PI * Math.sqrt(m / kVal);
  } else if (m != null && period != null) {
    kVal = (4 * Math.PI ** 2 * m) / period ** 2;
  } else if (kVal != null && period != null) {
    m = (kVal * period ** 2) / (4 * Math.PI ** 2);
  } else if (frequency != null && kVal != null) {
    T = 1 / frequency;
    m = (kVal * T ** 2) / (4 * Math.PI ** 2);
  } else {
    return null;
  }

  const omega = 2 * Math.PI / T;
  return { mass: m, k: kVal, period: T, frequency: 1 / T, omega };
}

function solvePendulum({ length, period, frequency, g }) {
  let L = length;
  let T = period;
  const gVal = g ?? state.g;

  if (L != null) {
    T = 2 * Math.PI * Math.sqrt(L / gVal);
  } else if (period != null) {
    L = (gVal * period ** 2) / (4 * Math.PI ** 2);
  } else if (frequency != null) {
    T = 1 / frequency;
    L = (gVal * T ** 2) / (4 * Math.PI ** 2);
  } else {
    return null;
  }

  const omega = 2 * Math.PI / T;
  return { length: L, period: T, frequency: 1 / T, omega, g: gVal };
}

function shmState({ amplitude, frequency, phaseDeg, time, period }) {
  const A = amplitude;
  const f = frequency ?? (period != null ? 1 / period : null);
  if (A == null || f == null || time == null) return null;
  const omega = 2 * Math.PI * f;
  const phase = (phaseDeg ?? 0) * (Math.PI / 180);
  const angle = omega * time + phase;
  const x = A * Math.cos(angle);
  const v = -A * omega * Math.sin(angle);
  const a = -A * omega ** 2 * Math.cos(angle);
  return { x, v, a, omega, f };
}

function energyState({ k, amplitude, position }) {
  if (k == null || amplitude == null || position == null) return null;
  const total = 0.5 * k * amplitude ** 2;
  const potential = 0.5 * k * position ** 2;
  const kinetic = Math.max(total - potential, 0);
  return { total, potential, kinetic };
}

function handleSpring() {
  const mass = parseFloat($("sp-mass").value);
  const k = parseFloat($("sp-k").value);
  const period = parseFloat($("sp-period").value);
  const frequency = parseFloat($("sp-frequency").value);
  const result = solveSpring({
    mass: Number.isFinite(mass) ? mass : null,
    k: Number.isFinite(k) ? k : null,
    period: Number.isFinite(period) ? period : null,
    frequency: Number.isFinite(frequency) ? frequency : null,
  });
  $("sp-output").textContent = result
    ? [
        `T = ${fmt(result.period, "s")}`,
        `f = ${fmt(result.frequency, "Hz")}`,
        `omega = ${fmt(result.omega, "rad/s")}`,
        `m = ${fmt(result.mass, "kg")}`,
        `k = ${fmt(result.k, "N/m")}`,
      ].join("\n")
    : "Enter two known values (mass/k/period/frequency).";
}

function handlePendulum() {
  const length = parseFloat($("pe-length").value);
  const period = parseFloat($("pe-period").value);
  const frequency = parseFloat($("pe-frequency").value);
  const g = parseFloat($("pe-g").value);
  const result = solvePendulum({
    length: Number.isFinite(length) ? length : null,
    period: Number.isFinite(period) ? period : null,
    frequency: Number.isFinite(frequency) ? frequency : null,
    g: Number.isFinite(g) ? g : null,
  });
  $("pe-output").textContent = result
    ? [
        `T = ${fmt(result.period, "s")}`,
        `f = ${fmt(result.frequency, "Hz")}`,
        `omega = ${fmt(result.omega, "rad/s")}`,
        `L = ${fmt(result.length, "m")}`,
        `g = ${fmt(result.g, "m/s^2")}`,
      ].join("\n")
    : "Enter length, period, or frequency.";
}

function handleShmState() {
  const amplitude = parseFloat($("shm-amplitude").value);
  const frequency = parseFloat($("shm-frequency").value);
  const period = parseFloat($("shm-period").value);
  const phase = parseFloat($("shm-phase").value);
  const time = parseFloat($("shm-time").value);
  const result = shmState({
    amplitude: Number.isFinite(amplitude) ? amplitude : null,
    frequency: Number.isFinite(frequency) ? frequency : null,
    period: Number.isFinite(period) ? period : null,
    phaseDeg: Number.isFinite(phase) ? phase : 0,
    time: Number.isFinite(time) ? time : null,
  });
  $("shm-output").textContent = result
    ? [
        `x = ${fmt(result.x, "m")}`,
        `v = ${fmt(result.v, "m/s")}`,
        `a = ${fmt(result.a, "m/s^2")}`,
        `omega = ${fmt(result.omega, "rad/s")}`,
      ].join("\n")
    : "Enter amplitude and (frequency or period) plus time.";
}

function handleEnergy() {
  const k = parseFloat($("en-k").value);
  const amplitude = parseFloat($("en-amplitude").value);
  const position = parseFloat($("en-position").value);
  const result = energyState({
    k: Number.isFinite(k) ? k : null,
    amplitude: Number.isFinite(amplitude) ? amplitude : null,
    position: Number.isFinite(position) ? position : null,
  });
  $("en-output").textContent = result
    ? [
        `K = ${fmt(result.kinetic, "J")}`,
        `U = ${fmt(result.potential, "J")}`,
        `E_total = ${fmt(result.total, "J")}`,
      ].join("\n")
    : "Enter spring constant, amplitude, and position.";
}

document.querySelectorAll("button[data-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const action = button.dataset.action;
    if (action === "spring") handleSpring();
    if (action === "pendulum") handlePendulum();
    if (action === "shm") handleShmState();
    if (action === "energy") handleEnergy();
  });
});

document.getElementById("clear-shm").addEventListener("click", () => {
  ["shm-output"].forEach((id) => {
    $(id).textContent = "";
  });
});
