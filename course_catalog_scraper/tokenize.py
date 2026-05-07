import json
import csv
from pathlib import Path

# --- CONFIG ---
SEM_TOKEN = "<SEM>"
INT_PREFIX = "<INT_"
INT_SUFFIX = ">"
INTERESTS = [
    "Cybersecurity", "Machine Learning",
    "Software Engineering", "Theory", "Numerical Analysis"
]
# path to your files
STUDENTS_JSON = Path("course_recommendation_dataset_final_v9.json")
USED_CSV       = Path("used_courses.csv")
# ----------------

# 1. Load your used_courses vocabulary
with USED_CSV.open() as f:
    reader = csv.reader(f)
    # assuming one course code per row
    used_courses = {row[0] for row in reader if row}

# 2. Load the student plans
with STUDENTS_JSON.open() as f:
    students = json.load(f)

all_sequences = []

for student in students:
    seq = []

    # 3. Add interest tokens (if any), sorted for consistency
    for interest in sorted(student["interests"]):
        tag = f"{INT_PREFIX}{interest.replace(' ', '_')}{INT_SUFFIX}"
        seq.append(tag)

    # 4. Always start with SEM_TOKEN
    seq.append(SEM_TOKEN)

    # 5. Precollege block (if present)
    pre = student.get("precollege", [])
    for course in pre:
        if course in used_courses:
            seq.append(course)
    # close precollege with another SEM
    seq.append(SEM_TOKEN)

    # 6. Semester blocks
    for sem_block in student["classes"]:
        # each sem_block is a dict like {"Fall 2025": ["CMSC131", ...]}
        for sem_label, courses in sem_block.items():
            # add each course, then a SEM_TOKEN to mark end of that term
            for course in courses:
                if course in used_courses:
                    seq.append(course)
            seq.append(SEM_TOKEN)

    all_sequences.append(seq)

# Example: inspect first few
for i, s in enumerate(all_sequences[:6], 1):
    print(f"Student #{i} sequence:")
    print(" ".join(s))
    print()

OUT_PATH = "all_student_sequences.txt"
with open(OUT_PATH, "w") as fw:
    for seq in all_sequences:
        # join tokens with spaces; the tokenizer will split on whitespace
        fw.write(" ".join(seq) + "\n")
