import psutil


class ProcessMonitor:

    @staticmethod
    def get_system_info():
        memory = psutil.virtual_memory()

        return {
            "cpu": psutil.cpu_percent(interval=None),
            "memory_percent": memory.percent,
            "memory_used": memory.used,
            "memory_total": memory.total,
            "load": psutil.getloadavg(),
        }

    @staticmethod
    def get_top_cpu(limit=5):
        processes = []

        for process in psutil.process_iter(
            ["pid", "name", "cpu_percent"]
        ):
            try:
                info = process.info

                processes.append({
                    "pid": info["pid"],
                    "name": info["name"] or "Unknown",
                    "cpu": info["cpu_percent"] or 0.0,
                })

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

        processes.sort(
            key=lambda item: item["cpu"],
            reverse=True,
        )

        return processes[:limit]

    @staticmethod
    def get_top_memory(limit=5):
        processes = []

        for process in psutil.process_iter(
            ["pid", "name", "memory_percent", "memory_info"]
        ):
            try:
                info = process.info

                memory_info = info["memory_info"]

                processes.append({
                    "pid": info["pid"],
                    "name": info["name"] or "Unknown",
                    "memory_percent": (
                        info["memory_percent"] or 0.0
                    ),
                    "memory": (
                        memory_info.rss
                        if memory_info
                        else 0
                    ),
                })

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

        processes.sort(
            key=lambda item: item["memory"],
            reverse=True,
        )

        return processes[:limit]
