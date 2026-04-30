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
  const mass = numberValue("de-mass");
  const volume = numberValue("de-volume");
  const rho = mass / volume;
  setOutput("de-output", [`rho = ${format(rho, "kg/m^3")}`]);
};

const pressure = () => {
  const force = numberValue("pr-force");
  const area = numberValue("pr-area");
  const pressureValue = force / area;
  setOutput("pr-output", [`P = ${format(pressureValue, "Pa")}`]);
};

const hydrostatic = () => {
  const rho = numberValue("hy-rho");
  const depth = numberValue("hy-depth");
  const p0 = numberValue("hy-p0");
  const gauge = rho * G * depth;
  const absolute = p0 + gauge;
  setOutput("hy-output", [
    `P_gauge = ${format(gauge, "Pa")}`,
    `P_abs = ${format(absolute, "Pa")}`,
  ]);
};

const buoyant = () => {
  const rho = numberValue("bu-rho");
  const volume = numberValue("bu-volume");
  const mass = numberValue("bu-mass");
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
  const flow = area1 * velocity1;
  const velocity2 = flow / area2;
  setOutput("co-output", [
    `Q = ${format(flow, "m^3/s")}`,
    `v2 = ${format(velocity2, "m/s")}`,
  ]);
};

const bernoulli = () => {
  const rho = numberValue("be-rho");
  const p1 = numberValue("be-p1");
  const p2 = numberValue("be-p2");
  const v1 = numberValue("be-v1");
  const v2 = numberValue("be-v2");
  const y1 = numberValue("be-y1");
  const y2 = numberValue("be-y2");
  const computedP2 = p1 + 0.5 * rho * (v1 ** 2 - v2 ** 2) + rho * G * (y1 - y2);
  const headTerm = (p1 - p2) / rho + G * (y1 - y2);
  const computedV2 = Math.sqrt(Math.max(v1 ** 2 + 2 * headTerm, 0));
  setOutput("be-output", [
    `P2 (from v2) = ${format(computedP2, "Pa")}`,
    `v2 (from P2) = ${format(computedV2, "m/s")}`,
  ]);
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
  "float-check": floatCheck,
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
