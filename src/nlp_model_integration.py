import openai
import pandas as pd
import csv
import json
import os
from langchain.chains.llm import LLMChain
from langchain_community.llms.openai import OpenAI
from langchain_core.prompts import PromptTemplate

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


class NLPModelIntegration:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.llm = OpenAI()
        self.rule_based_prompt = PromptTemplate(
            input_variables=["clause_type"],
            template="根据以下条款类型生成相应文本：{clause_type}"
        )
        self.statistical_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('nb', MultinomialNB())
        ])
        self.client = OpenAI()  # 初始化 OpenAI client
        # 这里假设已经有训练数据 X_train, y_train
        # self.statistical_pipeline.fit(X_train, y_train)

    def rule_based_generation(self, clause_type):
        if clause_type == 'contract_term':
            return "根据合同约定，双方应履行以下义务：..."
        elif clause_type == 'payment_term':
            return "付款方式为：..."
        else:
            return ""

    def generate_text(self, input_text):
        prompt = PromptTemplate(
            input_variables=["input_text"],
            template="请根据以下输入生成招投标相关文本：{input_text}"
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(input_text)


    def fine_tune_model(self, training_data_path):
        # 0. 将训练文件修改为jsonl格式
        jsonl_path  = self.convert_csv_to_jsonl(training_data_path, training_data_path.replace('.csv', '.jsonl'))

        # 1. 上传训练文件
        training_file = openai.files.create(
            file=open(jsonl_path, "rb"),
            purpose="fine-tune"
        )

        # 2. 创建微调任务
        fine_tuning_job = openai.fine_tuning.jobs.create(
            training_file=training_file.id,
            model="gpt-3.5-turbo",  # 使用有效模型标识
            hyperparameters={
                "n_epochs": 3  # 可自定义训练轮次
            }
        )

        # 3. 更新模型ID（需异步获取）
        self.llm = fine_tuning_job.fine_tuned_model

    def convert_csv_to_jsonl(self,csv_file_path, jsonl_file_path=None):
        """
        将 CSV 文件转换为 JSONL 格式文件。

        参数：
            csv_file_path: CSV 文件的路径
            jsonl_file_path: （可选）生成的 JSONL 文件路径。如果不传入，则默认在同一目录下，文件名和 CSV 文件一致，只是扩展名变为 .jsonl
        返回值：
            生成的 JSONL 文件的路径
        """
        if jsonl_file_path is None:
            base_name = os.path.splitext(csv_file_path)[0]
            jsonl_file_path = base_name + ".jsonl"

        with open(csv_file_path, mode="r", encoding="utf-8") as fin, \
                open(jsonl_file_path, mode="w", encoding="utf-8") as fout:
            reader = csv.DictReader(fin)
            for row in reader:
                # 这里将 CSV 中 original_text 和 annotated_text 字段转换为 JSONL 格式的 prompt 和 completion
                data = {
                    "prompt": row["original_text"],
                    "completion": row["annotated_text"]
                }
                json_line = json.dumps(data, ensure_ascii=False)
                fout.write(json_line + "\n")

        return jsonl_file_path

    def combine_models_outputs(self, input_text):
        rule_based_output = self.rule_based_generation(input_text)
        statistical_output = self.statistical_pipeline.predict([input_text])[0]
        # 这里假设已经微调了模型，并且使用微调后的模型
        fine_tuned_output = self.generate_text(input_text)
        # 可以根据实际情况进行更复杂的融合逻辑，这里简单拼接
        combined_output = rule_based_output + " " + statistical_output + " " + fine_tuned_output
        return combined_output