# Rewriting to dynamically track current term index instead of hardcoding terms for required course placement
import json, random, itertools, numpy as np

random.seed(202); np.random.seed(202)

CORE = ["CMSC131", "CMSC132", "CMSC216", "CMSC250", "CMSC330", "CMSC351"]
AREAS = {
    "Cybersecurity": ["CMSC411", "CMSC412", "CMSC414", "CMSC416", "CMSC417"],
    "Machine Learning": ["CMSC420", "CMSC421", "CMSC422", "CMSC423", "CMSC424",
                         "CMSC426", "CMSC427", "CMSC470", "CMSC471", "CMSC472",
                         "CMSC320", "CMSC335"],
    "Software Engineering": ["CMSC430", "CMSC433", "CMSC434", "CMSC435", "CMSC436", "CMSC471"],
    "Theory": ["CMSC451", "CMSC452", "CMSC454", "CMSC456", "CMSC457", "CMSC474"],
    "Numerical Analysis": ["CMSC460", "CMSC466"]
}
UNASSIGNED_ELECTIVES = ["CMSC401", "CMSC425", "CMSC473", "CMSC475", "CMSC477"]
EARLY_ELECTIVES = {"CMSC320", "CMSC335"}
ALL_ELECTIVES = sorted(set(itertools.chain.from_iterable(AREAS.values())))
TERMS = ["Fall", "Spring"]

def tlabel(start, i): return f"{TERMS[i % 2]} {start + i // 2}"

def pick_interests():
    areas = list(AREAS.keys())
    first = random.choice(areas)
    extras = []
    if random.random() < 0.4:
        extras.append(random.choice([a for a in areas if a != first]))
    if first == "Numerical Analysis" and not extras:
        extras.append(random.choice([a for a in areas if a != "Numerical Analysis"]))
    return [first] + extras

def add_course(sem, idx, course, taken):
    sem.setdefault(idx, [])
    if course not in sem[idx]:
        sem[idx].append(course)
    taken.add(course)

def choose_term_decreasing(earliest, last):
    decay = 0.6
    ks = list(range(last - earliest + 1))
    probs = [decay ** k for k in ks]
    probs = [p / sum(probs) for p in probs]
    return earliest + np.random.choice(ks, p=probs)

