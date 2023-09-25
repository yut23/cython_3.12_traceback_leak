# pylint: disable=import-error, useless-suppression
import gc
import sys
import traceback
from collections import UserDict
from typing import Any

import psutil

# pylint: disable-next=import-error, no-name-in-module, useless-suppression
from lib import get_spam

# import random
# import types
# import objgraph


if len(sys.argv) > 1:
    num_iters = int(sys.argv[1])
else:
    num_iters = 10


def main() -> None:
    d = UserDict()  # type: ignore
    d["lots of data"] = bytearray(1024**2)
    try:
        get_spam(d)
    except KeyError as e:
        tb = e.__traceback__
        # pylint: disable-next=no-member
        while tb is not None and tb.tb_frame.f_code.co_filename != "lib.pyx":
            tb = tb.tb_next
        if tb is not None and tb.tb_next is not None:
            print(tb.tb_next)
        # traceback.print_exception(e)


def collect() -> None:
    gc.collect()
    sys._clear_type_cache()  # pylint: disable=protected-access

# traceback.print_exception() adds a bunch of false positives, so run
# format_exc() beforehand to include them in initial_ids
try:
    raise KeyError
except KeyError:
    traceback.format_exc()

# pre-initialize these objects so they all get included in initial_ids
# counts_by_type = Counter()
objects = []
unreachable_garbage: list[Any] = []
initial_ids: set[int] = set()
initial_obj_count = 0
initial_block_count = 0
initial_vms = 0
process = psutil.Process()

collect()
initial_ids.update(map(id, gc.get_objects()))
initial_obj_count = len(gc.get_objects())
initial_block_count = sys.getallocatedblocks()
initial_vms = process.memory_info().vms
print(
    "initial: {:7d} objects, {:7d} blocks, {:6.2f}MiB VMS".format(
        initial_obj_count, initial_block_count, initial_vms / 1024**2
    )
)
for i in range(num_iters):
    main()
    collect()
    print(
        "iter {:2d}: {:+7d} objects, {:+7d} blocks, {:+6.2f}MiB VMS".format(
            i + 1,
            len(gc.get_objects()) - initial_obj_count,
            sys.getallocatedblocks() - initial_block_count,
            (process.memory_info().vms - initial_vms) / 1024**2,
        )
    )

# sys.exit(0)
print()
collect()
gc.disable()
count = 0
objects.extend(gc.get_objects())
for obj in objects:
    if id(obj) in initial_ids:
        continue
    refcount = sys.getrefcount(obj) - 1
    num_referrers = len(gc.get_referrers(obj))
    if refcount > num_referrers:
        count += 1
        # counts_by_type[str(type(obj))] += 1
        print(
            f"{len(unreachable_garbage)}: {object.__repr__(obj)}\t{obj!r} | {refcount} > {num_referrers}"
        )
        # if isinstance(obj, types.TracebackType):
        #     if not traceback_ids:
        #         objgraph.show_refs([obj], refcounts=True)
        #         objgraph.show_backrefs([obj], refcounts=True)
        #     traceback.print_tb(obj)
        unreachable_garbage.append(obj)
    del obj
# print()
# print(len(objects))
# print(count)
# for k, v in counts_by_type.most_common():
#     print(f"{k}: {v}")
# print(
#     "before gc: {:+7d} objects, {:+7d} blocks, {:+6.2f}MiB VMS".format(
#         len(gc.get_objects()) - initial_obj_count,
#         sys.getallocatedblocks() - initial_block_count,
#         (process.memory_info().vms - initial_vms) / 1024**2,
#     )
# )
del objects
gc.enable()
collect()
# print(
#     "after gc:  {:+7d} objects, {:+7d} blocks, {:+6.2f}MiB VMS".format(
#         len(gc.get_objects()) - initial_obj_count,
#         sys.getallocatedblocks() - initial_block_count,
#         (process.memory_info().vms - initial_vms) / 1024**2,
#     )
# )

# roots = objgraph.get_leaking_objects()
# print(len(roots))
# objgraph.show_most_common_types(objects=roots, limit=None)

# objgraph.show_chain(
#     objgraph.find_backref_chain(
#         random.choice(objgraph.by_type("MyBigObject")), objgraph.is_proper_module
#     ),
#     refcounts=True,
# )
