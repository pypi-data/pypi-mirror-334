import requests
import json
import pprint
import re


def add_system(messages: list, message):
    messages.append({"role": "system", "content": message})
    return messages


def add_user(messages: list, message):
    messages.append({"role": "user", "content": message})
    return messages


def add_assistant(messages: list, message):
    messages.append({"role": "assistant", "content": message})
    return messages


class LLM_API:
    """
    封装符号openai请求格式的API。
    """

    def __init__(self, api_key, model_name, url,
                 max_tokens=8000,
                 max_seq_len=8000,
                 temperature=0.7,
                 top_k=50,
                 top_p=1,
                 frequency_penalty=0,
                 stream=False,
                 ):
        """
        :param api_key: 用户的API密钥
        :param model_name: 使用的模型名称
        :param url: 发送提问的完整URL
        """
        self.api_key = api_key
        self.model_name = model_name
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # 初始化默认参数
        self.max_tokens = max_tokens
        self.max_seq_len = max_seq_len
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.stream = stream

    def send_request(self, messages: list | str,
                     max_tokens=None,
                     temperature=None,
                     top_k=None,
                     top_p=None,
                     frequency_penalty=None,
                     max_seq_len=None,
                     stream=None):
        """
        向语言模型发送请求并获取响应。 / Send a request to the language model and retrieve the response.
        :param messages: 消息列表，包含system、user和assistant等角色的消息。 / A list of messages containing roles such as system, user, and assistant.
        :param max_tokens: 最大输出token数。 / The maximum number of output tokens.
        :param temperature: 温度参数，控制输出的随机性。 / The temperature parameter, controlling the randomness of the output.
        :param top_k: 采样范围，控制生成的多样性。 / The sampling range, controlling the diversity of generation.
        :param top_p: 概率采样范围。 / The probability sampling range.
        :param frequency_penalty: 频率惩罚，避免重复内容。 / The frequency penalty, avoiding repetitive content.
        :param max_seq_len: 最大序列长度（输入+输出）。 / The maximum sequence length (input + output).
        :return: 模型的响应内容
        """
        if not stream: stream = self.stream
        # 如果传入的参数为None，则使用初始化时的默认值
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        temperature = temperature if temperature is not None else self.temperature
        top_k = top_k if top_k is not None else self.top_k
        top_p = top_p if top_p is not None else self.top_p
        frequency_penalty = frequency_penalty if frequency_penalty is not None else self.frequency_penalty
        max_seq_len = max_seq_len if max_seq_len is not None else self.max_seq_len

        # 如果messages类型为str,默认使用用户角色发送
        if isinstance(messages, str): messages = add_user([], messages)

        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "max_seq_len": max_seq_len
        }
        if stream:
            payload["stream"] = True
            response = requests.post(self.url,
                                     headers=self.headers,
                                     data=json.dumps(payload),
                                     timeout=60 * 30,
                                     stream=True
                                     )
            content = ""
            for chunk in response.iter_lines(chunk_size=None):
                if chunk:
                    chunk_str = chunk.decode('utf-8').strip()
                    if chunk_str.startswith("data: "):
                        json_str = chunk_str[6:]
                        if json_str == "[DONE]":
                            return content
                        else:
                            json_data = json.loads(json_str)
                            data = json_data['choices'][0]['delta']
                            if 'reasoning_content' in data and data['reasoning_content']:
                                print(data['reasoning_content'], end="")
                            if 'content' in data and data['content']:
                                print(data['content'], end="")
                                content += data['content']
                    else:
                        data = json.loads(chunk_str)
                        if "done" in data['done']:
                            if data['done'] == True:
                                return self._extract_think_and_response(content)[0]
                        content += data['message']['content']
                        print(data['message']['content'], end="")
        else:
            payload["stream"] = False
            response = requests.post(self.url,
                                     headers=self.headers,
                                     data=json.dumps(payload),
                                     timeout=60 * 30
                                     )

            if response.status_code == 200:
                response_data = response.json()
                print(response_data)
                if 'message' in response_data:
                    pprint.pprint(response_data['message']["content"])
                    response_content = self._extract_think_and_response(response_data['message']["content"])
                    return response_content[0]
                else:
                    response_content = self._extract_think_and_response(
                        response_data["choices"][0]["message"]["content"])
                    return response_content[0]
            else:
                try:
                    pprint.pprint(response.json())
                except Exception as e:
                    print(e)
                    pprint.pprint(response.text)
                raise Exception(f"请求失败，状态码：{response.status_code}, 错误信息：{response.text}")

    def _extract_think_and_response(self, text):
        """
        Extract the content within <think> tags and the content outside of these tags.
        :param text: The input text to process.
        :return: A tuple containing (thinking_content, response)
        """
        # Define the regex pattern
        pattern = re.compile(r'<think>(.*?)</think>', re.DOTALL)

        # Search for <think> tags
        match = pattern.search(text)

        if match:
            # Extract the content within <think> tags
            thinking_content = match.group(1).strip()
            # Extract the content outside <think> tags
            response = pattern.sub('', text).strip()
        else:
            # If no <think> tags are found, return an empty string for thinking_content
            # and the original text as response
            thinking_content = ""
            response = text.strip()

        return response, thinking_content
