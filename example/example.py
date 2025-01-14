# Colab: https://colab.research.google.com/drive/1YpDetI8BRbObPDEVdfqUcwhEX9UUXP-m?usp=sharing
import os
from pathlib import Path

from haystack.preview import Pipeline
from haystack.preview.components.file_converters import TextFileToDocument
from haystack.preview.components.writers import DocumentWriter

from chroma_haystack import ChromaDocumentStore
from chroma_haystack.retriever import ChromaDenseRetriever

HERE = Path(__file__).resolve().parent
file_paths = [HERE / "data" / Path(name) for name in os.listdir("data")]

# Chroma is used in-memory so we use the same instances in the two pipelines below
document_store = ChromaDocumentStore()

indexing = Pipeline()
indexing.add_component("converter", TextFileToDocument())
indexing.add_component("writer", DocumentWriter(document_store))
indexing.connect("converter", "writer")
indexing.run({"converter": {"paths": file_paths}})

querying = Pipeline()
querying.add_component("retriever", ChromaDenseRetriever(document_store))
results = querying.run({"retriever": {"queries": ["Variable declarations"], "top_k": 3}})

for d in results["retriever"][0]:
    print(d.metadata, d.score)
