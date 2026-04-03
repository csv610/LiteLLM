import json
import time
import os
from pathlib import Path
from typing import Union, Optional, Any


def save_result(
    data: Any,
    output_filename: Optional[str] = None,
    input_filename: Optional[str] = None,
    output_dir: str = "outputs",
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    if output_filename is None:
        if input_filename:
            base_name = Path(input_filename).stem
            output_filename = f"{base_name}_output"
        else:
            output_filename = f"output_{int(time.time())}"

    if output_filename.endswith((".json", ".md")):
        output_filename = Path(output_filename).stem

    json_path = os.path.join(output_dir, f"{output_filename}.json")

    data_to_save = data.model_dump() if hasattr(data, "model_dump") else data
    if isinstance(data, dict) and "markdown" in data and "data" in data:
        md_path = os.path.join(output_dir, f"{output_filename}.md")
        if data["markdown"]:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(data["markdown"])
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return md_path if data["markdown"] else json_path

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, indent=4)
    return json_path


def print_result(data: Any) -> None:
    print(f"\n{'=' * 80}")
    print("RESULT REPORT")
    print(f"{'=' * 80}\n")
    if hasattr(data, "markdown") and data.markdown:
        print(data.markdown)
    else:
        print(
            json.dumps(
                data.model_dump() if hasattr(data, "model_dump") else data, indent=2
            )
        )
    print(f"\n{'=' * 80}\n")
