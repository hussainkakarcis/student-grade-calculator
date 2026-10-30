import unittest
from student_grade_calculator import calculate_average, get_letter_grade, parse_score


class GradeCalculatorTests(unittest.TestCase):
    def test_valid_score_limits(self):
        for value, expected in [("0", 0), ("100", 100), (" 85.5 ", 85.5)]:
            with self.subTest(value=value):
                self.assertEqual(parse_score(value, 2, "Exam"), expected)

    def test_sample_average(self):
        self.assertAlmostEqual(calculate_average([92, 88, 94]), 274 / 3)

    def test_grade_boundaries(self):
        cases = [
            (0, "F"), (59.99, "F"), (60, "D"), (69.99, "D"),
            (70, "C"), (79.99, "C"), (80, "B"), (89.99, "B"),
            (90, "A"), (100, "A"),
        ]
        for average, expected in cases:
            with self.subTest(average=average):
                self.assertEqual(get_letter_grade(average), expected)


if __name__ == "__main__":
    unittest.main()
