from .tools import plot
from .utils import notify

notify.extend_finlab()
plot.extend_finlab()

__version__ = "0.1.2.dev1"

def main() -> None:
    print("Hello from fxe!")
