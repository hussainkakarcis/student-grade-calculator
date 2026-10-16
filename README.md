# Student Grade Calculator

## What this project does
This Python project reads student grade data from a CSV file, calculates each student's average, assigns a letter grade, displays the results, and saves the results to a new CSV file.

## Files
- `student_grade_calculator.py` - main Python program
- `students.csv` - sample student grade data
- `grade_results.csv` - generated after the program runs
- `test_student_grade_calculator.py` - automated calculation and grade-boundary tests
- `test_csv_workflow.py` - end-to-end validation of the supplied CSV sample

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
This covers the supplied valid sample; malformed-input handling is not tested.

## Skills demonstrated
- Python functions
- CSV file reading/writing
- Lists and dictionaries
- Loops
- Conditional statements
- Basic data processing

## Resume description supported by this project
Built a Python grade calculator that processes CSV records, computes equal-weight averages, assigns letter grades, and exports formatted results; verified all five sample records against expected output.
