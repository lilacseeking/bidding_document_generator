from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class NodeBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)

class NodeCreate(NodeBase):
    pass

class NodeUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None

class Node(NodeBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RelationshipBase(BaseModel):
    source_id: str
    target_id: str
    type: str
    properties: Dict[str, Any] = Field(default_factory=dict)

class RelationshipCreate(RelationshipBase):
    pass

class RelationshipUpdate(BaseModel):
    type: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None

class Relationship(RelationshipBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Link(BaseModel):
    source: str
    target: str
    type: str

class KnowledgeGraph(BaseModel):
    nodes: List[Node]
    links: List[Link]

    class Config:
        orm_mode = True 