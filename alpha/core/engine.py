from pathlib import Path
import importlib
import inspect

from alpha.core.module import AlphaModule


class AlphaEngine:

    def __init__(
        self,
        config,
        database,
        logger
    ):
        self.config = config
        self.database = database
        self.logger = logger
        self.modules = []

        self.context = {
            "config": config,
            "database": database,
            "logger": logger,
        }

    def initialize(self):
        self.database.initialize()

        self.load_modules()

        for module in self.modules:
            try:
                module.initialize(
                    self.context
                )

            except Exception as error:
                self.logger.error(
                    "Module initialization failed: "
                    "%s: %s",
                    module.name,
                    error
                )

    def load_modules(self):
        modules_path = Path(
            self.config.get(
                "modules",
                "directory",
                default="alpha/modules"
            )
        )

        if not modules_path.exists():
            self.logger.warning(
                "Module directory does not exist: %s",
                modules_path
            )
            return

        for file in sorted(
            modules_path.glob("*.py")
        ):
            if file.name.startswith("_"):
                continue

            module_name = (
                f"alpha.modules.{file.stem}"
            )

            try:
                imported = importlib.import_module(
                    module_name
                )

                for _, obj in inspect.getmembers(
                    imported,
                    inspect.isclass
                ):
                    if (
                        issubclass(
                            obj,
                            AlphaModule
                        )
                        and obj is not AlphaModule
                    ):
                        instance = obj()

                        self.modules.append(
                            instance
                        )

                        self.database.register_module(
                            instance.module_id,
                            instance.name,
                            instance.version
                        )

                        self.logger.info(
                            "Loaded module: %s",
                            instance.name
                        )

            except Exception as error:
                self.logger.error(
                    "Failed to load module %s: %s",
                    module_name,
                    error
                )

    def scan(self):
        results = {}

        for module in self.modules:
            try:
                self.logger.info(
                    "Scanning module: %s",
                    module.name
                )

                result = module.scan(
                    self.context
                )

                analysis = module.analyze(
                    self.context,
                    result
                )

                results[
                    module.module_id
                ] = analysis

            except Exception as error:
                self.logger.error(
                    "Module scan failed: %s: %s",
                    module.name,
                    error
                )

                results[
                    module.module_id
                ] = {
                    "status": "error",
                    "error": str(error)
                }

        return results

    def shutdown(self):
        for module in self.modules:
            try:
                module.shutdown(
                    self.context
                )

            except Exception as error:
                self.logger.error(
                    "Module shutdown failed: "
                    "%s: %s",
                    module.name,
                    error
                )

        self.database.close()
