def validate_dict(data, schema, allow_extra_keys=False):
    """
    这段代码的主要作用是验证一个多层嵌套字典的结构和数据类型是否符合预期的规则（由schema定义），并且在验证通过后对数据进行处理。具体功能包括：
        验证键是否存在：检查data中的键是否与schema中定义的键一致。
        验证值的类型：检查data中每个键对应的值是否符合schema中定义的类型（可以是单一类型、类型列表或嵌套字典）。
        支持值处理：如果schema中定义了处理函数（process），则对值进行处理。
        递归验证嵌套字典：如果data中的值是嵌套字典，则递归调用函数进行验证。
        返回处理后的数据：如果验证通过，返回处理后的数据；否则返回验证失败。
    ----
    验证多层嵌套字典中的键是否存在且值的类型符合预期。
    支持多选类型（通过列表或元组表示）和值处理（通过处理函数）。

    参数:
        data (dict): 需要验证的字典。
        schema (dict): 验证规则，键为需要检查的键，值为期望的类型或嵌套的schema。
                       如果值是一个列表或元组，表示可选类型。
                       如果值是一个字典，可以包含 'type' 和 'process' 键：
                           - 'type': 期望的类型或类型列表/元组。
                           - 'process': 可选的处理函数。
        allow_extra_keys (bool): 是否允许 data 中存在未在 schema 中定义的键。

    返回:
        tuple: (bool, dict)。第一个元素表示验证是否通过，第二个元素是处理后的数据。
    """
    if not isinstance(data, dict) or not isinstance(schema, dict):
        raise TypeError("data 和 schema 都必须是字典类型。")

    processed_data = {}  # 用于存储处理后的数据

    for key, expected in schema.items():
        if key not in data:
            print(f"键 '{key}' 不存在。")
            return False, None

        value = data[key]

        # 如果期望值是字典，递归验证嵌套字典
        if isinstance(expected, dict):
            # 检查类型是否符合预期
            if "type" in expected:
                expected_type = expected["type"]
                if isinstance(expected_type, (list, tuple)):
                    if not any(isinstance(value, t) for t in expected_type):
                        print(
                            f"键 '{key}' 的值类型不符合预期。期望类型为 {expected_type} 中的任意一种，实际类型为 {type(value)}。")
                        return False, None
                elif isinstance(expected_type, type):
                    if not isinstance(value, expected_type):
                        print(f"键 '{key}' 的值类型不符合预期。期望类型为 {expected_type}，实际类型为 {type(value)}。")
                        return False, None

            # 递归处理嵌套字典
            if isinstance(value, dict):
                is_valid, processed_value = validate_dict(value, expected, allow_extra_keys)
                if not is_valid:
                    return False, None
                processed_data[key] = processed_value
            else:
                processed_data[key] = value

            # 如果有处理函数，调用处理函数
            if "process" in expected and callable(expected["process"]):
                try:
                    processed_data[key] = expected["process"](processed_data[key])
                except Exception as e:
                    print(f"处理键 '{key}' 的值时发生错误: {e}")
                    return False, None

        # 如果期望值是类型或类型列表/元组，直接验证值的类型
        elif isinstance(expected, (list, tuple)):
            if not any(isinstance(value, t) for t in expected):
                print(f"键 '{key}' 的值类型不符合预期。期望类型为 {expected} 中的任意一种，实际类型为 {type(value)}。")
                return False, None
            processed_data[key] = value
        elif isinstance(expected, type):
            if not isinstance(value, expected):
                print(f"键 '{key}' 的值类型不符合预期。期望类型为 {expected}，实际类型为 {type(value)}。")
                return False, None
            processed_data[key] = value

    # 处理未在 schema 中定义的键
    if not allow_extra_keys:
        extra_keys = set(data.keys()) - set(schema.keys())
        if extra_keys:
            print(f"发现未定义的键: {extra_keys}")
            return False, None
    else:
        for key in data:
            if key not in schema:
                processed_data[key] = data[key]

    return True, processed_data

