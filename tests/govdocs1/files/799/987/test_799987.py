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

import rdflib.plugins.sparql

graph = rdflib.Graph()
graph.parse("analysis.json", format="json-ld")

nsdict = {k: v for (k, v) in graph.namespace_manager.namespaces()}


def test_confirm_location_generated() -> None:
    query = rdflib.plugins.sparql.processor.prepareQuery(
        """\
SELECT ?nLocation
WHERE {
  ?nLocation
    a uco-location:Location
}""",
        initNs=nsdict,
    )
    iris = set()
    for result in graph.query(query):
        assert isinstance(result, rdflib.query.ResultRow)
        assert isinstance(result[0], rdflib.term.IdentifiedNode)
        iris.add(result[0].toPython())
    assert len(iris) == 1
