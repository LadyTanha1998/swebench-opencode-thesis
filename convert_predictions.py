#!/usr/bin/env python3
"""Convert predictions from our JSONL format to SWE-bench Pro JSON format."""

import json
import sys
from pathlib import Path


def convert_predictions(input_path: str, output_path: str):
    """Convert predictions from JSONL to JSON array format."""
    
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    if not input_file.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    predictions = []
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON line: {e}")
                continue
            
            # Extract fields
            instance_id = entry.get("instance_id", "")
            model_patch = entry.get("model_patch", "")
            model_name = entry.get("model_name_or_path", "")
            
            # Skip empty patches
            if not model_patch.strip():
                print(f"Warning: Skipping empty patch for {instance_id}")
                continue
            
            # Convert to SWE-bench Pro format
            # Using model_name as prefix (e.g., "opencode-mimo-v2.5-free-run1")
            converted_entry = {
                "instance_id": instance_id,
                "patch": model_patch,
                "prefix": model_name
            }
            
            predictions.append(converted_entry)
    
    # Write as JSON array
    with open(output_file, 'w') as f:
        json.dump(predictions, f, indent=2)
    
    print(f"Converted {len(predictions)} predictions")
    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_predictions.py <input.jsonl> <output.json>")
        print("Example: python convert_predictions.py outputs/predictions_all.jsonl outputs/predictions_swebench_pro.json")
        sys.exit(1)
    
    convert_predictions(sys.argv[1], sys.argv[2])
