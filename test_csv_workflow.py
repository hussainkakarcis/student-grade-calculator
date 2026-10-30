import csv
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class CsvWorkflowTests(unittest.TestCase):
    def test_malformed_csv_workflow(self):
        project = Path(__file__).resolve().parent
        header = "Name,Assignment1,Assignment2,Exam\n"
        cases = [
            ("nonnumeric score", header + "Amina,92,88,invalid\n", "Row 2, Exam: enter a number"),
            ("blank score", header + "Amina,92,88,\n", "Row 2, Exam: score is required"),
            ("missing column", "Name,Assignment1,Assignment2\nAmina,92,88\n", "missing required column(s): Exam"),
            ("short row", header + "Amina,92,88\n", "Row 2, Exam: score is required"),
            ("missing name", header + ",92,88,90\n", "Row 2, Name: name is required"),
            ("empty file", "", "missing required column(s)"),
            ("duplicate header", "Name,Assignment1,Assignment2,Exam,Exam\n", "duplicate column names"),
            ("extra value", header + "Amina,92,88,90,extra\n", "Row 2: more values"),
            ("late invalid row", header + "Amina,92,88,90\nBilal,80,80,bad\n", "Row 3, Exam"),
        ]
        for value in ("nan", "inf", "-inf", "1e309", "-1", "101"):
            cases.append((value, header + f"Amina,92,88,{value}\n", "Row 2, Exam: score must be finite"))
        for label, contents, message in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as folder:
                workdir = Path(folder)
                (workdir / "students.csv").write_text(contents, encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, str(project / "student_grade_calculator.py")],
                    cwd=workdir,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(result.stderr.startswith("Error: "))
                self.assertIn(message, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse((workdir / "grade_results.csv").exists())

    def test_invalid_input_preserves_existing_output(self):
        project = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as folder:
            workdir = Path(folder)
            (workdir / "students.csv").write_text(
                "Name,Assignment1,Assignment2,Exam\nAmina,92,88,90\nBilal,80,80,bad\n"
            )
            output = workdir / "grade_results.csv"
            output.write_text("previous results\n")
            result = subprocess.run(
                [sys.executable, str(project / "student_grade_calculator.py")],
                cwd=workdir, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 1)
            self.assertEqual(output.read_text(), "previous results\n")

    def test_missing_input_file(self):
        project = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run(
                [sys.executable, str(project / "student_grade_calculator.py")],
                cwd=folder, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Error:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse((Path(folder) / "grade_results.csv").exists())

    def test_sample_csv_workflow(self):
        project = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as folder:
            workdir = Path(folder)
            shutil.copyfile(project / "students.csv", workdir / "students.csv")
            subprocess.run(
                [sys.executable, str(project / "student_grade_calculator.py")],
                cwd=workdir,
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            with (workdir / "grade_results.csv").open(newline="") as file:
                rows = list(csv.reader(file))

            self.assertEqual(rows, [
                ["Name", "Average", "LetterGrade"],
                ["Amina", "91.33", "A"],
                ["Bilal", "80.00", "B"],
                ["Sara", "70.67", "C"],
                ["Omar", "58.33", "F"],
                ["Layla", "95.00", "A"],
            ])


if __name__ == "__main__":
    unittest.main()
