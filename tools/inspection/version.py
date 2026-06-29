from __future__ import annotations

BLE_VERSION = "1.0.0"
WORKBENCH_VERSION = "1.0.0"


def version_string() -> str:
    return f"BLE {BLE_VERSION} | Workbench {WORKBENCH_VERSION}"
