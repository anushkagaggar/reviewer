import json
from pathlib import Path
from datetime import datetime


class MemoryManager:
    def __init__(self):
        self.stm_path = Path("memory/stm.json")
        self.ltm_path = Path("memory/ltm.json")

        self.stm = self._load(self.stm_path)
        self.ltm = self._load(self.ltm_path)

    def _load(self, path):
        if not path.exists():
            return {}

        try:
            return json.loads(path.read_text())
        except Exception:
            return {}

    def _save(self, path, data):
        path.write_text(json.dumps(data, indent=2))

    def _key(self, system_name, version):
        return f"{system_name}::{version}"

    # -------- STM --------

    def get_stm(self, system_name, version):
        key = self._key(system_name, version)
        return self.stm.get(key, [])

    def update_stm(self, system_name, version, issues):
        key = self._key(system_name, version)

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "key_issues": issues
        }

        history = self.stm.get(key, [])
        history.append(record)

        # Keep last 5 only
        self.stm[key] = history[-5:]

        self._save(self.stm_path, self.stm)

    # -------- LTM --------

    def get_ltm(self, system_name, version):
        key = self._key(system_name, version)
        return self.ltm.get(key, {})

    def update_ltm(self, system_name, version, issues):
        key = self._key(system_name, version)

        entry = self.ltm.get(key, {
            "recurring_issues": [],
            "last_updated": None
        })

        for issue in issues:
            if issue not in entry["recurring_issues"]:
                entry["recurring_issues"].append(issue)

        entry["last_updated"] = datetime.utcnow().isoformat()

        self.ltm[key] = entry

        self._save(self.ltm_path, self.ltm)
