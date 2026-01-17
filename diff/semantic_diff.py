def check_semantic_drift(expected, model_output):
    regressions = []
    
    if "keywords" in expected:
        for keyword in expected["keywords"]:
            if keyword.lower() not in model_output.lower():
                regressions.append({
                    "type": "semantic_drift",
                    "reason": f"Expected keyword '{keyword}' not found in output.",
                    "severity": "medium"
                })
    
    # Placeholder for more advanced semantic comparison (e.g., embedding similarity)
    # This would require an embedding model and a threshold.
    # if "reference_embedding" in expected and "model_output_embedding" in model_output:
    #     similarity = calculate_cosine_similarity(expected["reference_embedding"], model_output["model_output_embedding"])
    #     if similarity < expected["semantic_threshold"]:
    #         regressions.append({
    #             "type": "semantic_drift",
    #             "reason": "Semantic similarity below threshold.",
    #             "severity": "high"
    #         })

    return regressions
