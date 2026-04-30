const G = 6.6743e-11;

const fmt = (value, unit) => {
  const abs = Math.abs(value);
  if (abs >= 1e4 || (abs > 0 && abs < 1e-3)) {
    return `${value.toExponential(3)} ${unit}`;
  }
  return `${value.toFixed(4)} ${unit}`;
};

const inertia = (shape, mass, radius) => {
  if (shape === "disk") {
    return { I: 0.5 * mass * radius ** 2, beta: 0.5 };
  }
  if (shape === "ring") {
    return { I: mass * radius ** 2, beta: 1.0 };
  }
  if (shape === "sphere") {
    return { I: 0.4 * mass * radius ** 2, beta: 0.4 };
  }
  throw new Error("Unknown shape");
};

const parseNumber = (id) => Number(document.getElementById(id).value);
const parseSelect = (id) => document.getElementById(id).value;

const setOutput = (id, lines) => {
  document.getElementById(id).textContent = lines.join("\n");
};

const handleRotEnergy = () => {
  const shape = parseSelect("re-shape");
  const mass = parseNumber("re-mass");
  const radius = parseNumber("re-radius");
  const omega = parseNumber("re-omega");
  const { I } = inertia(shape, mass, radius);
  const kRot = 0.5 * I * omega ** 2;
  setOutput("re-output", [fmt(I, "kg·m^2"), fmt(kRot, "J")]);
};

const handleTorqueWork = () => {
  const torque = parseNumber("tw-torque");
  const angle = parseNumber("tw-angle");
  const work = torque * angle;
  setOutput("tw-output", [fmt(work, "J")]);
};

const handleAngularMomentum = () => {
  const mode = parseSelect("am-mode");
  const mass = parseNumber("am-mass");
  const radius = parseNumber("am-radius");
  if (mode === "rigid") {
    const omega = parseNumber("am-omega");
    const shape = parseSelect("am-shape");
    const { I } = inertia(shape, mass, radius);
    const L = I * omega;
    setOutput("am-output", [fmt(L, "kg·m^2/s")]);
    return;
  }
  const speed = parseNumber("am-speed");
  const angleDeg = parseNumber("am-angle");
  const angle = (Math.PI / 180) * angleDeg;
  const L = radius * mass * speed * Math.sin(angle);
  setOutput("am-output", [fmt(L, "kg·m^2/s")]);
};

const handleAngularImpulse = () => {
  const torque = parseNumber("ai-torque");
  const time = parseNumber("ai-time");
  const impulse = torque * time;
  setOutput("ai-output", [fmt(impulse, "N·m·s")]);
};

const handleConservation = () => {
  const i1 = parseNumber("co-i1");
  const omega1 = parseNumber("co-omega1");
  const i2 = parseNumber("co-i2");
  const omega2 = (omega1 * i1) / i2;
  setOutput("co-output", [fmt(omega2, "rad/s")]);
};

const handleRolling = () => {
  const shape = parseSelect("ro-shape");
  const mass = parseNumber("ro-mass");
  const radius = parseNumber("ro-radius");
  const height = parseNumber("ro-height");
  const { I, beta } = inertia(shape, mass, radius);
  const g = 9.81;
  const v = Math.sqrt((2 * g * height) / (1 + beta));
  const omega = v / radius;
  const kTrans = 0.5 * mass * v ** 2;
  const kRot = 0.5 * I * omega ** 2;
  setOutput("ro-output", [
    `v_cm = ${fmt(v, "m/s")}`,
    `omega = ${fmt(omega, "rad/s")}`,
    `K_trans = ${fmt(kTrans, "J")}`,
    `K_rot = ${fmt(kRot, "J")}`,
  ]);
};

const handleOrbit = () => {
  const type = parseSelect("or-type");
  const central = parseNumber("or-central");
  const sat = parseNumber("or-sat");
  if (type === "circular") {
    const radius = parseNumber("or-radius");
    const v = Math.sqrt((G * central) / radius);
    const L = sat * v * radius;
    const K = 0.5 * sat * v ** 2;
    const U = (-G * central * sat) / radius;
    const E = K + U;
    const T = (2 * Math.PI * radius) / v;
    setOutput("or-output", [
      `v_orbit = ${fmt(v, "m/s")}`,
      `L = ${fmt(L, "kg·m^2/s")}`,
      `K = ${fmt(K, "J")}`,
      `U = ${fmt(U, "J")}`,
      `E = ${fmt(E, "J")}`,
      `T = ${fmt(T, "s")}`,
    ]);
    return;
  }
  const peri = parseNumber("or-peri");
  const apo = parseNumber("or-apo");
  const semiMajor = 0.5 * (peri + apo);
  const vPeri = Math.sqrt(G * central * (2 / peri - 1 / semiMajor));
  const vApo = Math.sqrt(G * central * (2 / apo - 1 / semiMajor));
  const L = sat * peri * vPeri;
  const E = (-G * central * sat) / (2 * semiMajor);
  const T = 2 * Math.PI * Math.sqrt(semiMajor ** 3 / (G * central));
  setOutput("or-output", [
    `v_periapsis = ${fmt(vPeri, "m/s")}`,
    `v_apoapsis = ${fmt(vApo, "m/s")}`,
    `L = ${fmt(L, "kg·m^2/s")}`,
    `E = ${fmt(E, "J")}`,
    `T = ${fmt(T, "s")}`,
  ]);
};

const handleEscape = () => {
  const central = parseNumber("es-central");
  const radius = parseNumber("es-radius");
  const v = Math.sqrt((2 * G * central) / radius);
  setOutput("es-output", [fmt(v, "m/s")]);
};

const actions = {
  "rot-energy": handleRotEnergy,
  "torque-work": handleTorqueWork,
  "angular-momentum": handleAngularMomentum,
  "angular-impulse": handleAngularImpulse,
  conservation: handleConservation,
  rolling: handleRolling,
  orbit: handleOrbit,
  escape: handleEscape,
};

document.querySelectorAll("button[data-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const action = button.dataset.action;
    actions[action]?.();
  });
});

handleRotEnergy();
handleTorqueWork();
handleAngularMomentum();
handleAngularImpulse();
handleConservation();
handleRolling();
handleOrbit();
handleEscape();
