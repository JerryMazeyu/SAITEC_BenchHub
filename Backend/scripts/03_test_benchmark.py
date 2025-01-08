import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from flask import current_app
from app import create_app
import requests
import sqlite3
from random import choice
from utils import printtify, Style
import warnings
warnings.filterwarnings('ignore')



BASE_URL = "http://127.0.0.1:5000/benchmarks"  # Flask 服务的地址


# 向数据库插入初始数据
def start_server(config_class):
    printtify("启动项目!", color="green")
    app = create_app(config_class)
    global DB_PATH
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DB_PATH = rf"{os.path.join(BASE_DIR, 'instance', 'test.db')}"
    printtify(f"使用数据库路径为：{DB_PATH}")
    global DATA_PATH
    DATA_PATH = app.config["DATA_ROOT"]
    global BACKUP_PATH
    BACKUP_PATH = app.config["TRASH_ROOT"]
    return app


def get_random_testcase_id():
    """
    从数据库中随机获取一个 Testcase 的 ID。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 查询所有 ID
    cursor.execute("SELECT id FROM testcases")
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not ids:
        raise Exception("数据库中没有 Testcase 数据")
    
    id = choice(ids)
    printtify(f"从数据库中随机选择一个 Testcase ID: {id}", color="green")
    return id


def get_random_folder():
    """
    从指定目录中随机选择一个文件夹。
    """
    
    folders = [f for f in os.listdir(DATA_PATH) if os.path.isdir(os.path.join(DATA_PATH, f))]
    res = os.path.join(DATA_PATH, choice(folders))
    printtify(f"选择文件夹路径为：{res}")
    return res
    

def sync_data():
    printtify("============开始测试同步接口 /sync============", bright=True)
    response = requests.post(f"{BASE_URL}/sync")
    if response.status_code == 200:
        printtify("同步成功:", data = response.json(), color="green")
    else:
        printtify("同步失败:", data = response.text, color="red")
        raise Exception("同步失败")

def verify_testcase_count():
    """
    验证数据库中 Testcase 的数量是否与本地数据一致。
    """
    printtify("============验证数据库中的 Testcase 数量是否正确============", bright=True)
    # 获取本地 Testcase 数量
    local_testcases = [folder for folder in os.listdir(DATA_PATH) if os.path.isdir(os.path.join(DATA_PATH, folder))]
    local_count = len(local_testcases)

    # 查询数据库中的 Testcase 数量
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM testcases")
    db_count = cursor.fetchone()[0]
    conn.close()

    printtify(f"本地 Testcase 数量: {local_count}, 数据库 Testcase 数量: {db_count}")
    if local_count == db_count:
        printtify("数量一致.", color="green")
    else:
        printtify("数量不一致!", color="red")

def test_get_all_testcases():
    """
    测试获取所有 Testcase 的接口。
    """
    printtify("============测试获取所有 Testcase 接口 /testcases?page=-1============", bright=True)
    response = requests.get(f"{BASE_URL}/testcases?page=-1")
    if response.status_code == 200:
        data = response.json()
        printtify("获取成功", data, color="green")
    else:
        printtify("获取失败:", response.text, color="red")

def test_query_testcase_by_id():
    """
    测试通过 ID 查询 Testcase。
    """
    printtify(f"============测试通过 ID 查询 Testcase /testcases?id=xxxxx============", bright=True)
    testcase_id = get_random_testcase_id()
    response = requests.get(f"{BASE_URL}/testcases?id={testcase_id}")
    if response.status_code == 200:
        data = response.json()
        printtify(f"查询成功.", data, color="green")
    else:
        printtify("查询失败:", response.text, color="red")


def test_query_testcase_by_data_dimension(data_dimension):
    """
    测试通过 data_dimension 查询 Testcase。
    """
    printtify(f"============测试通过 data_dimension 查询 Testcase /testcases?data_dimension={data_dimension}============", bright=True)
    response = requests.get(f"{BASE_URL}/testcases?data_dimension={data_dimension}")
    if response.status_code == 200:
        data = response.json()
        printtify(f"查询成功.", data, color="green")
    else:
        printtify("查询失败:", response.text, color="red")


def test_pagination(page, page_size):
    """
    测试分页接口。
    """
    printtify(f"============测试分页接口 /testcases?page={page}&page_size={page_size}============", bright=True)
    response = requests.get(f"{BASE_URL}/testcases?page={page}&page_size={page_size}")
    if response.status_code == 200:
        data = response.json()
        printtify(f"分页查询成功.", data, color="green")
    else:
        printtify("分页查询失败:", response.text, color="red")

def get_random_testcase_id_and_version():
    """
    随机从数据库中选择一个 Testcase 的 ID 和一个版本。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 查询所有 Testcase 和版本
    cursor.execute("""
        SELECT t.id, v.version
        FROM testcases t
        JOIN versions v ON t.id = v.testcase_id
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise Exception("数据库中没有 Testcase 和版本数据")

    return choice(rows)  # 返回随机选择的 (testcase_id, version)

def test_modify_version():
    """
    测试软修改接口。
    """
    printtify(f"============测试软修改 Testcase xxx 的版本 xxx============", bright=True)
    testcase_id, version = get_random_testcase_id_and_version()
    modifications = {"meta": {"description": "这是修改后的描述"}}

    response = requests.post(
        f"{BASE_URL}/testcases/{testcase_id}/{version}",
        json={"operation": "modify", "modifications": modifications}
    )

    if response.status_code == 200:
        printtify(f"修改成功", response.json(), color="green")
        # 验证是否在 backup 文件夹中存在原始版本
        original_backup_path = os.path.join(BACKUP_PATH, testcase_id, f"{version}.json")
        if not os.path.exists(original_backup_path):
            printtify(f"Backup 文件夹中未找到原始版本文件: {original_backup_path}", color="red")
            raise Exception(f"Backup 文件夹中未找到原始版本文件: {original_backup_path}")
        printtify(f"原始版本文件已备份: {original_backup_path}", color="green")
    else:
        printtify(f"修改失败", response.text, color="red")


def test_delete_testcase():
    """
    测试删除整个 Testcase。
    """
    testcase_id, _ = get_random_testcase_id_and_version()

    printtify(f"============测试删除 Testcase {testcase_id}============", bright=True)
    response = requests.delete(f"{BASE_URL}/testcases/{testcase_id}")

    if response.status_code == 200:
        printtify("删除成功", response.json(), color="green")
        # 验证是否在 backup 文件夹中存在整个 Testcase 的备份
        testcase_backup_path = os.path.join(BACKUP_PATH, testcase_id)
        if not os.path.exists(testcase_backup_path):
            raise Exception(f"Backup 文件夹中未找到 Testcase 的备份: {testcase_backup_path}")
        printtify(f"Testcase 已备份: {testcase_backup_path}", color="green")
    else:
        printtify(f"删除失败", response.text, color="red")
        raise Exception("删除 Testcase 测试失败")


def test_add_testcase():
    """
    测试新增 Testcase。
    """
    folder_path = input("输入添加路径：")
    if not folder_path:
        folder_path = get_random_folder()
    printtify(f"============测试新增 Testcase, 文件夹路径: {folder_path}============", bright=True)
    response = requests.post(
        f"{BASE_URL}/testcases",
        json={"folder_path": folder_path}
    )

    if response.status_code == 201:
        printtify(f"添加成功", response.json(), color="green")
        # 验证是否添加到数据库
        added_testcase = response.json()["data"]
        testcase_id = added_testcase["id"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM testcases WHERE id = ?", (testcase_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise Exception(f"数据库中未找到新增的 Testcase: {testcase_id}")
        printtify(f"数据库中已成功添加 Testcase: {testcase_id}", color="green")
    else:
        printtify(f"添加失败", response.text, color="red")
        raise Exception("新增 Testcase 测试失败")


def test_search_dimension():
    """
    测试查询dimension。
    """
    from time import sleep
    response = requests.get(f"{BASE_URL}/dimensions")
    if response.status_code == 200:
        printtify(f"查询成功", response.json(), color="green")
    else:
        printtify(f"查询失败", response.text, color="red")
        raise Exception("查询 Dimension 测试失败")
    printtify(f"等待2s, 观察是否从缓存中查询.")
    sleep(2)
    response = requests.get(f"{BASE_URL}/dimensions")
    if response.status_code == 200:
        printtify(f"查询成功", response.json(), color="green")
    else:
        printtify(f"查询失败", response.text, color="red")
        raise Exception("查询 Dimension 测试失败")
    
    
    

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a config for the Flask application.")
    parser.add_argument(
        "--env",
        choices=["development", "testing"],
        default="testing",
        help="Specify the environment.",
    )
    args = parser.parse_args()
    printtify("Step3. Benchmark模块测试", align="center", bright=True)
    config_class = f"app.config.{args.env.capitalize()}Config"
    printtify(f"使用配置文件为: {config_class}")
    # 启动 Flask 应用
    app = start_server(config_class)

    # 启动服务
    printtify("启动 Flask 服务.")
    from threading import Thread
    server_thread = Thread(target=app.run, kwargs={"host": "127.0.0.1", "port": 5000, "debug": False})
    server_thread.start()

    try:
        # 测试同步接口
        sync_data()

        # 验证 Testcase 数量
        verify_testcase_count()

        # 测试获取所有 Testcase
        test_get_all_testcases()

        # 测试通过 ID 查询
        test_query_testcase_by_id()

        # 测试通过 data_dimension 查询
        example_dimension = "文本问答"  # 替换为实际的 data_dimension
        test_query_testcase_by_data_dimension(example_dimension)

        # 测试分页接口
        test_pagination(page=1, page_size=10)

        # 测试修改
        test_modify_version()

        # 测试删除
        test_delete_testcase()

        # 测试增加
        test_add_testcase()

        # 测试查询dimension
        test_search_dimension()


    except Exception as e:
        printtify(f"测试失败: \n {e}", color="red")

    finally:
        # 停止 Flask 服务
        printtify("停止 Flask 服务")
        server_thread.join(timeout=1)


