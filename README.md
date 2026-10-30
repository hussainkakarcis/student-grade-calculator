# Student Grade Calculator

[![Tests](https://github.com/hussainkakarcis/student-grade-calculator/actions/workflows/tests.yml/badge.svg)](https://github.com/hussainkakarcis/student-grade-calculator/actions/workflows/tests.yml)

## What this project does
This Python project reads student grade data from a CSV file, calculates each student's average, assigns a letter grade, displays the results, and saves the results to a new CSV file.

## Files
- `student_grade_calculator.py` - main Python program
- `students.csv` - sample student grade data
- `grade_results.csv` - generated after the program runs
- `test_student_grade_calculator.py` - automated calculation and grade-boundary tests
- `test_csv_workflow.py` - end-to-end tests of the supplied CSV sample and malformed inputs

## How to run
1. Install Python 3.
2. Put `student_grade_calculator.py` and `students.csv` in the same folder.
3. Open a terminal in that folder.
4. Run:

```bash
python student_grade_calculator.py
```

## Validation example

Run `python student_grade_calculator.py` with the included
`students.csv`. The generated `grade_results.csv` should contain:

```csv
Name,Average,LetterGrade
Amina,91.33,A
Bilal,80.00,B
Sara,70.67,C
Omar,58.33,F
Layla,95.00,A
```

For example, Amina's average is (92 + 88 + 94) / 3 = 91.333...,
displayed as 91.33 with letter grade A.

All three scores have equal weight. Letter grades use the unrounded
average: A >= 90, B >= 80, C >= 70, D >= 60, and F < 60.
Exported averages are formatted to two decimal places.

## Automated tests

From the project folder, run:

```bash
python -m unittest -v
```

The tests check a sample average and 10 letter-grade cases, including
values at and just below each passing-grade boundary. They use Python's
built-in `unittest` module and require no additional packages.
An end-to-end test also runs the unchanged script with the included
`students.csv` in a temporary folder and checks the generated CSV header
and all five expected records, including row order, two-decimal averages,
and letter grades. It leaves the repository's CSV files untouched.
Input validation requires the Name, Assignment1, Assignment2, and Exam columns,
a nonblank name, and finite numeric scores from 0 through 100 (inclusive).
Invalid input produces a concise `Error:` message with the record row and field
where applicable, exits with status 1, and does not create or overwrite the
output CSV. Record rows count the header as row 1. Correct the input and rerun;
an output left from an earlier successful run is not a new result.

Tests cover missing/blank/nonnumeric scores, missing names and columns,
duplicate headers, extra values, short rows, non-finite and out-of-range scores,
missing input files, and preservation of previous output when a later row is
invalid. Valid sample output remains unchanged.

GitHub Actions runs `python -m unittest -v` on every push and pull request,
using Python 3.12 on Ubuntu. The workflow uses Node 24-based checkout and
setup-python actions.

## Skills demonstrated
- Python functions
- CSV file reading/writing
- Lists and dictionaries
- Loops
- Conditional statements
- Basic data processing

## Resume description supported by this project
Built a Python grade calculator that processes CSV records, computes equal-weight averages, assigns letter grades, and exports formatted results; verified all five sample records against expected output.
