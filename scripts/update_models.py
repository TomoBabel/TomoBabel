#!/usr/bin/env python3
from linkml.generators.pydanticgen import PydanticGenerator
from black import format_file_in_place, WriteBack, FileMode
from pathlib import Path

schema_path = Path("data_model/entities.yaml")
output_path = Path("tomobabel/models/models.py")

# Generate the models
output_code = PydanticGenerator(schema_path, metadata_mode=None).serialize()

# Read existing model
with open("tomobabel/models/models.py") as existing:
    current = existing.read()

# check for changes and rewrite if necessary:
if current != output_code:
    print("🔄 Updating Pydantic models...")
    with open(output_path, "w") as f:
        f.write("# type: ignore\n" + output_code)

# Format with Black (in place)
print("🎨 Formatting with black (in place)...")
format_file_in_place(output_path, fast=False, mode=FileMode(), write_back=WriteBack.YES)

print("✅ Done.")
