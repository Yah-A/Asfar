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

function solveSpring({ mass, k }) {
  if (mass == null || k == null) return null;
  const period = 2 * Math.PI * Math.sqrt(mass / k);
  const omega = 2 * Math.PI / period;
  return { mass, k, period, frequency: 1 / period, omega };
}

function solvePendulum({ length, g }) {
  if (length == null) return null;
  const gVal = g ?? state.g;
  const period = 2 * Math.PI * Math.sqrt(length / gVal);
  const omega = 2 * Math.PI / period;
  return { length, period, frequency: 1 / period, omega, g: gVal };
}

function shmState({ amplitude, frequency, phaseDeg, time }) {
  const A = amplitude;
  const f = frequency;
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
  const result = solveSpring({
    mass: Number.isFinite(mass) ? mass : null,
    k: Number.isFinite(k) ? k : null,
  });
  $("sp-output").textContent = result
    ? [
        `T = ${fmt(result.period, "s")}`,
        `f = ${fmt(result.frequency, "Hz")}`,
        `omega = ${fmt(result.omega, "rad/s")}`,
        `m = ${fmt(result.mass, "kg")}`,
        `k = ${fmt(result.k, "N/m")}`,
      ].join("\n")
    : "Enter mass and spring constant.";
}

function handlePendulum() {
  const length = parseFloat($("pe-length").value);
  const g = parseFloat($("pe-g").value);
  const result = solvePendulum({
    length: Number.isFinite(length) ? length : null,
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
    : "Enter pendulum length.";
}

function handleShmState() {
  const amplitude = parseFloat($("shm-amp").value);
  const frequency = parseFloat($("shm-freq").value);
  const phase = parseFloat($("shm-phase").value);
  const time = parseFloat($("shm-time").value);
  const result = shmState({
    amplitude: Number.isFinite(amplitude) ? amplitude : null,
    frequency: Number.isFinite(frequency) ? frequency : null,
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
    : "Enter amplitude, frequency, and time.";
}

function handleEnergy() {
  const k = parseFloat($("en-k").value);
  const amplitude = parseFloat($("en-amp").value);
  const position = parseFloat($("en-x").value);
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
    if (action === "shm-state") handleShmState();
    if (action === "energy") handleEnergy();
  });
});

handleSpring();
handlePendulum();
handleShmState();
handleEnergy();
