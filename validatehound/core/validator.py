# core/validator.py
"""
Validatore base per RustHound-CE outputs.
Applica modelli Pydantic definiti in core.schemas.
"""
from typing import Dict, Any, List, Tuple
from pydantic import ValidationError
from . import schemas


class ValidationResult:
    def __init__(self, filename: str):
        self.filename = filename
        self.valid_count = 0
        self.invalid_count = 0
        self.errors: List[str] = []

    def add_error(self, msg: str):
        self.invalid_count += 1
        self.errors.append(msg)

    def add_valid(self):
        self.valid_count += 1

    def summary(self) -> str:
        return f"{self.filename}: {self.valid_count} valid, {self.invalid_count} invalid"


def validate_data(data: Dict[str, Any]) -> Dict[str, ValidationResult]:
    """
    Esegue validazione di base su ogni file JSON presente nel dict `data`
    restituito da core.loader.load().
    """
    results: Dict[str, ValidationResult] = {}
    for filename, content in data.items():
        res = ValidationResult(filename)
        model_cls = None
        for key in schemas.SCHEMA_MAP:
            if filename.lower().endswith(key):
                model_cls = schemas.SCHEMA_MAP[key]
                break
        
        if model_cls is None:
            # file non riconosciuto, skip
            results[filename] = res
            continue

        if not isinstance(content, list):
            res.add_error("Expected a list of objects")
            results[filename] = res
            continue

        for idx, item in enumerate(content):
            try:
                model_cls.parse_obj(item)
                res.add_valid()
            except ValidationError as e:
                res.add_error(f"Item {idx}: {e.errors()}")
        results[filename] = res
    return results
