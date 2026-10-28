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
            ("nonnumeric score", header + "Amina,92,88,invalid\n", "ValueError"),
            ("blank score", header + "Amina,92,88,\n", "ValueError"),
            ("missing column", "Name,Assignment1,Assignment2\nAmina,92,88\n", "KeyError"),
            ("short row", header + "Amina,92,88\n", "TypeError"),
        ]
        for label, contents, exception in cases:
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
                self.assertTrue(result.stderr.splitlines()[-1].startswith(exception + ":"))
                self.assertFalse((workdir / "grade_results.csv").exists())

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
