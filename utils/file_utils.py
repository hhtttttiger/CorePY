import os
import hashlib

def get_file_extension(file_name):
    """
    获取文件名的后缀部分，并去除开头的点号（.）
    
    Args:
        file_name (str): 文件名
        
    Returns:
        str: 文件后缀，不含点号
    """
    return os.path.splitext(file_name)[1].lstrip('.')


def calculate_file_md5(file_path):
    """
    计算文件的 MD5 值。

    Args:
        file_path (str): 文件的路径。

    Returns:
        str: 文件的 MD5 值。

    Raises:
        FileNotFoundError: 如果指定的文件不存在。

    """
    # 尝试打开文件并读取内容
    try:
        with open(file_path, "rb") as f:
            # 创建 MD5 对象
            md5 = hashlib.md5()
            # 逐块更新 MD5
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
    except FileNotFoundError:
        # 如果文件不存在，则抛出 FileNotFoundError 异常
        raise FileNotFoundError(f"File '{file_path}' not found.")
    
    # 返回计算得到的 MD5 值
    return md5.hexdigest()