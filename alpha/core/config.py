from pathlib import Path
import yaml


class Config:

    def __init__(self, path="config.yaml"):

        self.path = Path(path)

        self.data = self._load()

    def _load(self):

        if not self.path.exists():

            return {}

        with self.path.open(
            "r",
            encoding="utf-8"
        ) as file:

            data = yaml.safe_load(file)

        if not isinstance(data, dict):

            return {}

        return data

    def get(
        self,
        key,
        default=None
    ):

        current = self.data

        for part in key.split("."):

            if not isinstance(
                current,
                dict
            ):

                return default

            if part not in current:

                return default

            current = current[part]

        return current