def build_student():
    start = random.choice([2024, 2025, 2026])
    sem = {}
    taken = set()
    interests = pick_interests()
    pre = []

    random_math_number = random.random()

    if random_math_number < 0.65: pre.append("MATH140")
    if random_math_number < 0.4: pre.append("MATH141")
    if random.random() < 0.5: pre.append("CMSC131")
    if random.random() < 0.3 and {"CMSC131", "MATH140"}.issubset(pre): pre.append("CMSC132")
    if random.random() < 0.025 and {"MATH140", "MATH141"}.issubset(pre): pre.append("OTHER_MATH4XX")
    taken.update(pre)

    current_term = 0

    # Place MATH140 as early as possible
    if "MATH140" not in pre:
        add_course(sem, current_term, "MATH140", taken)
        add_course(sem, current_term + 1, "MATH141", taken)
        idx_math141 = current_term + 1

        if "CMSC131" not in pre:
            add_course(sem, current_term, "CMSC131", taken)

        add_course(sem, current_term + 1, "CMSC132", taken)

        current_term += 2
    elif "MATH141" not in pre:
        add_course(sem, current_term, "MATH141", taken)
        idx_math141 = current_term

        if "CMSC131" not in pre:
            add_course(sem, current_term, "CMSC131", taken)
            add_course(sem, current_term + 1, "CMSC132", taken)
            current_term += 2
        else:
            add_course(sem, current_term, "CMSC132", taken)
            current_term += 1
    else:
        if "CMSC131" not in pre:
            add_course(sem, current_term, "CMSC131", taken)
            add_course(sem, current_term + 1, "CMSC132", taken)
            current_term += 2
        elif "CMSC131" not in pre:
            add_course(sem, current_term, "CMSC132", taken)
            current_term += 1
        else:
            pass
        idx_math141 = current_term - 1


    for c in ["CMSC216", "CMSC250"]:
        if c not in taken:
            add_course(sem, current_term, c, taken)
    idx_after_216 = current_term
    current_term += 1

    for c in ["CMSC330", "CMSC351"]:
        if c not in taken:
            add_course(sem, current_term, c, taken)
    if random.random() < 0.15 and "CMSC320" not in taken:
        add_course(sem, current_term, "CMSC320", taken)
    idx_after_330 = current_term
    current_term += 1

    area_counts = {a: 0 for a in AREAS}
    elective_needed = 7 - len([c for c in taken if c.startswith("CMSC") and c not in CORE])

    elective_needed = 7 - len([c for c in taken if c.startswith("CMSC") and c not in CORE])
    last_term = 7  # or compute dynamically

    while elective_needed > 0 and current_term <= last_term:
        # capacity for CMSC courses this term
        cs_courses = [c for c in sem.get(current_term, []) if c.startswith("CMSC")]
        cs_cap     = 3 - len(cs_courses)
        if cs_cap <= 0:
            current_term += 1
            continue

        # how many terms remain (including this one)
        terms_left     = last_term - current_term + 1
        electives_left = elective_needed

        # minimum to take this term: floor(n/k), but at least 1
        min_per_term = max(1, electives_left // terms_left)
        max_per_term = min(3, cs_cap)

        # pick how many electives to schedule this term
        m = random.randint(min_per_term, max_per_term)

        for _ in range(m):
            # pick one valid elective exactly as before
            area = random.choice(
                [a for a in interests if area_counts[a] < 3] or
                [a for a in AREAS if area_counts[a] == 0] or
                list(AREAS.keys())
            )
            candidates = [e for e in AREAS[area] if e not in taken]
            if not candidates:
                candidates = [e for e in ALL_ELECTIVES if e not in taken]
            if not candidates:
                candidates = [e for e in UNASSIGNED_ELECTIVES if e not in taken]
            if not candidates:
                break

            elective = random.choice(candidates)
            # respect early‐elective constraints
            if elective in EARLY_ELECTIVES and current_term <= idx_after_216:
                continue
            if elective not in EARLY_ELECTIVES and current_term <= idx_after_330:
                continue

            add_course(sem, current_term, elective, taken)
            if elective in ALL_ELECTIVES:
                for a, lst in AREAS.items():
                    if elective in lst:
                        area_counts[a] += 1

            elective_needed -= 1
            if elective_needed <= 0:
                break

        # move on to next term
        current_term += 1

    last_term = max(sem.keys())
    for mc in ["STAT4XX", "OTHER_MATH4XX"]:
        if mc in taken: continue
        earliest = idx_math141 + 1
        term_choice = choose_term_decreasing(earliest, last_term)
        add_course(sem, term_choice, mc, taken)

    classes = [{tlabel(start, i): sem[i]} for i in sorted(sem) if sem[i]]
    return {"start_semester": tlabel(start, 0), "precollege": pre, "classes": classes, "interests": interests}

students = []
while len(students) < 1000:
    s = build_student()
    courses = set(s["precollege"])
    for blk in s["classes"]:
        courses.update(next(iter(blk.values())))
    electives = [c for c in courses if c.startswith("CMSC") and c not in CORE]
    areas = {a for a, lst in AREAS.items() if any(e in lst for e in electives)}
    if len(electives) >= 7 and len(areas) >= 3 and all(c in courses for c in CORE) and {"MATH140", "MATH141", "STAT4XX", "OTHER_MATH4XX"}.issubset(courses):
        students.append(s)

out_path = "course_recommendation_dataset_final_v9.json"
with open(out_path, "w") as f:
    json.dump(students, f, indent=2)
