import openai
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
        # 1. 上传训练文件
        training_file = self.client.files.create(
            file=open(training_data_path, "rb"),
            purpose="fine-tune"
        )

        # 2. 创建微调任务
        fine_tuning_job = self.client.fine_tuning.jobs.create(
            training_file=training_file.id,
            model="gpt-3.5-turbo-0613",  # 使用有效模型标识
            hyperparameters={
                "n_epochs": 3  # 可自定义训练轮次
            }
        )

        # 3. 更新模型ID（需异步获取）
        self.llm = fine_tuning_job.fine_tuned_model


    def combine_models_outputs(self, input_text):
        rule_based_output = self.rule_based_generation(input_text)
        statistical_output = self.statistical_pipeline.predict([input_text])[0]
        # 这里假设已经微调了模型，并且使用微调后的模型
        fine_tuned_output = self.generate_text(input_text)
        # 可以根据实际情况进行更复杂的融合逻辑，这里简单拼接
        combined_output = rule_based_output + " " + statistical_output + " " + fine_tuned_output
        return combined_output