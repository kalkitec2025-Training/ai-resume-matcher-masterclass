# Section 2: Python – The Foundation of Modern Development (Completed)

candidate_name = "Rahul Sharma"
years_experience = 3

resume_skills = ["Python", "SQL", "FastAPI", "Git"]
job_required_skills = ["Python", "FastAPI", "PostgreSQL", "Docker", "Git"]


def calculate_match(candidate_skills: list[str], required_skills: list[str]) -> dict:
    # Normalize to lowercase for accurate comparison
    cand_set = {skill.lower() for skill in candidate_skills}

    matched = []
    missing = []

    for skill in required_skills:
        if skill.lower() in cand_set:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(required_skills)) * 100) if required_skills else 0

    return {
        "candidate": candidate_name,
        "match_score": score,
        "matching_skills": matched,
        "missing_skills": missing,
    }


if __name__ == "__main__":
    result = calculate_match(resume_skills, job_required_skills)
    print("Match Score:", f"{result['match_score']}%")
    print("Matched Skills:", result["matching_skills"])
    print("Missing Skills:", result["missing_skills"])
