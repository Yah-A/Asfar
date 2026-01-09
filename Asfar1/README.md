# Momentum Drop Lab

A small interactive webpage for a physics momentum assignment:

- Drop **3 balls** from a chosen **height**.
- Each ball has a different **mass**.
- When they hit the ground, the page shows impact **speed** and **momentum** using:
  - \(p = m v\)
  - \(v = \sqrt{2gh}\) (ignoring air resistance)

## How to run

Open `index1.html` in any modern browser (Chrome / Edge / Firefox).

If you prefer using a local server:

```bash
cd Asfar1
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Notes

- Gravity is set to \(g = 9.81\text{ m/s}^2\).
- Bounce is modeled with a coefficient of restitution \(e\) using \(v'=-e\,v\).
