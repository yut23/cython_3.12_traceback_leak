import sys
from collections import UserDict

# pylint: disable-next=import-error, no-name-in-module, useless-suppression
from lib import get_spam


def main() -> None:
    d = UserDict()  # type: ignore
    d["lots of data"] = bytearray(1024**2)
    try:
        get_spam(d)
    except KeyError:
        pass


if len(sys.argv) > 1:
    num_iters = int(sys.argv[1])
else:
    num_iters = 10

for i in range(num_iters):
    main()
    print(f"{i+1}/{num_iters}\r", end="")
print()
