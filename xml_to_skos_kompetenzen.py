from lxml import etree as ET
from rdflib import Graph, Literal, Namespace, RDF, URIRef, BNode
from rdflib.namespace import SKOS, DCTERMS
from pathlib import Path
import re
import uuid
import os
from xml_to_skos import parseXML, sortData, addToNode, buildSkos, writeGraph, writeLog


log = []

tree = ET.parse("data/rlp-bb-edited.xml")

# remove <themainhalt>
for themainhalt in tree.xpath("//themainhalt"):
    themainhalt.getparent().remove(themainhalt)

xmlRoot = tree.getroot()
parsedXML, logging = parseXML(xmlRoot, tree)
log.extend(logging)

data, logging = sortData(parsedXML)
log.extend(logging)

nodes = addToNode(data)
serialized_graph = buildSkos(
    nodes,
    name_of_graph="RLP Berlin-Brandenburg Kompetenzen",
    base_url="http://opencurricula/berlin-brandenburg/competences/"
)

# create data dir if not there
Path(Path.cwd() / "data").mkdir(exist_ok=True)

# write graph
graphname = (Path.cwd() / "data" / "curriculum_bb_competences_skos.ttl")
writeGraph(graphname, serialized_graph)

# write error log
print(log)
log_filename = (Path.cwd() / "log-competences.txt")
writeLog(log_filename, log)


print("I'm done. Goodbye!")

