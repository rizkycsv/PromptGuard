def classify_tone(text):
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in ["apologize", "sorry", "cannot assist", "guidelines"]):
        return "refusal"
    elif any(keyword in text_lower for keyword in ["explain", "educate", "inform", "definition"]):
        return "instructive"
    elif any(keyword in text_lower for keyword in ["speculate", "imagine", "hypothetically"]):
        return "speculative"
    elif any(keyword in text_lower for keyword in ["legal", "financial", "medical"]):
        return "formal"
    return "neutral"

def check_tone_drift(expected, model_output):
    regressions = []
    
    if "tone" in expected:
        expected_tones = expected["tone"]
        if not isinstance(expected_tones, list):
            expected_tones = [expected_tones] # Make it a list for consistent handling

        actual_tone = classify_tone(model_output)
        
        if actual_tone not in expected_tones:
            regressions.append({
                "type": "tone_drift",
                "reason": f"Expected tone(s) {expected_tones} but got '{actual_tone}'.",
                "severity": "medium"
            })
            
    return regressions
