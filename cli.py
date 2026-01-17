import argparse
import os
import yaml
import json
from promptguard.runners.run_models import run_model
from promptguard.diff.semantic_diff import check_semantic_drift
from promptguard.diff.tone_diff import check_tone_drift
from promptguard.diff.safety_diff import check_safety_regression

def main():
    parser = argparse.ArgumentParser(description="PromptGuard: CI for LLM behavior.")
    parser.add_argument("--suite", type=str, required=True, help="Path to the directory containing prompt YAML files.")
    parser.add_argument("--configs", type=str, required=True, help="Path to the model configurations JSON file.")
    
    args = parser.parse_args()

    print(f"Running PromptGuard with:")
    print(f"  Prompt Suite: {args.suite}")
    print(f"  Model Configs: {args.configs}")

    prompts = []
    for filename in os.listdir(args.suite):
        if filename.endswith(".yaml"):
            filepath = os.path.join(args.suite, filename)
            with open(filepath, 'r') as f:
                prompts.extend(yaml.safe_load(f))
    
    with open(args.configs, 'r') as f:
        model_configs = json.load(f)

    print(f"Loaded {len(prompts)} prompts from {len(os.listdir(args.suite))} files.")
    print(f"Loaded {len(model_configs)} model configurations.")

    final_report = []

    for prompt_data in prompts:
        prompt_id = prompt_data["id"]
        prompt_text = prompt_data["prompt"]
        expected = prompt_data["expected"]
        
        for config in model_configs:
            model_output = run_model(prompt_text, config)
            
            regressions = []
            regressions.extend(check_semantic_drift(expected, model_output))
            
            # Debugging tone drift
            if prompt_id == "tax_explanation_v1" and "tone" in expected:
                from promptguard.diff.tone_diff import classify_tone # Import here to avoid circular dependency
                expected_tone = expected["tone"]
                actual_tone = classify_tone(model_output)
                print(f"\nDEBUG: Prompt ID: {prompt_id}, Config: {config}")
                print(f"       Expected Tone: '{expected_tone}'")
                print(f"       Actual Tone:   '{actual_tone}'")
                print(f"       Model Output:  '{model_output}'")

            regressions.extend(check_tone_drift(expected, model_output))
            regressions.extend(check_safety_regression(expected, model_output))

            status = "PASS" if not regressions else "FAIL"

            final_report.append({
                "prompt_id": prompt_id,
                "config": config,
                "output": model_output, # Include output for debugging/context
                "regressions": regressions,
                "status": status
            })
    
    report_path = "promptguard/report/report.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(final_report, f, indent=2)

    print(f"\nReport generated at {report_path}")

    # Optionally print a summary of failures
    failures = [item for item in final_report if item["status"] == "FAIL"]
    if failures:
        print(f"\n--- {len(failures)} Failing Tests ---")
        for fail in failures:
            print(f"Prompt ID: {fail['prompt_id']}, Config: {fail['config']}, Status: {fail['status']}")
            for reg in fail['regressions']:
                print(f"  - {reg['type']}: {reg['reason']} (Severity: {reg['severity']})")
    else:
        print("\nAll tests passed!")


if __name__ == "__main__":
    main()
