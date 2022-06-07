import traceback
import sys

from pathlib import Path

dir = Path(__file__).parent / "includes"
sys.path.append(str(dir))


def launch():
    from libs.server import setup
    from libs.installation import check_module_installed

    for mod in ["flask"]:
        let = check_module_installed(mod)

    if not let:
        print("failed to import flask")
        return

    setup()


try:
    launch()
except Exception as e:
    traceback.print_exc()
    sys.exit()
