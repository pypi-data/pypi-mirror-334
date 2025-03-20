from . import roll
from . import roll_pass

VERSION ="3.0.0.post2"

import importlib.util

REPORT_INSTALLED = bool(importlib.util.find_spec("pyroll.report"))

if REPORT_INSTALLED:
    from . import report
    import pyroll.report

    pyroll.report.plugin_manager.register(report)

