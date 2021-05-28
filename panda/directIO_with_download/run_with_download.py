#!/usr/bin/env python

import io
import requests
import sys
import time
import uproot
import json
import math
import awkward as ak

from physlite_experiments.physlite_events import (
    physlite_events, get_lazy_form, get_branch_forms, Factory, LazyGet, from_parquet
)
from physlite_experiments.analysis_example import get_obj_sel
from physlite_experiments.utils import subdivide

def run(file_like, max_chunksize=50000):
    output = {
        collection: {
            flag : 0
            for flag in ["baseline", "passOR", "signal"]
        } for collection in ["Electrons", "Muons", "Jets"]
    }
    nevents = 0
    print("Processing data in memory")
    start = time.time()
    with uproot.open(file_like) as f:
        tree = f["CollectionTree"]
        if max_chunksize is not None and tree.num_entries > max_chunksize:
            n_chunks = math.ceil(tree.num_entries / max_chunksize)
        else:
            n_chunks = 1
        form = json.dumps(get_lazy_form(get_branch_forms(tree)))
        entry_start = 0
        for num_entries in subdivide(tree.num_entries, n_chunks):
            print("Processing", num_entries, "entries")
            entry_stop = entry_start + num_entries
            cache = {}
            container = LazyGet(
                tree, entry_start=entry_start, entry_stop=entry_stop,
                cache=cache
            )
            factory = Factory(form, entry_stop - entry_start, container)
            events = factory.events
            events_decorated = get_obj_sel(events)
            entry_start = entry_stop
            for collection in output:
                for flag in output[collection]:
                    output[collection][flag] += ak.count_nonzero(
                        events_decorated[collection][flag]
                    )
            nevents += len(events)
    print(f"Took {time.time() - start:.2f} seconds")
    return output, nevents


if __name__ == "__main__":

    from requests_futures.sessions import FuturesSession

    session = FuturesSession(max_workers=1)
    futures = {}

    input_files = sys.argv[1].replace(r"&amp;", r"&").split(",")

    # put first file in queue
    print(f"Put {input_files[0]} in download queue")
    futures[input_files[0]] = session.get(input_files[0])
    for i, url in enumerate(input_files):
        if i < (len(input_files) - 1):
            # put next file in queue
            print(f"Put {input_files[i + 1]} in download queue")
            futures[input_files[i + 1]] = session.get(input_files[i + 1])
        print("Waiting for Download")
        start = time.time()
        file_like = io.BytesIO(futures.pop(url).result().content)
        print(f"Had to wait {time.time() - start:.2f} seconds")
        print(run(file_like))
