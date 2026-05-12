const G = 9.81;
const RHO_WATER = 1000;

const format = (value, unit) => {
  const abs = Math.abs(value);
  if (abs >= 1e4 || (abs > 0 && abs < 1e-3)) {
    return `${value.toExponential(3)} ${unit}`;
  }
  return `${value.toFixed(4)} ${unit}`;
};

const numberValue = (id) => Number(document.getElementById(id).value);

const setOutput = (id, lines) => {
  document.getElementById(id).textContent = lines.join("\n");
};

const density = () => {
  const mass = numberValue("den-mass");
  const volume = numberValue("den-volume");
  if (!Number.isFinite(mass) || !Number.isFinite(volume) || volume === 0) {
    setOutput("den-output", ["Enter mass and volume."]);
    return;
  }
  const rho = mass / volume;
  setOutput("den-output", [`rho = ${format(rho, "kg/m^3")}`]);
};

const pressure = () => {
  const force = numberValue("pr-force");
  const area = numberValue("pr-area");
  const radius = numberValue("pr-radius");
  const finalArea =
    Number.isFinite(area) && area > 0 ? area : Math.PI * radius ** 2;
  if (!Number.isFinite(force) || !Number.isFinite(finalArea) || finalArea === 0) {
    setOutput("pr-output", ["Enter force and area (or radius)."]);
    return;
  }
  const pressureValue = force / finalArea;
  setOutput("pr-output", [`P = ${format(pressureValue, "Pa")}`]);
};

const hydrostatic = () => {
  const rho = numberValue("hy-density");
  const depth = numberValue("hy-depth");
  const p0 = numberValue("hy-p0");
  if (!Number.isFinite(rho) || !Number.isFinite(depth) || !Number.isFinite(p0)) {
    setOutput("hy-output", ["Enter density, depth, and reference pressure."]);
    return;
  }
  const gauge = rho * G * depth;
  const absolute = p0 + gauge;
  setOutput("hy-output", [
    `P_gauge = ${format(gauge, "Pa")}`,
    `P_abs = ${format(absolute, "Pa")}`,
  ]);
};

const buoyant = () => {
  const rho = numberValue("bu-density");
  const volume = numberValue("bu-volume");
  const mass = numberValue("bu-mass");
  if (!Number.isFinite(rho) || !Number.isFinite(volume) || !Number.isFinite(mass)) {
    setOutput("bu-output", ["Enter density, volume, and mass."]);
    return;
  }
  const force = rho * volume * G;
  const apparent = mass * G - force;
  setOutput("bu-output", [
    `F_b = ${format(force, "N")}`,
    `W_app = ${format(apparent, "N")}`,
  ]);
};

const floatCheck = () => {
  const rhoObj = numberValue("fl-object");
  const rhoFluid = numberValue("fl-fluid");
  if (!Number.isFinite(rhoObj) || !Number.isFinite(rhoFluid)) {
    setOutput("fl-output", ["Enter both densities."]);
    return;
  }
  const floats = rhoObj <= rhoFluid;
  const fraction = Math.min(rhoObj / rhoFluid, 1);
  setOutput("fl-output", [
    `rho_obj = ${format(rhoObj, "kg/m^3")}`,
    `rho_fluid = ${format(rhoFluid, "kg/m^3")}`,
    `result = ${floats ? "floats" : "sinks"}`,
    `fraction_submerged = ${fraction.toFixed(3)}`,
  ]);
};

const continuity = () => {
  const area1 = numberValue("co-area1");
  const area2 = numberValue("co-area2");
  const velocity1 = numberValue("co-velocity1");
  if (!Number.isFinite(area1) || !Number.isFinite(area2) || !Number.isFinite(velocity1)) {
    setOutput("co-output", ["Enter areas and velocity."]);
    return;
  }
  const flow = area1 * velocity1;
  const velocity2 = flow / area2;
  setOutput("co-output", [
    `Q = ${format(flow, "m^3/s")}`,
    `v2 = ${format(velocity2, "m/s")}`,
  ]);
};

const bernoulli = () => {
  const rho = numberValue("be-density");
  const p1 = numberValue("be-p1");
  const p2 = numberValue("be-p2");
  const v1 = numberValue("be-v1");
  const v2 = numberValue("be-v2");
  const y1 = numberValue("be-h1");
  const y2 = numberValue("be-h2");
  if (!Number.isFinite(rho) || !Number.isFinite(p1) || !Number.isFinite(v1)) {
    setOutput("be-output", ["Enter density, P1, and v1."]);
    return;
  }
  const lines = [];
  if (Number.isFinite(v2)) {
    const computedP2 =
      p1 + 0.5 * rho * (v1 ** 2 - v2 ** 2) + rho * G * (y1 - y2);
    lines.push(`P2 (from v2) = ${format(computedP2, "Pa")}`);
  }
  if (Number.isFinite(p2)) {
    const headTerm = (p1 - p2) / rho + G * (y1 - y2);
    const computedV2 = Math.sqrt(Math.max(v1 ** 2 + 2 * headTerm, 0));
    lines.push(`v2 (from P2) = ${format(computedV2, "m/s")}`);
  }
  if (!lines.length) {
    lines.push("Enter v2 or P2 to solve.");
  }
  setOutput("be-output", lines);
};

const torricelli = () => {
  const height = numberValue("to-height");
  const v = Math.sqrt(2 * G * height);
  setOutput("to-output", [`v_exit = ${format(v, "m/s")}`]);
};

const actions = {
  density,
  pressure,
  hydrostatic,
  buoyant,
  float: floatCheck,
  continuity,
  bernoulli,
  torricelli,
};

document.addEventListener("click", (event) => {
  const action = event.target.dataset.action;
  if (!action || !actions[action]) {
    return;
  }
  actions[action]();
});
