AP Physics 1 Unit 8 Programming Project
=======================================

Title: Oscillations and Simple Harmonic Motion Lab

Overview
--------
This project builds a small command-line toolkit for oscillations. You will model
simple harmonic motion (SHM), calculate periods and frequencies, generate motion
tables for graphs, and compare energy at different positions in the cycle.

Learning Objectives (Oscillations)
----------------------------------
- Identify features of simple harmonic motion from restoring-force models.
- Calculate period, frequency, and angular frequency for springs and pendulums.
- Represent SHM with displacement, velocity, and acceleration vs. time.
- Compare kinetic and potential energy throughout an oscillation.

Project Structure
-----------------
- oscillations_lab.py  -> command-line toolkit for Unit 8 calculations
- samples/             -> sample CSV data for graphing practice
- output/              -> optional folder for JSON/CSV results (ignored by git)

Setup
-----
This project uses only the Python standard library.

Run the help menu:
  python3 oscillations_lab.py --help

Create an output folder if you want to save results:
  mkdir -p output

Part A: Defining Simple Harmonic Motion
---------------------------------------
Goal: Show that acceleration is proportional to displacement.

1) Generate a time series and make an a vs. x graph.
   python3 oscillations_lab.py shm-state \
     --amplitude 0.5 --period 2.0 --start 0 --stop 2.0 --step 0.25 \
     --output output/shm_series.csv

2) Plot acceleration vs. displacement and explain why the slope is negative.

Part B: Period and Frequency (Springs)
--------------------------------------
Goal: Connect period, frequency, and system parameters.

1) Compute period and frequency for a spring oscillator:
   python3 oscillations_lab.py spring-solve --mass 0.35 --k 18

2) Use the same data to solve for mass if the period is measured:
   python3 oscillations_lab.py spring-solve --k 18 --period 0.88

3) Explain how this could be used to "weigh" an astronaut in space.

Part C: Period and Frequency (Pendulums)
----------------------------------------
Goal: Use pendulum data to infer length.

1) Compute period and frequency for a simple pendulum:
   python3 oscillations_lab.py pendulum-solve --length 0.75

2) Measure a long string by timing oscillations:
   python3 oscillations_lab.py pendulum-solve --period 1.74

3) Explain why the small-angle assumption matters.

Part D: Representing SHM
------------------------
Goal: Compare position, velocity, and acceleration over time.

1) Compute the state at a single time:
   python3 oscillations_lab.py shm-state \
     --amplitude 0.3 --frequency 0.8 --time 0.40

2) Use the sample data in samples/shm_time_series.csv to sketch graphs.

Part E: Energy in SHM
---------------------
Goal: Compare kinetic and potential energy at different positions.

1) Compute energy at a given displacement:
   python3 oscillations_lab.py shm-energy --k 12 --amplitude 0.25 --position 0.10

2) Repeat for several positions and identify where kinetic energy is maximum.

Deliverables
------------
1) A short report (1-2 pages) with:
   - tables or graphs for each part
   - brief explanations connecting results to physics principles
2) Any data files you used (CSV or JSON output)
3) One extension of your choice (ideas below)

Extension Ideas
---------------
- Compare how changing amplitude affects total energy but not period.
- Build a phase-space plot (velocity vs. displacement).
- Use your data to estimate g from a pendulum experiment.

Notes
-----
Sample CSV files are in samples/. Use --output with .csv for tables:
  python3 oscillations_lab.py shm-state ... --output output/shm_series.csv
