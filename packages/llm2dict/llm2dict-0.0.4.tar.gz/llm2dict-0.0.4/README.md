# llm2dict
<span>
<img src=https://img.shields.io/badge/version-0.0.3-blue>
<img src=https://img.shields.io/badge/license-MIT-green>  
</span>

### 简介 
**llm2dict** 通过与大型语言模型（LLM）的两次交互，将自然语言的回答自动转换为结构化的 Python **字典dict** / **列表list**。

<!-- 旨在通过与大语言模型（LLM）的两次交互，将自然语言转换为结构化的 Python 字典或列表数据。这个包的核心功能是通过两次提问，第一次获取大语言模型的自然语言回答，第二次则提取特定格式的数据并将其转换为 Python 可执行的代码，最终返回结构化的数据(**dict**或**list**)。 -->
 


**llm2dict** 将提取格式的任务交给了 LLM 处理：

- 第一次提问：获取 LLM 的自然语言回答。 
- 第二次提问：让 LLM 根据第一次的回答和指定的数据结构，生成提取数据的 Python 代码。 
- 代码执行：自动执行生成的代码，返回结构化的数据。 

你只需输入问题和期望的数据结构，即可获得**关键词确定**的结构化的数据，让LLM的注意力回到问题本身。



### 安装与使用  

你可以通过以下命令安装 **llm2dict** 包：
```bash
pip install llm2dict
```  

**使用示例**  
```python
from llm2dict import llm2dict,LLM_API
#  硅基流动API: https://cloud.siliconflow.cn/models
api_key = "<修改成你的api_key>"
url = "https://api.siliconflow.cn/v1/chat/completions"
model_name = "Qwen/QwQ-32B"
llm=LLM_API(api_key,model_name,url)

# 发给llm的提问
msg = "写关于爱情的歌，要顺口，歌词不要太多重复，可以短一点。写一下这首歌的简介（50字）。起一个歌名。为这首歌写一个吸引人的长句标题（参考小红书风格）。写5条这首歌的评论（参考网易云音乐的评论风格）"

#str 用文本设定返回的数据结构
data_structures = """
{
    "歌名": str,
    "歌词": list,  # 每一句歌词一项,放到列表里
    "简介": str,
    "标题": str,
    "评论": list,
}
"""

# 调用llm2dict函数，使llm返回结构化数据
dict_data = llm2dict(msg,data_structures,llm.send_request)
print("dict_data:",dict_data)
```  

返回数据：
```python
{'歌名': '《心跳拼图》',
 '歌词': ['图书馆第三排的风掀动书页',
        '你睫毛投下的阴影 在我手背作祟',
        '橡皮擦蹭过草稿纸的轻响',
        '偷走了所有解题公式',
        '指纹在玻璃窗写下未完成的吻',
        '时针停摆在借阅卡签名的那秒',
        '我们都是散落的拼图碎片',
        '在安全距离外 碰撞成银河',
        '自动贩卖机吞下硬币的闷响',
        '映出你侧脸轮廓的金属回响',
        '奶茶杯沿的唇印半颗月亮',
        '被我藏进校服口袋发酵成糖'],
 '简介': "慵懒吉他与电子音效交织，讲述暗恋时笨拙又甜蜜的试探。用'指纹吻''时针停摆'等意象，勾勒出不敢完全靠近却渴望完整的心动模样。",
 '标题': '#爱情就像散落的拼图碎片 我在歌词里藏了三个心动瞬间 星星吻过眼睑的夜晚 愿你也拥有《心跳拼图》的勇气🌙✨',
 '评论': ["副歌那句'碰撞成银河'直接戳到泪点，想起高三教室窗外的星光",
        "verse里'吞下硬币的闷响'细节太戳我！就是我们初遇的自动贩卖机",
        '建议循环播放第五遍开始，电子音效像心跳漏拍的节奏，耳膜在恋爱',
        '最后奶茶杯沿的唇印细节太绝了！我直接把这句设为锁屏壁纸了',
        "在网易云听歌时旁边女生突然小声念'指纹在玻璃窗写下未完成的吻'，原来我们都在听这首"]}
```  



### 项目结构
```
├── llm2dict/               
│   ├── llm2dict.py     # 核心实现
│   ├── api.py          # 大模型API
│   ├── execute.py      # 执行生成的代码
│   ├── prompt.py       # 生成代码的提示词模版
│   └── validate.py     # 数据结构验证
```


### 代码说明

**函数名：** **llm2dict()**  
**说明：** 核心函数，使模型输出结构化数据  
```python
llm2dict(msg, data_structures, api) -> dict|list|False
```
**传入参数：**
| 参数名 | 类型 | 可选 | 说明 |
|-----|-----|-----|-----|
| msg | list/str | 否 | 向大模型发送的提问，例：[{"role": "system", "content": ""},{"role": "user", "content": ""}] |
|data_structures|str|否| 希望返回的格式，例：<br>"{'歌名': str,<br> '歌词': list, #每一句一项<br> '简介': str,<br> '标题': str,<br> '评论': list,\|False, <br>'标题': str, <br>'评论': list\|False,}" |
| api | function |否 | 封装好的大模型API，传入问题(str)，返回大模型生成的回答(str) | 
| to_code_api | function | 可选 | 指定第二次交换的大模型API | 
| delay | int | 可选 | 2次请求API的间隔时间 | 
| to_dict_prompt_template | str | 可选 | 提示词模板，用于生成提取数据的python代码。可参考prompt.py中的dict_prompt_template | 

