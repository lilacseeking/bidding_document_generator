from neo4j import GraphDatabase
import pandas as pd


class KnowledgeGraphConstruction:
    def __init__(self, uri, user, password):
        self.driver =  GraphDatabase.driver(uri, auth=(user, password))

    def create_node(self, label, properties):
        with self.driver.session() as session:
            session.run(f"CREATE (n:{label} $props)", props=properties)

    def create_relationship(self, start_label: str, start_id: int,
                            rel_type: str, end_label: str, end_id: int):
        """创建关系方法（支持中文关系类型）"""
        # 使用f-string直接插入关系类型名称
        cypher = f"""
        MATCH (a:{start_label} {{id: $start_id}}), 
              (b:{end_label} {{id: $end_id}})
        MERGE (a)-[:`{rel_type}`]->(b)
        """
        # 注意：反引号`用于处理特殊字符

        parameters = {
            "start_id": start_id,
            "end_id": end_id
        }
        with self.driver.session() as session:
            session.run(cypher, parameters)

    def build_graph(self):
        laws_df = pd.read_csv('../data/laws.csv')
        standards_df = pd.read_csv('../data/standards.csv')
        project_cases_df = pd.read_csv('../data/project_cases.csv')
        suppliers_df = pd.read_csv('../data/suppliers.csv')
        experts_df = pd.read_csv('../data/experts.csv')

        # 创建招标项目节点
        for index, row in project_cases_df.iterrows():
            self.create_node("招标项目", {"id": row["project_id"], "name": row["project_name"]})

        # 创建投标方节点
        for index, row in suppliers_df.iterrows():
            self.create_node("投标方", {"id": row["supplier_id"], "name": row["supplier_name"]})

        # 创建招标项目与投标方的参与关系
        for index, row in project_cases_df.iterrows():
            self.create_relationship("招标项目", row["project_id"], "参与", "投标方", row["bidder_id"])

    def query_graph(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]