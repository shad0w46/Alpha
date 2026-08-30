from abc import ABC, abstractmethod


class AlphaModule(ABC):

    @property
    @abstractmethod
    def module_id(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def version(self):
        pass

    def initialize(self, context):
        pass

    @abstractmethod
    def scan(self, context):
        pass

    def analyze(
        self,
        context,
        scan_result
    ):
        return scan_result

    def actions(
        self,
        context,
        analysis
    ):
        return []

    def shutdown(self, context):
        pass
