const G = 9.81; // m/s^2

/** @typedef {{name:string,color:string,mass:number,radiusPx:number,xFrac:number,y:number,v:number,impact?:{t:number,v:number,p:number,ke:number}}} Ball */

function clamp(n, a, b) {
  return Math.min(b, Math.max(a, n));
}

function fmt(n, digits = 2) {
  if (!Number.isFinite(n)) return "—";
  return n.toFixed(digits);
}

function setText(el, text) {
  if (!el) return;
  el.textContent = String(text);
}

function clearNode(el) {
  if (!el) return;
  while (el.firstChild) el.removeChild(el.firstChild);
}

function makeCell(text) {
  const td = document.createElement("td");
  td.textContent = text;
  return td;
}

function makeRow(cells) {
  const tr = document.createElement("tr");
  for (const c of cells) tr.appendChild(makeCell(c));
  return tr;
}

const dom = {
  canvas: /** @type {HTMLCanvasElement|null} */ (document.getElementById("simCanvas")),
  heightRange: /** @type {HTMLInputElement|null} */ (document.getElementById("heightRange")),
  heightNumber: /** @type {HTMLInputElement|null} */ (document.getElementById("heightNumber")),
  restitution: /** @type {HTMLInputElement|null} */ (document.getElementById("restitution")),
  restitutionOut: /** @type {HTMLOutputElement|null} */ (document.getElementById("restitutionOut")),
  dropBtn: /** @type {HTMLButtonElement|null} */ (document.getElementById("dropBtn")),
  resetBtn: /** @type {HTMLButtonElement|null} */ (document.getElementById("resetBtn")),
  pauseBtn: /** @type {HTMLButtonElement|null} */ (document.getElementById("pauseBtn")),
  gValue: document.getElementById("gValue"),
  theoryBody: document.querySelector("#theoryTable tbody"),
  measuredBody: document.querySelector("#measuredTable tbody"),
  note: document.getElementById("note"),
  massInputs: /** @type {HTMLInputElement[]} */ (Array.from(document.querySelectorAll(".massInput"))),
};

/** @type {{height:number,e:number,balls:Ball[],running:boolean,paused:boolean,t:number,lastTs:number|null}} */
const state = {
  height: 3,
  e: 0.75,
  balls: [
    {
      name: "Ball A",
      color: "#6ee7ff",
      mass: 0.5,
      radiusPx: 18,
      xFrac: 0.30,
      y: 0,
      v: 0,
    },
    {
      name: "Ball B",
      color: "#a7f3d0",
      mass: 1.0,
      radiusPx: 20,
      xFrac: 0.50,
      y: 0,
      v: 0,
    },
    {
      name: "Ball C",
      color: "#fde68a",
      mass: 2.0,
      radiusPx: 22,
      xFrac: 0.70,
      y: 0,
      v: 0,
    },
  ],
  running: false,
  paused: false,
  t: 0,
  lastTs: null,
};

function syncInitialUI() {
  setText(dom.gValue, fmt(G, 2));

  if (dom.heightRange) dom.heightRange.value = String(state.height);
  if (dom.heightNumber) dom.heightNumber.value = String(state.height);
  if (dom.restitution) dom.restitution.value = String(state.e);
  if (dom.restitutionOut) dom.restitutionOut.value = `e = ${fmt(state.e, 2)}`;

  for (let i = 0; i < state.balls.length; i += 1) {
    const input = dom.massInputs[i];
    if (!input) continue;
    input.value = String(state.balls[i].mass);
  }
}

function computeTheory() {
  const h = state.height;
  const v = Math.sqrt(2 * G * h);
  return state.balls.map((b) => {
    const p = b.mass * v;
    const ke = 0.5 * b.mass * v * v;
    return { name: b.name, mass: b.mass, v, p, ke };
  });
}

function renderTheoryTable() {
  const rows = computeTheory();
  clearNode(dom.theoryBody);
  for (const r of rows) {
    dom.theoryBody?.appendChild(
      makeRow([r.name, fmt(r.mass, 2), fmt(r.v, 3), fmt(r.p, 3), fmt(r.ke, 2)]),
    );
  }
}

function renderMeasuredTable() {
  clearNode(dom.measuredBody);
  for (const b of state.balls) {
    dom.measuredBody?.appendChild(
      makeRow([
        b.name,
        b.impact ? fmt(b.impact.t, 3) : "—",
        b.impact ? fmt(b.impact.v, 3) : "—",
        b.impact ? fmt(b.impact.p, 3) : "—",
        b.impact ? fmt(b.impact.ke, 2) : "—",
      ]),
    );
  }
}

