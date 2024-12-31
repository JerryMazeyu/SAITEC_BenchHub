import os
import json
from datetime import datetime
from app.utils.hashing import generate_id
from flask import request, jsonify, current_app


class DataManager():
    def __init__(self):
        config_class = os.getenv('FLASK_CONFIG', 'app.config.DevelopmentConfig')
        self.data_path = config_class.get('DATA_ROOT')

    # 数据导入
    def import_data(self):
        """
        从指定路径导入数据。
        当前逻辑暂时不实现，直接 pass。
        """
        pass

    # 数据检查
    def check_data_sync(self, db_benchmarks):
        """
        检查本地数据和数据库中的数据是否同步。
        :param db_benchmarks: 数据库中的 benchmark 数据（假设为字典形式）
        """
        local_benchmarks = self._load_local_benchmarks()

        # 比较本地和数据库数据
        discrepancies = []
        for local_id, local_data in local_benchmarks.items():
            if local_id not in db_benchmarks:
                discrepancies.append(f"Benchmark {local_id} 存在于本地，但不存在于数据库。")
            else:
                local_versions = set(local_data["versions"])
                db_versions = set(db_benchmarks[local_id]["versions"])
                if local_versions != db_versions:
                    discrepancies.append(
                        f"Benchmark {local_id} 的版本不同步：本地版本 {local_versions}，数据库版本 {db_versions}。"
                    )

        # 如果有差异，以本地数据为准同步数据库
        if discrepancies:
            print("发现以下差异，正在以本地数据为准同步数据库：")
            for discrepancy in discrepancies:
                print(discrepancy)
            self._sync_to_db(local_benchmarks)

    # 数据操作
    def operate_data(self, benchmark_id=None, version=None, operation=None, data=None):
        """
        对数据进行增删改查操作。
        :param benchmark_id: Benchmark 的 ID
        :param version: 具体版本
        :param operation: 操作类型，支持 'add', 'delete', 'update', 'read'
        :param data: 操作时需要提供的数据
        """
        local_benchmarks = self._load_local_benchmarks()

        if operation == "read":
            if benchmark_id and version:
                return self._read_version(benchmark_id, version)
            elif benchmark_id:
                return local_benchmarks.get(benchmark_id)
            else:
                return local_benchmarks
        elif operation == "add":
            self._add_data(benchmark_id, version, data)
        elif operation == "delete":
            self._delete_data(benchmark_id, version)
        elif operation == "update":
            self._update_data(benchmark_id, version, data)
        else:
            raise ValueError(f"未知操作类型：{operation}")

    # 私有方法：加载本地数据
    def _load_local_benchmarks(self):
        """从本地加载所有 Benchmark 的元数据"""
        local_benchmarks = {}
        if not self.data_path or not os.path.exists(self.data_path):
            raise FileNotFoundError(f"指定的数据路径 {self.data_path} 不存在。")

        for folder_name in os.listdir(self.data_path):
            folder_path = os.path.join(self.data_path, folder_name)
            if os.path.isdir(folder_path):
                metadata_path = os.path.join(folder_path, "metadata.json")
                if os.path.exists(metadata_path):
                    with open(metadata_path, "r", encoding="utf-8") as f:
                        metadata = json.load(f)
                    local_benchmarks[metadata["id"]] = {
                        "name": metadata["name"],
                        "versions": [v["version"] for v in metadata["versions"]],
                        "path": folder_path,
                        "data_type": metadata["class"]
                    }
        return local_benchmarks

    # 私有方法：同步到数据库
    def _sync_to_db(self, local_benchmarks):
        """将本地数据同步到数据库（当前仅输出模拟操作）"""
        print("正在将以下数据同步到数据库：")
        for benchmark_id, data in local_benchmarks.items():
            print(f"Benchmark ID: {benchmark_id}, 数据路径: {data['path']}, 版本: {data['versions']}")

    # 私有方法：读取特定版本
    def _read_version(self, benchmark_id, version):
        """读取指定 Benchmark 和版本的数据"""
        benchmark_path = os.path.join(self.data_path, benchmark_id)
        version_path = os.path.join(benchmark_path, f"{version}.json")
        if not os.path.exists(version_path):
            raise FileNotFoundError(f"版本 {version} 的数据文件不存在：{version_path}")
        with open(version_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # 私有方法：添加数据
    def _add_data(self, benchmark_id, version, data):
        """添加新数据"""
        benchmark_path = os.path.join(self.data_path, benchmark_id)
        os.makedirs(benchmark_path, exist_ok=True)
        version_path = os.path.join(benchmark_path, f"{version}.json")
        with open(version_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"添加数据成功：{version_path}")

    # 私有方法：删除数据
    def _delete_data(self, benchmark_id, version=None):
        """删除指定 Benchmark 或版本的数据"""
        benchmark_path = os.path.join(self.data_path, benchmark_id)
        if version:
            version_path = os.path.join(benchmark_path, f"{version}.json")
            if os.path.exists(version_path):
                os.remove(version_path)
                print(f"已删除版本 {version} 的数据文件：{version_path}")
        else:
            if os.path.exists(benchmark_path):
                for file in os.listdir(benchmark_path):
                    file_path = os.path.join(benchmark_path, file)
                    os.remove(file_path)
                os.rmdir(benchmark_path)
                print(f"已删除 Benchmark 数据：{benchmark_path}")

    # 私有方法：更新数据
    def _update_data(self, benchmark_id, version, data):
        """更新指定版本的数据"""
        self._add_data(benchmark_id, version, data)  # 直接覆盖保存
        print(f"更新数据成功：Benchmark ID: {benchmark_id}, Version: {version}")
