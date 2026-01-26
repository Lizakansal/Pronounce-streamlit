import re

def free_speech_accuracy(spoken_text):
    if not spoken_text or len(spoken_text.strip()) == 0:
        return 0, "No clear speech detected"

    text = spoken_text.lower().strip()
    words = text.split()

    # Metrics

    fillers = ["um", "uh", "erm", "hmm", "ah"]
    filler_count = sum(1 for w in words if w in fillers)

    repetition_penalty = 0
    for i in range(len(words)-1):
        if words[i] == words[i+1]:
            repetition_penalty += 1

    broken_words = [w for w in words if len(w) == 1]
    broken_penalty = len(broken_words)

    has_structure = bool(re.search(r"[a-zA-Z]+\s+[a-zA-Z]+", text))

    unique_ratio = len(set(words)) / max(len(words), 1)

    # Scoring

    score = 100

    # penalties
    score -= filler_count * 7
    score -= repetition_penalty * 6
    score -= broken_penalty * 5

    if not has_structure:
        score -= 15

    if unique_ratio < 0.5:
        score -= 10

    # clamp score
    score = max(30, min(score, 95))

    #Feedback 

    if score >= 85:
        feedback = "Very clear pronunciation and fluent speech"
    elif score >= 70:
        feedback = "Good clarity, minor pronunciation issues"
    elif score >= 55:
        feedback = "Average clarity, improve fluency and articulation"
    else:
        feedback = "Low clarity, speak slower and clearer"

    return score, feedback
