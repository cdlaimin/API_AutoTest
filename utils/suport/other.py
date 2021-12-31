def switch_name(name):
    """
    将驼峰式命名转换成下划线
    """
    change_name = ""
    for char in name:
        if char.isupper():
            change_name += '_' + char.lower()
        else:
            change_name += char

    return change_name.strip('_')
