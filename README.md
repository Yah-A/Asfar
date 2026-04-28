AP Physics 1 Unit 6 Programming Project
=======================================

Title: Energy and Momentum of Rotating Systems Lab

Overview
--------
This project builds a command-line toolkit for Unit 6 topics: rotational kinetic
energy, torque and work, angular momentum and impulse, conservation of angular
momentum, rolling without slipping, and orbiting satellites. You will compute
quantities, compare scenarios, and generate data tables for graphs.

Learning Objectives (Unit 6)
----------------------------
- Describe rotational kinetic energy and relate it to rotational inertia.
- Connect torque and angular displacement to work.
- Use angular momentum and angular impulse to predict changes in rotation.
- Apply conservation of angular momentum to changing systems.
- Model rolling without slipping and compare shapes.
- Analyze circular and elliptical orbits using conservation principles.

Project Structure
-----------------
- rotating_systems.py  -> command-line toolkit for calculations
- samples/             -> sample CSV data for torque graphs
- output/              -> optional folder for JSON results (ignored by git)

Setup
-----
This project uses only the Python standard library.

Run the help menu:
  python3 rotating_systems.py --help

Create an output folder if you want to save results:
  mkdir -p output

Part A: Rotational Kinetic Energy
---------------------------------
Goal: Compare how rotational inertia changes the kinetic energy.

1) Use the same mass, radius, and angular speed for three shapes.
   Example:
     python3 rotating_systems.py rotational-energy \
       --shape disk --mass 2 --radius 0.3 --omega 12
     python3 rotating_systems.py rotational-energy \
       --shape ring --mass 2 --radius 0.3 --omega 12
     python3 rotating_systems.py rotational-energy \
       --shape sphere --mass 2 --radius 0.3 --omega 12

2) In a short paragraph, explain why the energies differ.
   Connect the differences to the moment of inertia.

Part B: Torque and Work
-----------------------
Goal: Relate torque, angular displacement, and work.

1) Use the constant-torque mode:
  python3 rotating_systems.py torque-work --torque 4 --angle 2.5

2) Create a torque vs angle table (theta, torque), then compute work:
   python3 rotating_systems.py torque-work \
     --data-file samples/torque_vs_angle.csv

3) Sketch the torque vs angle graph and estimate the area by hand.
   Compare your estimate with the program output.

Part C: Angular Momentum and Angular Impulse
---------------------------------------------
Goal: Connect torque over time to changes in angular momentum.

1) Compute angular momentum for a rotating object:
   python3 rotating_systems.py angular-momentum \
     --shape disk --mass 1.2 --radius 0.25 --omega 18

2) Compute angular impulse for a torque pulse:
   python3 rotating_systems.py angular-impulse --torque 3.2 --time 0.8

3) Use a torque vs time table to compute impulse and compare:
   python3 rotating_systems.py angular-impulse \
     --data-file samples/torque_vs_time.csv

Part D: Conservation of Angular Momentum
-----------------------------------------
Goal: Model a skater pulling in arms or a collapsing star.

1) Compute a new angular speed for the same system:
   python3 rotating_systems.py conservation --I1 1.8 --omega1 2.5 --I2 0.6

2) Explain why angular speed changes when the moment of inertia changes.

Part E: Rolling Without Slipping
--------------------------------
Goal: Compare translational and rotational energy for rolling objects.

1) Compare a solid disk, hoop, and solid sphere on the same incline:
   python3 rotating_systems.py rolling \
     --shape disk --mass 2 --radius 0.2 --height 0.8
   python3 rotating_systems.py rolling \
     --shape ring --mass 2 --radius 0.2 --height 0.8
   python3 rotating_systems.py rolling \
     --shape sphere --mass 2 --radius 0.2 --height 0.8

2) Rank the objects by final speed and explain using energy and inertia.

Part F: Orbiting Satellites
---------------------------
Goal: Use energy and angular momentum in orbital motion.

1) Circular orbit:
   python3 rotating_systems.py orbit --type circular \
     --central-mass 5.97e24 --radius 7.0e6 --sat-mass 500

2) Elliptical orbit with periapsis/apoapsis:
   python3 rotating_systems.py orbit --type elliptical \
     --central-mass 5.97e24 --periapsis 7.0e6 --apoapsis 1.2e7 --sat-mass 500

3) Answer the essential question: why do satellites move faster at periapsis?

Part G: Escape Velocity
-----------------------
Goal: Compute the escape speed from a central body.

1) Example:
   python3 rotating_systems.py escape --central-mass 5.97e24 --radius 6.37e6

Deliverables
------------
1) A short report (1-2 pages) with:
   - tables or graphs for each part
   - brief explanations connecting results to physics principles
2) Any data files you used (CSV or JSON output)
3) One extension of your choice (ideas below)

Extension Ideas
---------------
- Compare energy loss when rolling with slipping vs without slipping.
- Build a parameter sweep (loop) to create a data table for graphs.
- Explore how changing system selection affects angular momentum.
- Test how changing orbit radius affects period and energy.

Notes
-----
Sample CSV files can have headers "theta,torque" or "time,torque".
Use the --output flag to save JSON results:
  python3 rotating_systems.py rotational-energy ... --output output/partA.json
