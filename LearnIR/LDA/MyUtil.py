import re

# def isNumber(word):
#     # 调用正则
#     value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
#     result = value.match(word)
#     if result:
#         return True
#     else:
#         return False

# 判断word是否为数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False