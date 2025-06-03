from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.config import settings
from neo4j import GraphDatabase
import uuid
from datetime import datetime

# Neo4j connection
driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

def get_node(db: Session, node_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a node by ID.
    """
    with driver.session() as session:
        result = session.run("""
            MATCH (n {id: $node_id})
            RETURN n
        """, node_id=node_id)
        node = result.single()
        return dict(node["n"]) if node else None

def get_nodes(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get multiple nodes.
    """
    with driver.session() as session:
        result = session.run("""
            MATCH (n)
            RETURN n
            SKIP $skip
            LIMIT $limit
        """, skip=skip, limit=limit)
        return [dict(record["n"]) for record in result]

def create_node(
    db: Session,
    *,
    obj_in: schemas.NodeCreate
) -> Dict[str, Any]:
    """
    Create a new node.
    """
    node_id = str(uuid.uuid4())
    now = datetime.utcnow()
    properties = {
        **obj_in.dict(),
        "id": node_id,
        "created_at": now,
        "updated_at": now
    }
    
    with driver.session() as session:
        result = session.run("""
            CREATE (n:Node $properties)
            RETURN n
        """, properties=properties)
        return dict(result.single()["n"])

def update_node(
    db: Session,
    *,
    node_id: str,
    obj_in: schemas.NodeUpdate
) -> Optional[Dict[str, Any]]:
    """
    Update a node.
    """
    update_data = obj_in.dict(exclude_unset=True)
    if not update_data:
        return get_node(db, node_id)
    
    update_data["updated_at"] = datetime.utcnow()
    
    with driver.session() as session:
        result = session.run("""
            MATCH (n {id: $node_id})
            SET n += $properties
            RETURN n
        """, node_id=node_id, properties=update_data)
        node = result.single()
        return dict(node["n"]) if node else None

def delete_node(
    db: Session,
    *,
    node_id: str
) -> bool:
    """
    Delete a node.
    """
    with driver.session() as session:
        result = session.run("""
            MATCH (n {id: $node_id})
            DETACH DELETE n
            RETURN count(n) as deleted
        """, node_id=node_id)
        return result.single()["deleted"] > 0

def get_relationship(
    db: Session,
    relationship_id: str
) -> Optional[Dict[str, Any]]:
    """
    Get a relationship by ID.
    """
    with driver.session() as session:
        result = session.run("""
            MATCH ()-[r {id: $relationship_id}]->()
            RETURN r
        """, relationship_id=relationship_id)
        rel = result.single()
        return dict(rel["r"]) if rel else None

def create_relationship(
    db: Session,
    *,
    obj_in: schemas.RelationshipCreate
) -> Dict[str, Any]:
    """
    Create a new relationship.
    """
    relationship_id = str(uuid.uuid4())
    now = datetime.utcnow()
    properties = {
        **obj_in.dict(),
        "id": relationship_id,
        "created_at": now,
        "updated_at": now
    }
    
    with driver.session() as session:
        result = session.run("""
            MATCH (a {id: $source_id}), (b {id: $target_id})
            CREATE (a)-[r:$type $properties]->(b)
            RETURN r
        """, 
        source_id=obj_in.source_id,
        target_id=obj_in.target_id,
        type=obj_in.type,
        properties=properties)
        return dict(result.single()["r"])

def update_relationship(
    db: Session,
    *,
    relationship_id: str,
    obj_in: schemas.RelationshipUpdate
) -> Optional[Dict[str, Any]]:
    """
    Update a relationship.
    """
    update_data = obj_in.dict(exclude_unset=True)
    if not update_data:
        return get_relationship(db, relationship_id)
    
    update_data["updated_at"] = datetime.utcnow()
    
    with driver.session() as session:
        result = session.run("""
            MATCH ()-[r {id: $relationship_id}]->()
            SET r += $properties
            RETURN r
        """, relationship_id=relationship_id, properties=update_data)
        rel = result.single()
        return dict(rel["r"]) if rel else None

def delete_relationship(
    db: Session,
    *,
    relationship_id: str
) -> bool:
    """
    Delete a relationship.
    """
    with driver.session() as session:
        result = session.run("""
            MATCH ()-[r {id: $relationship_id}]->()
            DELETE r
            RETURN count(r) as deleted
        """, relationship_id=relationship_id)
        return result.single()["deleted"] > 0

def search_nodes(
    db: Session,
    *,
    query: str,
    skip: int = 0,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Search for nodes by name or properties.
    """
    with driver.session() as session:
        result = session.run("""
            MATCH (n)
            WHERE n.name CONTAINS $query
            OR ANY(prop in keys(n) WHERE toString(n[prop]) CONTAINS $query)
            RETURN n
            SKIP $skip
            LIMIT $limit
        """, query=query, skip=skip, limit=limit)
        return [dict(record["n"]) for record in result]

def get_node_types(db: Session) -> List[str]:
    """
    Get all available node types.
    """
    with driver.session() as session:
        result = session.run("""
            MATCH (n)
            RETURN DISTINCT labels(n) as types
        """)
        types = []
        for record in result:
            types.extend(record["types"])
        return list(set(types))

def get_relationship_types(db: Session) -> List[str]:
    """
    Get all available relationship types.
    """
    with driver.session() as session:
        result = session.run("""
            MATCH ()-[r]->()
            RETURN DISTINCT type(r) as types
        """)
        return [record["types"] for record in result] 