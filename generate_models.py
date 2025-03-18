#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "datamodel-code-generator[debug]>=0.28.2",
# ]
# ///

JSONIX_EXECUTABLE  = "~/Downloads/jsonix-schema-compiler-full.jar"



converter_command = """
export PATH="/usr/lib/jvm/java-8-openjdk/jre/bin/:$PATH"
exec java -jar ~/Downloads/jsonix-schema-compiler-full.jar -generateJsonSchema -p PO ./schema.xsd
"""


codegen_command = "datamodel-codegen --input PO.jsonschema --input-file-type jsonschema --output model.py --help"