**返回值：** **dict**/**list** | **Flase**

----
  
**类名：** **LLM_API**  
**说明：** 大模型接口，封装了请求大模型API的函数，支持多个平台
```python
llm=LLM_API(api_key, model_name, url)
llm.send_request("1+1等于多少?")
```
**传入参数：**
| 参数名 | 类型 | 可选 | 说明 |
|-----|-----|-----|-----|
| api_key | str | 否 | API平台秘钥 |
| model_name | str | 否 | 模型名称 |
| url | str | 否 | 完整的请求url |

**硅基流动**
```python
    # 硅基流动 https://cloud.siliconflow.cn/models
    api_key = "填入api_key"
    url = "https://api.siliconflow.cn/v1/chat/completions"
    model_name = "Qwen/QwQ-32B"
    llm = LLM_API(api_key=api_key, model_name=model_name, url=url)
    llm.max_tokens = 16000 #设定最大返回token数
    max_seq_len = 16000 #设定最大序列长度
    print(llm.send_request("1+1等于多少?"))
```

**DeepSeek**
```python
    # DeepSeek https://platform.deepseek.com/usage
    api_key = "填入api_key" 
    url = "https://api.deepseek.com/v1/chat/completions"
    model_name = "deepseek-chat"
    llm = LLM_API(api_key=api_key, model_name=model_name, url=url)
    print(llm.send_request("1+1等于多少?"))
```

**KIMI**
```python
    # KIMI https://platform.moonshot.cn/docs/intro#%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B
    api_key = "填入api_key"
    url = "https://api.moonshot.cn/v1/chat/completions"
    model_name = "moonshot-v1-8k"
    llm = LLM_API(api_key=api_key, model_name=model_name, url=url)
    print(llm.send_request("1+1等于多少?"))
```

**阿里云百炼**
```python
    # 阿里云百炼 https://www.aliyun.com/product/bailian
    api_key = "填入api_key"
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    model_name = "qwq-32b"
    #阿里云需要stream=True
    llm = LLM_API(api_key=api_key, model_name=model_name, url=url, stream=True)
    print(llm.send_request("1+1等于多少?"))
```
**火山引擎**
```python
    # 豆包 https://www.volcengine.com/product/doubao
    api_key = "填入api_key"
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    model_name = "deepseek-r1-250120"
    llm = LLM_API(api_key=api_key, model_name=model_name, url=url)
    print(llm.send_request("1+1等于多少?"))
```

----
**函数名：** **add_system() / add_user() / add_assistant()** 构建提问/提问上下文
```python
msg = []
msg = add_system(msg, "你是AI助手")
msg = add_user(msg, "1+1等于多少")
msg = add_assistant(msg, "1+1等于2")
print(msg)
```
返回:
```python
[
    {"role": "system", "content": "你是AI助手"}, 
    {"role": "user", "content": "1+1等于多少"}, 
    {"role": "assistant", "content": "1+1等于2"}
]
```
----
**函数名：** **validate_dict**  
**说明：** 验证数据结构是否符合规则  
**传入参数：**
| 参数名 | 类型 | 可选 | 说明 |
|-----|-----|-----|-----|
| data | dict | 否 | 被检验的数据 |
| schema | dict | 否 | 检验规则 |
| allow_extra_keys | bool | 可选 | 是否把data中没有被schema检验的数据也返回 |  

验证数据类型：
```python
data={
    "name":"alice",
    "age":30.5,
}
schema={
    "name":str,
    "age":[int,float]
}
validate_dict(data,schema)
```
验证成功：
```python
(True, {'name': 'alice', 'age': 30.5})
```
"age"类型不符合规则：
```python
data={
    "name":"alice",
    "age":"30.5",
}
schema={
    "name":str,
    "age":[int,float]
}
validate_dict(data,schema)
```
验证失败，返回：
```python
(False, None)
```
根据schema，data缺失"address"数据：
```python
data={
    "name":"alice",
    "age":30.5,
}
schema={
    "name":str,
    "age":[int,float],
    "address":{
        "city": str,
    }
}
validate_dict(data,schema)
```
验证失败，返回：
```python
(False, None)
```

使用{'type':str,'process': lambda x: x.upper()}  
传入的处理函数，对"city"数据做处理：
```python
data={
    "name":"alice",
    "age":30.5,
    "address":{
        "city":"shanghai"
    }
}
schema={
    "name":str,
    "age":[int,float],
    "address":{
        "city": {'type':str,'process': lambda x: x.upper()},
    }
}
validate_dict(data,schema)
```
验证成功并处理后返回：
```python
(True, {'name': 'alice', 'age': 30.5, 'address': {'city': 'SHANGHAI'}})
```

----


##### 其他  
- 需要使用QWQ32b/deepseek-r1:671b 以上模型