from alpha.core.module import AlphaModule


class SystemModule(AlphaModule):

    module_id = "system"

    name = "System"

    version = "0.1.0"

    def initialize(self, context):
        context["logger"].info(
            "System module initialized"
        )

    def scan(self, context):
        return {
            "status": "ok",
            "message": "System module is working"
        }

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
