import os
import datetime

def move_file(source_path, dest_path):
    """
    将文件从 source_path 移动到 dest_path，如果目标路径文件已存在，则重命名目标文件。
    :param source_path: 源文件路径
    :param dest_path: 目标文件路径
    """
    try:
        if os.path.exists(dest_path):
            # 添加时间戳后缀或递增编号避免冲突
            base, ext = os.path.splitext(dest_path)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_dest_path = f"{base}_{timestamp}{ext}"

            # 如果冲突文件依然存在，递增编号
            counter = 1
            while os.path.exists(new_dest_path):
                new_dest_path = f"{base}_{timestamp}_{counter}{ext}"
                counter += 1

            print(f"目标文件 {dest_path} 已存在，重命名为 {new_dest_path}。")
            dest_path = new_dest_path

        # 移动文件
        os.rename(source_path, dest_path)
        print(f"已将文件从 {source_path} 移动到 {dest_path}。")
    except Exception as e:
        raise RuntimeError(f"移动文件时出错：{str(e)}")
