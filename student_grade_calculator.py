import csv

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
        reader = csv.DictReader(file)

        for row in reader:
            name = row["Name"]
            scores = [
                float(row["Assignment1"]),
                float(row["Assignment2"]),
                float(row["Exam"])
            ]

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
    main()
