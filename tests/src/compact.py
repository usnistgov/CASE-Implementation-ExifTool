#!/usr/bin/env python3

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

"""
This script attempts to apply the PyLD "compact" call to the JSON-LD generated by rdf-toolkit.  The issue this script resolves is somewhat cosmetic: rdf-toolkit emits a top-level array of dictionaries, and creates a context dictionary for each dictionary that is a direct child of that array.

This script requires adherence to the JSON-LD requirement that terms not be empty strings.  This includes the blank context prefix permitted in Turtle, and permitted in JSON-LD by some parsers.
https://www.w3.org/TR/json-ld11/#terms
"""

__version__ = "0.1.2"

import json
import logging
import os

import pyld  # type: ignore

_logger = logging.getLogger(os.path.basename(__file__))


def main() -> None:
    with open(args.out_json, "w") as out_fh:
        doc = None
        with open(args.in_json, "r") as in_fh:
            doc = json.load(in_fh)
        assert doc is not None

        # Grab the first occurrence of every key.
        total_context = dict()
        for obj in doc:
            local_context = obj.get("@context")
            if local_context is None:
                continue
            for key in local_context.keys():
                if key not in total_context:
                    # Accrue new key.
                    total_context[key] = local_context[key]

        # Sort keys.
        total_context_keys = sorted(total_context.keys())
        _total_context = dict()
        for key in total_context_keys:
            _total_context[key] = total_context[key]
        total_context = _total_context

        _logger.debug("total_context = %r." % total_context)

        compacted = pyld.jsonld.compact(doc, total_context)

        # Add xsd prefix back in to context dictionary.  .compact() removes it, and this causes some xsd definitions like xsd:long to no longer resolve in SPARQL queries.
        compacted["@context"]["xsd"] = "http://www.w3.org/2001/XMLSchema#"

        out_fh.write(json.dumps(compacted, indent=4))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("in_json")
    parser.add_argument("out_json")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    main()
