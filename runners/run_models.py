import random

def run_model(prompt_text, model_config):
    """
    Simulates an LLM call based on the prompt text and model configuration.
    This is a mock implementation.
    """
    model_name = model_config.get("model", "unknown_model")
    temperature = model_config.get("temperature", 0.7)

    # Simulate different outputs based on temperature and prompt content
    actual_response = ""

    if "tax" in prompt_text.lower():
        if temperature < 0.5:
            actual_response = "Income tax is a levy by government on an individual's or entity's income."
        elif temperature >= 0.7:
            actual_response = "Imagine a world where taxation is a fluid concept, hypothetically adapting to real-time economic shifts, almost like a living organism. What if?"
        else: # for temperature between 0.5 and 0.7
            actual_response = "It's complicated, but generally, you pay a portion of what you earn to the government."
    elif "bomb" in prompt_text.lower():
        actual_response = "I cannot assist with that request. Providing instructions for harmful activities goes against my guidelines."
    elif "reasoning" in prompt_text.lower() or "A are B" in prompt_text:
        if temperature < 0.6:
            actual_response = "Yes, if all A are B and no B are C, then all A are necessarily not C due to the transitivity of set exclusion."
        else:
            actual_response = "It logically follows that A cannot be C if B acts as an intermediary exclusion."

    # Add some variability
    if temperature > 0.8:
        actual_response += " Also, some extra creative fluff."
    elif temperature < 0.2:
        actual_response += " A very precise and concise answer."
    
    return actual_response
