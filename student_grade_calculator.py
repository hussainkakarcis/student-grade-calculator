import csv
import math
import sys


SCORE_FIELDS = ("Assignment1", "Assignment2", "Exam")


def parse_score(value, row_number, field):
    prefix = f"Row {row_number}, {field}"
    if value is None or not value.strip():
        raise ValueError(f"{prefix}: score is required.")
    try:
        score = float(value)
    except ValueError:
        raise ValueError(f"{prefix}: enter a number from 0 to 100.") from None
    if not math.isfinite(score) or not 0 <= score <= 100:
        raise ValueError(f"{prefix}: score must be finite and between 0 and 100.")
    return score

def calculate_average(scores):
    return sum(scores) / len(scores)

def get_letter_grade(average):
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"

def main():
    input_file = "students.csv"
    output_file = "grade_results.csv"

    results = []

    with open(input_file, "r", newline="") as file:
        reader = csv.DictReader(file, strict=True)
        required = ("Name",) + SCORE_FIELDS
        missing = [field for field in required if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("CSV header: missing required column(s): " + ", ".join(missing))
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("CSV header: duplicate column names are not allowed.")

        for row_number, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(f"Row {row_number}: more values than header columns.")
            name = row["Name"]
            if name is None or not name.strip():
                raise ValueError(f"Row {row_number}, Name: name is required.")
            scores = [parse_score(row[field], row_number, field) for field in SCORE_FIELDS]

            average = calculate_average(scores)
            letter_grade = get_letter_grade(average)

            results.append({
                "Name": name,
                "Average": f"{average:.2f}",
                "LetterGrade": letter_grade
            })

    print("Student Grade Results")
    print("-" * 30)

    for result in results:
        print(
            f'{result["Name"]}: '
            f'{result["Average"]}% - {result["LetterGrade"]}'
        )

    with open(output_file, "w", newline="") as file:
        fieldnames = ["Name", "Average", "LetterGrade"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
