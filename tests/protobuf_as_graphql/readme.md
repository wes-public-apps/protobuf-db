# Reproducilibity Rules
- PEP8 style
- imports, enums, map classes, nested classes, and then class for relevant protobuf
- map class name format is "Map<key type><value type>" (this can be used to find existing classes if present)

# Auto Generation Considerations
- all types found within an object should all be documented on the same file
- NOT PREFERRED: parse the proto files to keep structure (maybe object can give us the same data)