# Section 4: AI-Assisted Debugging & Code Understanding Exercise
# We will ask an AI coding assistant to:
#   1) Explain what this function does in plain English
#   2) Find and fix the 3 bugs hidden below!

def summarize_candidate(profile):
    name = profile["full_name"]
    exp = profile["experience_years"]
    skills = profile["skills"]

    # Bug 1: TypeError when concatenating string + integer
    headline = name + " has " + exp + " years of experience."

    # Bug 2: Wrong key name ('skill_list' instead of 'skills')
    top_skill = profile["skill_list"][0]

    # Bug 3: Division by zero if skills list is empty
    avg_len = sum(len(s) for s in skills) / len(skills)

    return headline + " Top skill: " + top_skill


if __name__ == "__main__":
    sample = {"full_name": "Anita Verma", "experience_years": 4, "skills": ["Python", "SQL"]}
    print(summarize_candidate(sample))