function renderNote() {
  const vTheory = Math.sqrt(2 * G * state.height);
  const masses = state.balls.map((b) => b.mass);
  const minM = Math.min(...masses);
  const maxM = Math.max(...masses);
  if (minM <= 0 || maxM <= 0) {
    setText(dom.note, "");
    return;
  }
  const ratio = maxM / minM;
  setText(
    dom.note,
    `At height h = ${fmt(state.height, 2)} m, theory says impact speed is the same for all balls: v = √(2gh) ≈ ${fmt(
      vTheory,
      3,
    )} m/s. So momentum scales with mass: the heaviest ball has about ${fmt(
      ratio,
      2,
    )}× the momentum of the lightest (at the same v).`,
  );
}

function setHeight(h) {
  state.height = clamp(h, 0.5, 10);
  if (dom.heightRange) dom.heightRange.value = String(state.height);
  if (dom.heightNumber) dom.heightNumber.value = String(state.height);
  stopAndReset();
  renderTheoryTable();
  renderNote();
  draw();
}

function setRestitution(e) {
  state.e = clamp(e, 0, 1);
  if (dom.restitution) dom.restitution.value = String(state.e);
  if (dom.restitutionOut) dom.restitutionOut.value = `e = ${fmt(state.e, 2)}`;
  draw();
}

function stopAndReset() {
  state.running = false;
  state.paused = false;
  state.t = 0;
  state.lastTs = null;
  for (const b of state.balls) {
    b.y = 0;
    b.v = 0;
    delete b.impact;
  }
  renderMeasuredTable();
  updateButtons();
}

function updateButtons() {
  if (!dom.pauseBtn || !dom.dropBtn) return;
  dom.dropBtn.disabled = state.running && !state.paused;
  dom.pauseBtn.disabled = !state.running;
  dom.pauseBtn.textContent = state.paused ? "Resume" : "Pause";
}

function startDrop() {
  stopAndReset();
  state.running = true;
  state.paused = false;
  state.lastTs = null;
  updateButtons();
  requestAnimationFrame(loop);
}

function togglePause() {
  if (!state.running) return;
  state.paused = !state.paused;
  state.lastTs = null; // avoid big dt on resume
  updateButtons();
  if (!state.paused) requestAnimationFrame(loop);
}

function settleCheck() {
  // Consider "settled" if all balls are on the ground and nearly not moving.
  for (const b of state.balls) {
    if (Math.abs(b.v) > 0.001) return false;
    if (Math.abs(b.y - state.height) > 1e-6) return false;
  }
  return true;
}

function step(dt) {
  state.t += dt;
  const h = state.height;
  const e = state.e;

  for (const b of state.balls) {
    // Free fall (down is positive)
    b.v += G * dt;
    b.y += b.v * dt;

    if (b.y >= h) {
      // Impact
      const impactV = b.v; // downward, positive
      b.y = h;

      if (!b.impact) {
        const p = b.mass * impactV;
        const ke = 0.5 * b.mass * impactV * impactV;
        b.impact = { t: state.t, v: impactV, p, ke };
      }

      // Bounce (velocity reversal with restitution)
      const bouncedV = -e * impactV;
      // If the bounce is tiny, stop jittering.
      if (Math.abs(bouncedV) < 0.25) {
        b.v = 0;
      } else {
        b.v = bouncedV;
      }
    }
  }
}

function loop(ts) {
  if (!state.running || state.paused) return;

  if (state.lastTs == null) state.lastTs = ts;
  const rawDt = (ts - state.lastTs) / 1000;
  state.lastTs = ts;

  // Clamp dt for stability (tab switching etc.)
  const dt = clamp(rawDt, 0, 1 / 30);

  // Substep slightly for smoother impacts.
  const subSteps = dt > 1 / 90 ? 2 : 1;
  const sdt = dt / subSteps;
  for (let i = 0; i < subSteps; i += 1) step(sdt);

  renderMeasuredTable();
  draw();

  if (settleCheck()) {
    state.running = false;
    state.paused = false;
    updateButtons();
    return;
  }

  requestAnimationFrame(loop);
}

