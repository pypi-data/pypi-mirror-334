import re
import random

safe_globals = {
    '__builtins__': {
        # 基本内置函数
        'print': print,
        'len': len,
        'range': range,
        'int': int,
        'float': float,
        'str': str,
        'list': list,
        'dict': dict,
        'tuple': tuple,
        'set': set,
        'bool': bool,
        'type': type,
        'isinstance': isinstance,
        'min': min,
        'max': max,
        'sum': sum,
        'abs': abs,
        'round': round,
        'zip': zip,
        'map': map,
        'filter': filter,
        'sorted': sorted,
        'reversed': reversed,
        'enumerate': enumerate,
        'all': all,
        'any': any,
        'chr': chr,
        'ord': ord,
        'hex': hex,
        'bin': bin,
        'oct': oct,
        'id': id,
        'hash': hash,
        'repr': repr,
        'callable': callable,
        'hasattr': hasattr,
        'getattr': getattr,
        'setattr': setattr,
        'delattr': delattr,
        'property': property,
        'staticmethod': staticmethod,
        'classmethod': classmethod,
        'issubclass': issubclass,
        'super': super,
        'object': object,
        # 数学函数
        'pow': pow,
        'divmod': divmod,
        # 迭代工具
        'iter': iter,
        'next': next,
        # 异常处理
        'BaseException': BaseException,
        'Exception': Exception,
        'ValueError': ValueError,
        'TypeError': TypeError,
        'IndexError': IndexError,
        'KeyError': KeyError,
        'AttributeError': AttributeError,
        'StopIteration': StopIteration,
        # 其他
        'open': None,  # 禁用文件操作
        'eval': None,  # 禁用 eval
        'exec': None,  # 禁用 exec
        '__import__': None,  # 禁用导入模块
    },
    # 允许使用 re 模块的所有功能
    're': re,
    'random':random,
}



def extract_python_code(text: str) -> str | list:
    """
    从文本中提取Python代码块。
    参数:
        text (str): 包含代码块的文本。
    返回:
        list: 提取的Python代码块列表。
    ------
    Extract Python code blocks from text.

    Parameters:
    - text (str): The text containing code blocks.

    Returns:
    - list: A list of extracted Python code blocks.
    ------
    """
    # 正则表达式匹配Python代码块
    pattern = r'```python(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)

    # 去除每个匹配项的前后空白字符
    code_blocks = [match.strip() for match in matches]

    if not code_blocks:
        return [text.strip()]  # 如果没有匹配到代码块，返回空列表

    # 移除代码块中的import语句
    filtered_code_blocks = []
    for code in code_blocks:
        filtered_code = re.sub(r'^(import\s+[\w\.]+|from\s+[\w\.]+\s+import\s+[\w\*, ]+)\n', '', code,
                               flags=re.MULTILINE)
        filtered_code_blocks.append(filtered_code)

    return filtered_code_blocks


def exec_code(code: str, *args, **kwargs):
    codes = extract_python_code(code)
    locals_dict = {
        'args': args,
        'kwargs': kwargs,
        "data": None,
    }
    for _ in codes:
        try:
            exec(_, safe_globals, locals_dict)  # 输出 20
        except NameError as e:
            print("禁用/Disable:",e)
    return locals_dict['data']


