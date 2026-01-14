import re

# Psychological keyword dictionaries
STRESS_WORDS = [
    "stress", "anxiety", "pressure", "depression", "mental", "panic",
    "harassment", "unsafe", "fear", "scared", "threat", "abuse"
]

ANGER_WORDS = [
    "angry", "frustrated", "irritated", "annoyed", "furious",
    "complain", "worst", "hate"
]

def analyze_psychological_state(text):
    text = text.lower()

    stress_count = sum(1 for word in STRESS_WORDS if re.search(rf"\b{word}\b", text))
    anger_count = sum(1 for word in ANGER_WORDS if re.search(rf"\b{word}\b", text))

    stress_score = stress_count * 2 + anger_count

    # Emotion detection
    if stress_count >= 2:
        emotion = "Stress"
    elif anger_count >= 2:
        emotion = "Anger"
    else:
        emotion = "Neutral"

    # Priority logic
    if stress_score >= 5:
        priority = "Critical"
    elif stress_score >= 3:
        priority = "High"
    elif stress_score >= 1:
        priority = "Medium"
    else:
        priority = "Low"

    return stress_score, emotion, priority
