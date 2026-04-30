AP Physics 1 Unit 9 Programming Project
=======================================

Title: Fluids and Buoyancy Lab

Overview
--------
This project builds a small command-line toolkit for fluids. You will calculate
density, pressure, buoyant force, and flow properties, then connect those results
to conservation laws in fluids.

Learning Objectives (Fluids)
----------------------------
- Describe fluids and compute density from mass and volume.
- Calculate pressure on surfaces and in static fluids.
- Apply Archimedes’ principle to buoyancy and floating.
- Use continuity and Bernoulli’s equation for fluid flow.

Project Structure
-----------------
- fluids_lab.py        -> command-line toolkit for Unit 9 calculations
- samples/             -> sample CSV data for graphing practice
- output/              -> optional folder for JSON/CSV results (ignored by git)

Setup
-----
This project uses only the Python standard library.

Run the help menu:
  python3 fluids_lab.py --help

Create an output folder if you want to save results:
  mkdir -p output

Part A: Density and Internal Structure
--------------------------------------
Goal: Use density to compare materials.

1) Compute density from mass and volume:
   python3 fluids_lab.py density --mass 0.85 --volume 0.00095

2) Solve for volume of an unknown sample:
   python3 fluids_lab.py density --mass 0.72 --volume 0.0008

3) Explain why objects with lower density than water float.

Part B: Pressure in Fluids
--------------------------
Goal: Compare surface pressure and hydrostatic pressure.

1) Pressure from a perpendicular force:
   python3 fluids_lab.py pressure --force 480 --area 0.08

2) Gauge and absolute pressure at depth:
   python3 fluids_lab.py hydrostatic --density 1000 --depth 4.2

3) Generate a pressure vs. depth table:
   python3 fluids_lab.py pressure-table --depths 0,1,2,3,4,5,6 --density 1000 \
     --output output/pressure_depth.csv

Part C: Buoyancy and Newton’s Laws
----------------------------------
Goal: Use Archimedes’ principle to predict floating.

1) Compute buoyant force on a submerged object:
   python3 fluids_lab.py buoyant --density 1000 --volume 0.003 --mass 0.0

2) Compare buoyant force to weight:
   python3 fluids_lab.py buoyant --density 1000 --volume 0.003 \
     --mass 2.2

3) Describe what happens when the object density is greater than the fluid density.

Part D: Conservation Laws in Fluids
------------------------------------
Goal: Use continuity and Bernoulli’s equation.

1) Continuity in a pipe:
   python3 fluids_lab.py continuity --area1 0.004 --velocity1 1.6 --area2 0.0015

2) Check float vs sink for a sample:
   python3 fluids_lab.py float-check --object-density 850 --fluid-density 1000

3) Pressure change between two points:
   python3 fluids_lab.py bernoulli \
     --density 1000 --pressure1 180000 --velocity1 1.2 --height1 0.4 \
     --velocity2 2.8 --height2 1.1

4) Torricelli’s theorem (tank outflow speed):
   python3 fluids_lab.py torricelli --height 1.3

Deliverables
------------
1) A short report (1-2 pages) with:
   - tables or graphs for each part
   - brief explanations connecting results to physics principles
2) Any CSV or JSON files you used
3) One extension of your choice (ideas below)

Extension Ideas
---------------
- Use density data to rank unknown materials.
- Compare pressure vs. depth for freshwater vs. saltwater.
- Analyze how changing pipe area changes flow speed and pressure.

Notes
-----
Use the --output flag to save JSON results:
  python3 fluids_lab.py density ... --output output/partA.json
