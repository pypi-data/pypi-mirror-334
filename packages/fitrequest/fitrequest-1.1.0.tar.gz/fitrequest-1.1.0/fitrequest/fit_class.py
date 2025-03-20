from pathlib import Path

import yaml

from fitrequest.fit_config import FitConfig


class FitClass:
    @staticmethod
    def from_json(json_path: Path | str) -> type:
        """Generate a ``fitrequest`` class from a ``json`` file."""
        with open(str(json_path), encoding='utf-8') as json_file:
            return FitConfig.model_validate_json(json_file.read()).fit_class

    @staticmethod
    def from_yaml(yaml_path: Path | str) -> type:
        """Generate a ``fitrequest`` class from a ``yaml`` file."""
        with open(str(yaml_path), encoding='utf-8') as yaml_file:
            return FitConfig.model_validate(yaml.safe_load(yaml_file)).fit_class

    @staticmethod
    def from_dict(**kwargs) -> type:
        """Generate a ``fitrequest`` class from a keyword arguments."""
        return FitConfig(**kwargs).fit_class
