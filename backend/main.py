from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import networkx as nx

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class Node(BaseModel):
    id: str
    type: str

class Edge(BaseModel):
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class PipelineResponse(BaseModel):
    num_nodes: int
    num_edges: int
    is_dag: bool

@app.get('/')
def read_root():
    return {'status': 'Pipeline API is running'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: Pipeline) -> PipelineResponse:
    """
    Parse and validate a pipeline.
    
    Returns:
    - num_nodes: Number of nodes in the pipeline
    - num_edges: Number of edges in the pipeline
    - is_dag: Whether the pipeline forms a DAG (no cycles)
    """
    # Count nodes and edges
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)
    
    # Create a directed graph for cycle detection
    G = nx.DiGraph()
    
    # Add nodes to graph
    for node in pipeline.nodes:
        G.add_node(node.id)
    
    # Add edges to graph
    for edge in pipeline.edges:
        G.add_edge(edge.source, edge.target)
    
    # Check if the graph is a DAG (has cycles if not DAG)
    is_dag = nx.is_directed_acyclic_graph(G)
    
    return PipelineResponse(
        num_nodes=num_nodes,
        num_edges=num_edges,
        is_dag=is_dag
    )
