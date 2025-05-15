import erdantic as erd
import copy
from pathlib import Path
from tomobabel.models.top_level import DataSet

docs = Path(__file__).parents[1].absolute() / "docs/files/models_diagram.png"

# Remove the annotation fields because they make the graph too spider-webby
remove_classes = ["Annotation", "AnnotationSet"]
remove_fields = ["annotations"]

diagram = erd.create(DataSet)

mod_copy = copy.deepcopy(diagram.models)
for i in diagram.models:
    if diagram.models[i].full_name.qual_name in remove_classes:
        del mod_copy[i]

diagram.models = mod_copy

edge_copy = copy.deepcopy(diagram.edges)
for i in diagram.edges:
    if (
        any([x in i for x in remove_classes])
        or diagram.edges[i].source_field_name in remove_fields
    ):
        del edge_copy[i]
diagram.edges = edge_copy
diagram.draw(out=docs, graph_attr={"ranksep": 1.0})
