import csv
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class CsvWorkflowTests(unittest.TestCase):
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
