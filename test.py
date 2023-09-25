import gc
import sys
from collections import UserDict

from lib import get_spam


def test_leak() -> None:
    d = UserDict()  # type: ignore
    try:
        get_spam(d)
    except KeyError as e:
        tb = e.__traceback__
        # pylint: disable-next=no-member
        while tb is not None and tb.tb_frame.f_code.co_filename != "lib.pyx":
            tb = tb.tb_next
        assert tb is not None
        # get the next traceback object after the Cython code
        tb = tb.tb_next
    # subtract one for the temporary argument reference
    refcount = sys.getrefcount(tb) - 1
    # add one since get_referrers() doesn't include the locals dict
    num_referrers = len(gc.get_referrers(tb)) + 1
    assert refcount <= num_referrers, "traceback was leaked"
