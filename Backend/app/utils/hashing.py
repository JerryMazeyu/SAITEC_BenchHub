import hashlib

def generate_id(name):
    """根据输入名称生成唯一 ID"""
    return hashlib.md5(name.encode('utf-8')).hexdigest()