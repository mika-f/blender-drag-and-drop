import traceback
import sys

from pathlib import Path

dir = Path(__file__).parent / "includes"
sys.path.append(str(dir))


def launch():
    from libs.server import setup

    setup()


try:
    launch()
except Exception as e:
    traceback.print_exc()
    sys.exit()
