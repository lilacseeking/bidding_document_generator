import csv
from openai import OpenAI
import numpy as np
import pandas as pd
import json
import os
import time
from requests import post, get
import dashscope
from dashscope import Generation
from langchain import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


class NLPModelIntegrationAliyun:
    def __init__(self, access_key_secret):
        # 初始化百炼SDK
        dashscope.api_key = access_key_secret
        self.client = OpenAI(
            api_key=dashscope.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.fine_tuned_model_id = ''
        self.bucket_name = 'lilacseeking-bidding'  # 替换为实际bucket名称
        self.job_id = 'ft-202504200508-06d8'
        # self.job_id = ''

        # 初始化统计模型
        self.statistical_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('nb', MultinomialNB())
        ])

    def rule_based_generation(self, clause_type):
        # 规则生成部分保持不变
        if clause_type == 'contract_term':
            return "根据合同约定，双方应履行以下义务：..."
        elif clause_type == 'payment_term':
            return "付款方式为：..."
        else:
            return ""

    def generate_text(self, input_text):
        # 使用百炼的生成API
        response = Generation.call(
            model='qwen-max',
            prompt=input_text,
            max_length=500,
            top_p=0.8
        )
        return response.output.text

    def upload_file_to_dashscope(self, file_path, description):
        """
        上传文件到 DashScope 的 Python 实现

        参数:
        api_key (str): DashScope API 密钥
        file_path (str): 要上传的文件路径
        description (str): 文件描述文本

        返回:
        dict: 包含响应状态码和内容的字典
        """
        url = 'https://dashscope.aliyuncs.com/api/v1/files'

        headers = {
            'Authorization': f'Bearer {dashscope.api_key}'  # 从实例属性获取密钥
        }

        try:
            with open(file_path, 'rb') as f:
                files = {
                    'files': (os.path.basename(file_path), f),  # 文件字段
                    'descriptions': (None, description)  # 文本字段
                }

                response = post(
                    url,
                    headers=headers,
                    files=files
                )

                # 处理响应
                if response.status_code == 200:
                    return {
                        'status': 'success',
                        'code': response.status_code,
                        'data': response.json()
                    }
                else:
                    return {
                        'status': 'error',
                        'code': response.status_code,
                        'message': response.text
                    }

        except FileNotFoundError:
            return {'status': 'error', 'message': 'File not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def create_fine_tune(self, training_file_ids, model="qwen2.5-72b-instruct", hyper_parameters=None,
                         training_type="efficient_sft"):
        """
        创建 DashScope 微调任务
        Args:
            training_file_ids (list): 训练文件的ID列表
            model (str): 基础模型名称（默认 qwen-turbo）
            hyper_parameters (dict): 超参数（默认为空字典）
            training_type (str): 训练类型（默认 sft）
        Returns:
            dict: API 响应结果
        """
        url = "https://dashscope.aliyuncs.com/api/v1/fine-tunes"

        headers = {
            "Authorization": f"Bearer {dashscope.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "training_file_ids": training_file_ids,
            "hyper_parameters": {
                "n_epochs": 1,
                "batch_size": 5,
                "learning_rate": "5e-5",
                "split": 0.9,
                "warmup_ratio": 0.1,
                "eval_steps": 100,
                "lora_rank": 16,
                "gradient_accumulation_steps": 2
            },
            "training_type": training_type
        }

        try:
            response = post(url, headers=headers, json=data)
            response.raise_for_status()  # 检查 HTTP 错误
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            if response:
                print(f"响应状态码: {response.status_code}, 内容: {response.text}")
            return None

    def fine_tune_model(self, training_data_path):
        # 转换数据格式并上传
        if self.job_id == '':
            jsonl_path = '../data/bidding_data_bailian.jsonl'
            upload_result = self.upload_file_to_dashscope(jsonl_path, jsonl_path)

            # 创建微调任务
            job = self.create_fine_tune(
                training_file_ids=[file['file_id'] for file in upload_result['data']['data']['uploaded_files']],
                # 替换为实际文件ID
                hyper_parameters={"epochs": 3}  # 可选参数
            )
            self.job_id = job.get('output').get('job_id')

        # self.statistical_pipeline.fit(self.load_training_data())

        # 轮询任务状态：使用 FineTunes.get
        task = self.wait_for_fine_tune_completion(self.job_id)  # 从响应中提取 job_id

        # 获取微调后的模型ID
        # self.fine_tuned_model_id = task.get('output').get('job_name')
        self.fine_tuned_model_id = 'qwen-max'

    def load_training_data(self):
        df = pd.read_csv('../data/project_cases.csv')
        text_columns = df.columns[:-1]
        X = df[text_columns].apply(lambda row: ' '.join(row.astype(str)), axis=1).values
        y = df.iloc[:, -1].values  # 标签列

        # 确保 X 是一个字符串数组
        X = np.array([str(x) for x in X])

        # 确保 y 是一维数组
        y = np.array(y).reshape(-1)

        # 数据验证
        if len(X) == 0 or len(y) == 0:
            raise ValueError("数据集为空")
        if len(X) != len(y):
            raise ValueError("特征与标签数量不匹配")
        return X, y

    def fine_tune_with_dashscope_api(self):
        # 使用百炼模型的HTTP API进行微调
        url = "https://dashscope.aliyuncs.com/api/v1/fine-tunes"

        headers = {
            "Authorization": f"Bearer {dashscope.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "qwen-turbo",
            "training_file_ids": [self.job_id],  # 使用当前任务ID
            "hyper_parameters": {"epochs": 3},
            "training_type": "efficient_sft"
        }

    def wait_for_fine_tune_completion(self, job_id, poll_interval=15):
        """
        同步阻塞等待微调任务完成
        Args:
            job_id (str): 微调任务ID
            poll_interval (int): 轮询间隔秒数（默认60）
        Returns:
            dict: 最终任务详情
        Raises:
            Exception: 任务失败时抛出异常
        """
        while True:
            # 获取任务状态
            job_info = self.get_fine_tune(job_id)
            if not job_info:
                raise Exception("获取任务状态失败")

            status = job_info.get('output').get('status')
            print(f"当前任务状态: {status} (轮询时间: {time.strftime('%Y-%m-%d %H:%M:%S')})")

            # 成功/失败状态处理
            if status == "SUCCEEDED":
                print(f"微调成功！模型ID: {job_info.get('output').get('job_name')}")
                return job_info
            elif status in ("FAILED", "CANCELLED"):
                error_msg = job_info.get('output').get('message', '未知错误')
                raise Exception(f"微调失败: {error_msg}")
            elif status in ["PENDING", "RUNNING", "QUEUING"]:
                print(f"等待 {poll_interval} 秒后重试...")
                time.sleep(poll_interval)
            else:
                raise Exception(f"未知状态: {status}")

    def get_fine_tune(self, job_id):
        """
        获取 DashScope 微调任务详情
        Args:
            job_id (str): 微调任务ID (例如 "ft-123456")
        Returns:
            dict: API 响应结果（包含任务状态、模型ID等信息）
        """
        url = f"https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}"

        headers = {
            "Authorization": f"Bearer {dashscope.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = get(url, headers=headers)
            response.raise_for_status()  # 自动处理 4xx/5xx 错误
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            if response:
                print(f"状态码: {response.status_code}, 错误详情: {response.text}")
            return None

    def convert_csv_to_jsonl(self, csv_file_path):
        # 转换逻辑保持不变
        jsonl_file_path = csv_file_path.replace('.csv', '.jsonl')
        with open(csv_file_path, 'r', encoding="utf-8") as fin, open(jsonl_file_path, 'w', encoding="utf-8") as fout:
            reader = csv.DictReader(fin)
            for row in reader:
                data = {
                    "prompt": row["original_text"],
                    "completion": row["annotated_text"]
                }
                fout.write(json.dumps(data) + '\n')
        return jsonl_file_path

    def combine_models_outputs(self, input_text, model_name):
        # 组合各模型输出
        rule_output = self.rule_based_generation('contract_term')
        # statistical_output = self.statistical_pipeline.predict([input_text])[0]

        # 使用微调后的模型
        ft_response = dashscope.Generation.call(
            api_key=dashscope.api_key,
            model=self.fine_tuned_model_id,
            prompt=input_text
        )
        combined = f"{rule_output}\n{ft_response.get('output').get('text')}"
        return combined