function draw() {
  const canvas = dom.canvas;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const w = canvas.width;
  const hPx = canvas.height;

  // Layout
  const pad = 26;
  const top = 26;
  const groundThickness = 18;
  const groundY = hPx - pad - groundThickness;
  const usable = groundY - top;
  const metersToPx = usable / state.height;

  // Background
  ctx.clearRect(0, 0, w, hPx);
  const bg = ctx.createLinearGradient(0, 0, 0, hPx);
  bg.addColorStop(0, "rgba(255,255,255,0.06)");
  bg.addColorStop(1, "rgba(0,0,0,0.35)");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, w, hPx);

  // Height ticks
  ctx.save();
  ctx.globalAlpha = 0.9;
  ctx.strokeStyle = "rgba(255,255,255,0.10)";
  ctx.fillStyle = "rgba(255,255,255,0.55)";
  ctx.lineWidth = 1;
  ctx.font = "12px ui-sans-serif, system-ui";

  const tickCount = Math.min(10, Math.max(3, Math.floor(state.height)));
  for (let i = 0; i <= tickCount; i += 1) {
    const yM = (state.height * i) / tickCount;
    const y = top + yM * metersToPx;
    ctx.beginPath();
    ctx.moveTo(pad, y);
    ctx.lineTo(w - pad, y);
    ctx.stroke();
    if (i === 0) {
      ctx.fillText("0 m (start)", pad + 6, y + 14);
    } else if (i === tickCount) {
      ctx.fillText(`${fmt(state.height, 2)} m (ground)`, pad + 6, y - 8);
    }
  }
  ctx.restore();

  // Ground
  ctx.save();
  ctx.fillStyle = "rgba(255,255,255,0.10)";
  ctx.fillRect(0, groundY, w, groundThickness);
  ctx.fillStyle = "rgba(255,255,255,0.16)";
  ctx.fillRect(0, groundY, w, 2);
  ctx.restore();

  // Balls
  for (const b of state.balls) {
    const x = b.xFrac * w;
    const y = top + b.y * metersToPx;

    // Shadow on ground
    const dy = groundY - y;
    const shadowAlpha = clamp(1 - dy / usable, 0, 1) * 0.35;
    ctx.save();
    ctx.globalAlpha = shadowAlpha;
    ctx.fillStyle = "rgba(0,0,0,0.7)";
    ctx.beginPath();
    ctx.ellipse(x, groundY + groundThickness / 2, b.radiusPx * 0.9, b.radiusPx * 0.35, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // Ball body
    const grad = ctx.createRadialGradient(
      x - b.radiusPx * 0.35,
      y - b.radiusPx * 0.35,
      b.radiusPx * 0.2,
      x,
      y,
      b.radiusPx * 1.1,
    );
    grad.addColorStop(0, "rgba(255,255,255,0.95)");
    grad.addColorStop(0.2, b.color);
    grad.addColorStop(1, "rgba(0,0,0,0.35)");

    ctx.save();
    ctx.fillStyle = grad;
    ctx.strokeStyle = "rgba(255,255,255,0.22)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(x, y, b.radiusPx, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.restore();

    // Label
    ctx.save();
    ctx.fillStyle = "rgba(255,255,255,0.86)";
    ctx.font = "12px ui-sans-serif, system-ui";
    ctx.fillText(`${b.name}  m=${fmt(b.mass, 2)}kg`, x - 55, y - b.radiusPx - 10);
    ctx.restore();
  }

  // HUD
  ctx.save();
  ctx.fillStyle = "rgba(255,255,255,0.75)";
  ctx.font = "12px ui-sans-serif, system-ui";
  const status = state.running ? (state.paused ? "Paused" : "Running") : "Ready";
  ctx.fillText(`t = ${fmt(state.t, 2)} s   |   h = ${fmt(state.height, 2)} m   |   e = ${fmt(state.e, 2)}   |   ${status}`, 20, 18);
  ctx.restore();
}

function wireEvents() {
  dom.heightRange?.addEventListener("input", () => setHeight(Number(dom.heightRange?.value)));
  dom.heightNumber?.addEventListener("input", () => setHeight(Number(dom.heightNumber?.value)));
  dom.restitution?.addEventListener("input", () => setRestitution(Number(dom.restitution?.value)));

  dom.dropBtn?.addEventListener("click", startDrop);
  dom.resetBtn?.addEventListener("click", () => {
    stopAndReset();
    draw();
  });
  dom.pauseBtn?.addEventListener("click", togglePause);

  dom.massInputs.forEach((input, idx) => {
    input.addEventListener("input", () => {
      const v = Number(input.value);
      // Keep masses positive and not crazy.
      state.balls[idx].mass = clamp(v, 0.05, 50);
      input.value = String(state.balls[idx].mass);
      stopAndReset();
      renderTheoryTable();
      renderNote();
      draw();
    });
  });
}

// Boot
syncInitialUI();
wireEvents();
renderTheoryTable();
renderMeasuredTable();
renderNote();
updateButtons();
draw();
