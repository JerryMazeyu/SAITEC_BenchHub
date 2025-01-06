import os
import json
from datetime import datetime
from app.models.testcase import Testcase, Version
from app.utils import move_file, generate_id
from flask import request, jsonify, current_app
from app.extensions import db
import hashlib


class DataManager():
    def __init__(self):
        try:
            self.data_path = current_app.config.get('DATA_ROOT')
            self.trash_path = current_app.config.get('TRASH_ROOT')
        except:
            pass

    # 数据导入
    def import_data(self):
        """
        从指定路径导入数据。
        当前逻辑暂时不实现，直接 pass。
        """
        pass

    # 数据检查
    def sync(self):
        """
        同步本地数据和数据库中的数据，包括 Testcase 的 meta 字段和 Version 的信息。
        """
        # 加载本地数据
        local_benchmarks = self._load_local_benchmarks()

        for local_id, local_data in local_benchmarks.items():
            # 同步 Testcase 的 meta 数据
            self._sync_meta_to_db(local_id, local_data)

            # 同步 Version 数据
            self._sync_versions_to_db(local_id, local_data["versions"], local_data)

        print("所有数据同步完成。")

    def get_testcases(self, filters=None, page=-1, page_size=10):
        """
        根据筛选条件获取 Testcase 列表，包括版本数据。
        :param filters: 查询条件（字典形式）
        :return: 满足条件的 Testcase 列表及版本数据
        """
        try:
            query = Testcase.query

            # 如果提供了筛选条件，逐个应用过滤
            if filters:
                for field, value in filters.items():
                    if hasattr(Testcase, field):
                        query = query.filter(getattr(Testcase, field) == value)

            if page != -1:
                # 查询总数（用于分页信息）
                total_count = query.count()

                # 分页查询
                testcases = query.paginate(page=page, per_page=page_size, error_out=False).items
            else:
                
                # 查询数据库
                testcases = query.all()
                total_count = len(testcases)

            # 构造响应数据
            results = {}
            data = {}
            for testcase in testcases:
                # 加载 meta.json 数据
                id = testcase.id
                meta_path = os.path.join(testcase.path, "meta.json")
                meta_data = {}
                if os.path.exists(meta_path):
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta_data = json.load(f)
                
                # 加载每个版本的数据
                versions = {}
                for version in testcase.versions:
                    version_path = os.path.join(testcase.path, f"{version.version}.json")
                    if os.path.exists(version_path):
                        with open(version_path, "r", encoding="utf-8") as f:
                            version_data = json.load(f)
                        
                        # 从版本文件中加载 meta 字段并与 meta.json 合并
                        version_meta = version_data.get("meta", {})
                        combined_meta = {**meta_data, **version_meta}  # meta 字段优先
                        
                        versions[version.version] = {
                            "data_content": version_data.get("data_content", {}),
                            "meta": combined_meta,
                        }
                data[id] = versions
            results["data"] = data
            results["total_count"] = total_count
            results["page"] = page
            results["page_size"] = page_size
            return results

        except Exception as e:
            raise RuntimeError(f"获取 Testcase 数据失败: {str(e)}")

    def soft_delete_version(self, testcase_id, version=None):
        """
        对某个版本或所有版本进行软删除，将其移动到 trash 文件夹，并更新数据库。
        如果所有版本都被删除，则 Testcase 和 meta.json 也会同步删除。
        :param testcase_id: Testcase 的 ID
        :param version: 要删除的版本号，如果为 None 则删除所有版本
        """
        testcase_path = os.path.join(self.data_path, testcase_id)
        trash_testcase_path = os.path.join(self.trash_path, testcase_id)
        
        if not os.path.exists(testcase_path):
            print(f"测试用例 {testcase_path} 不存在，无需删除。")
            # 仅删除指定版本的数据库记录
            self._sync_deleted_versions_to_db(testcase_id, version)
        
        else:
            # 确保 trash 文件夹存在
            os.makedirs(trash_testcase_path, exist_ok=True)

            # 获取所有版本文件
            if version:
                versions_to_delete = [f"{version}.json"]
            else:
                versions_to_delete = [file for file in os.listdir(testcase_path) if file.endswith(".json") and file != "meta.json"]
            
            # 删除本地版本文件并移动到 trash
            for version_file in versions_to_delete:
                source_path = os.path.join(testcase_path, version_file)
                if not os.path.exists(source_path):
                    print(f"版本文件 {source_path} 不存在，跳过删除。")
                    continue

                # 移动文件到 trash 文件夹
                dest_path = os.path.join(trash_testcase_path, version_file)
                move_file(source_path, dest_path)
                print(f"已将版本文件 {version_file} 移动到 {dest_path}。")

            # 如果所有版本都被删除，删除 meta.json 和 Testcase
            remaining_versions = [file for file in os.listdir(testcase_path) if file.endswith(".json") and file != "meta.json"]
            if not remaining_versions:
                # 移动 meta.json 到 trash 文件夹
                meta_path = os.path.join(testcase_path, "meta.json")
                if os.path.exists(meta_path):
                    trash_meta_path = os.path.join(trash_testcase_path, "meta.json")
                    move_file(meta_path, trash_meta_path)
                    print(f"已将 meta.json 移动到 {trash_meta_path}。")

                # 删除本地 Testcase 目录
                os.rmdir(testcase_path)
                print(f"已删除 Testcase 目录 {testcase_path}。")

            # 同步删除数据库中的 Testcase 和其所有版本
            self._sync_deleted_testcase_to_db(testcase_id)
            
    def soft_modify_version(self, testcase_id, version, modifications):
        """
        对某个版本进行软修改，将原文件移动到 backup 文件夹，并保存修改后的新文件。
        同时更新数据库中的版本记录。
        :param testcase_id: Testcase 的 ID
        :param version: 要修改的版本号
        :param modifications: 修改内容（字典形式）
        """
        testcase_path = os.path.join(self.data_path, testcase_id)
        backup_path = os.path.join(self.trash_path, testcase_id)

        # 确保路径存在
        os.makedirs(backup_path, exist_ok=True)

        # 检查版本文件是否存在
        version_path = os.path.join(testcase_path, f"{version}.json")
        if not os.path.exists(version_path):
            raise FileNotFoundError(f"版本文件 {version_path} 不存在，无法修改。")

        # 移动原版本文件到 backup 文件夹
        backup_version_path = os.path.join(backup_path, f"{version}.json")
        move_file(version_path, backup_version_path)
        print(f"已将原始版本 {version} 移动到 {backup_version_path}。")

        # 加载原文件数据
        with open(backup_version_path, "r", encoding="utf-8") as f:
            original_data = json.load(f)

        # 合并修改内容
        modified_data = {**original_data, **modifications}

        # 保存修改后的文件
        with open(version_path, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, indent=4, ensure_ascii=False)
        print(f"已将修改后的版本 {version} 保存到 {version_path}。")

        # 同步数据库
        self._sync_modified_version_to_db(testcase_id, version, modifications)

    def add_testcase(self, folder_path):
        """
        增加新的 Testcase。
        :param folder_path: 包含 meta.json 和至少一个版本文件（如 v1.json）的文件夹路径。
        """
        try:
            # 检查文件夹是否存在
            if not os.path.exists(folder_path):
                raise FileNotFoundError(f"指定的文件夹 {folder_path} 不存在。")

            # 检查 meta.json 和 v1.json 是否存在
            meta_path = os.path.join(folder_path, "meta.json")
            version_path = os.path.join(folder_path, "v1.json")
            if not os.path.exists(meta_path) or not os.path.exists(version_path):
                raise ValueError("meta.json 和 v1.json 文件必须存在。")

            # 加载 meta.json 和 v1.json 的内容
            with open(meta_path, "r", encoding="utf-8") as f:
                meta_data = json.load(f)

            with open(version_path, "r", encoding="utf-8") as f:
                version_data = json.load(f)

            # 检查并补全 meta.json 的字段
            required_meta_fields = [
                "data_resource", "data_type", "data_dimension",
                "description", "uploader", "answer_mode", "created_at"
            ]
            for field in required_meta_fields:
                if field not in meta_data:
                    meta_data[field] = ""

            # 为 created_at 提供默认值
            if not meta_data["created_at"]:
                meta_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            

            if "data_content" not in version_data:
                raise ValueError("v1.json 必须包含 data_content 字段。")

            # 将 meta.json 和 v1.json 的内容进行字符串拼接
            combined_content = json.dumps(meta_data, sort_keys=True) + json.dumps(version_data, sort_keys=True)

            # 生成 MD5 作为 ID
            testcase_id = hashlib.md5(combined_content.encode("utf-8")).hexdigest()

            # 检查数据库中是否已存在
            if Testcase.query.get(testcase_id):
                raise ValueError(f"Testcase {testcase_id} 已存在，无法重复添加。")

            # 复制文件夹到 data 目录下
            dest_path = os.path.join(self.data_path, testcase_id)
            os.makedirs(dest_path, exist_ok=True)

            meta_dest_file = os.path.join(dest_path, "meta.json")
            
            with open(meta_dest_file, "w", encoding="utf-8") as dest:
                json.dump(meta_data, dest, ensure_ascii=False, indent=4)
            
            v1_dest_file = os.path.join(dest_path, "v1.json")
            with open(v1_dest_file, "w", encoding="utf-8") as dest:
                json.dump(version_data, dest, ensure_ascii=False, indent=4)

            print(f"文件夹 {folder_path} 已复制到 {dest_path}。")

            # 同步到数据库
            testcase = Testcase(
                id=testcase_id,
                description=meta_data.get("description", ""),
                data_resource=meta_data.get("data_resource", ""),
                data_type=meta_data["data_type"],
                data_dimension=meta_data["data_dimension"],
                path=dest_path,
                created_at=datetime.strptime(meta_data["created_at"], "%Y-%m-%d %H:%M:%S"),
                uploader=meta_data.get("uploader", "")
            )
            db.session.add(testcase)

            version = Version(
                testcase_id=testcase_id,
                version="v1",
                update_time=datetime.now(),
                transform_method=version_data.get("meta", {}).get("transform_method", ""),
                data_type=meta_data["data_type"],
                data_dimension=meta_data["data_dimension"]
            )
            db.session.add(version)

            db.session.commit()
            print(f"Testcase {testcase_id} 已成功添加到数据库。")
            return {"id": testcase_id}

        except Exception as e:
            raise RuntimeError(f"添加 Testcase 时出错: {str(e)}")

    def _sync_modified_version_to_db(self, testcase_id, version, modifications):
        """
        同步修改的版本到数据库。
        :param testcase_id: Testcase 的 ID
        :param version: 要修改的版本号
        :param modifications: 修改内容（字典形式）
        """
        db_version = Version.query.filter_by(testcase_id=testcase_id, version=version).first()

        if not db_version:
            raise ValueError(f"数据库中未找到版本 {version}，无法同步修改。")

        # 更新数据库字段
        if "meta" in modifications:
            db_version.data_type = modifications["meta"].get("data_type", db_version.data_type)
            db_version.data_dimension = modifications["meta"].get("data_dimension", db_version.data_dimension)

        # 更新更新时间
        db_version.update_time = datetime.utcnow()

        # 提交数据库更改
        db.session.commit()
        print(f"数据库已同步修改后的版本 {version}。")


    def _sync_deleted_versions_to_db(self, testcase_id, version=None):
        """
        同步删除的版本到数据库，标记为已删除。
        :param testcase_id: Testcase 的 ID
        :param version: 要删除的版本号，如果为 None 则删除所有版本
        """
        if version:
            # 删除特定版本
            db_version = Version.query.filter_by(testcase_id=testcase_id, version=version).first()
            if db_version:
                db.session.delete(db_version)
                print(f"数据库已删除版本 {version}。")
        else:
            # 删除所有版本
            db_versions = Version.query.filter_by(testcase_id=testcase_id).all()
            for db_version in db_versions:
                db.session.delete(db_version)
                print(f"数据库已删除版本 {db_version.version}。")

        # 提交更改
        db.session.commit()
        print(f"数据库已同步删除操作：Testcase {testcase_id}。")


    def _sync_deleted_testcase_to_db(self, testcase_id):
        """
        删除数据库中的 Testcase 及其所有关联版本。
        :param testcase_id: Testcase 的 ID
        """
        # 删除 Testcase
        db_testcase = Testcase.query.get(testcase_id)
        if db_testcase:
            db.session.delete(db_testcase)
            print(f"数据库已删除 Testcase {testcase_id} 及其所有版本。")

        # 删除所有关联的版本
        db_versions = Version.query.filter_by(testcase_id=testcase_id).all()
        for db_version in db_versions:
            db.session.delete(db_version)

        # 提交更改
        db.session.commit()
        print(f"数据库已同步删除操作：Testcase {testcase_id} 和所有关联版本。")

    def _load_local_benchmarks(self):
        """
        从本地加载所有 Benchmark 的元数据。
        """
        local_benchmarks = {}
        if not self.data_path or not os.path.exists(self.data_path):
            raise FileNotFoundError(f"指定的数据路径 {self.data_path} 不存在。")

        for folder_name in os.listdir(self.data_path):
            folder_path = os.path.join(self.data_path, folder_name)
            if os.path.isdir(folder_path):
                metadata_path = os.path.join(folder_path, "meta.json")
                
                # 检查是否存在 meta.json
                if not os.path.exists(metadata_path):
                    print(f"跳过：未找到 meta.json 文件：{metadata_path}")
                    continue

                # 加载 meta.json 数据
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)

                # 提取版本信息
                versions = []
                for file_name in os.listdir(folder_path):
                    if file_name.endswith(".json") and file_name != "meta.json":
                        version_name = os.path.splitext(file_name)[0]  # 提取文件名作为版本号
                        versions.append(version_name)

                # 构建本地 Benchmark 数据结构
                local_benchmarks[folder_name] = {
                    "id": folder_name,
                    "data_resource": metadata.get("data_resource", ""),
                    "data_type": metadata.get("data_type", ""),
                    "data_dimension": metadata.get("data_dimension", ""),
                    "description": metadata.get("description", ""),
                    "uploader": metadata.get("uploader", ""),
                    "answer_mode": metadata.get("answer_mode", ""),
                    "created_at": metadata.get("created_at", ""),
                    "versions": sorted(versions),  # 按字典序排序版本
                    "path": folder_path,  # 本地路径
                }

        return local_benchmarks
    
    def _sync_versions_to_db(self, testcase_id, local_versions, local_data):
        """
        同步本地版本信息到数据库中的 Version 表，并合并 meta.json 和版本文件中的 meta 数据。
        :param testcase_id: Testcase 的 ID
        :param local_versions: 本地版本集合
        :param local_data: 本地 Benchmark 数据，用于补充 data_type 和 data_dimension
        """
        # 加载 meta.json
        meta_path = os.path.join(local_data["path"], "meta.json")
        meta_data = {}
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta_data = json.load(f)

        # 从数据库加载现有版本
        db_versions = {v.version: v for v in Version.query.filter_by(testcase_id=testcase_id).all()}

        # 遍历本地版本
        for version in local_versions:
            version_path = os.path.join(local_data["path"], f"{version}.json")
            if not os.path.exists(version_path):
                print(f"跳过：未找到本地版本文件 {version_path}")
                continue

            # 加载版本文件
            with open(version_path, "r", encoding="utf-8") as f:
                version_data = json.load(f)

            # 从版本文件中加载 meta 字段，并与 meta.json 合并
            version_meta = version_data.get("meta", {})
            combined_meta = {**meta_data, **version_meta}

            # 提取必要字段
            data_type = combined_meta.get("data_type", "")
            data_dimension = combined_meta.get("data_dimension", "")
            transform_method = combined_meta.get("transform_method", "")

            # 如果版本不存在于数据库，创建新版本
            if version not in db_versions:
                new_version = Version(
                    testcase_id=testcase_id,
                    version=version,
                    update_time=datetime.utcnow(),
                    transform_method=transform_method,
                    data_type=data_type,
                    data_dimension=data_dimension,
                )
                db.session.add(new_version)
                print(f"添加版本 {version} 到数据库。")
            else:
                # 更新已存在版本的 meta 信息
                db_version = db_versions[version]
                db_version.data_type = data_type
                db_version.data_dimension = data_dimension
                db_version.transform_method = transform_method

        # 删除数据库中多余的版本
        for version in db_versions.keys():
            if version not in local_versions:
                db.session.delete(db_versions[version])
                print(f"删除数据库中多余的版本 {version}。")

        # 提交更改
        db.session.commit()
        print(f"同步 Testcase {testcase_id} 的版本数据完成。")

    def _sync_meta_to_db(self, testcase_id, local_data):
        """
        同步本地 meta 数据到数据库中的 Testcase 表。
        :param testcase_id: Testcase 的 ID
        :param local_data: 本地 Benchmark 数据
        """
        meta_path = os.path.join(local_data["path"], "meta.json")
        meta_data = {}

        # 加载 meta.json
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta_data = json.load(f)

        # 更新或创建 Testcase
        testcase = Testcase.query.get(testcase_id)
        if not testcase:
            testcase = Testcase(id=testcase_id)
            db.session.add(testcase)

        # 更新字段
        testcase.description = meta_data.get("description", local_data.get("description", ""))
        testcase.data_resource = meta_data.get("data_resource", local_data["data_resource"])
        testcase.data_type = meta_data.get("data_type", local_data["data_type"])
        testcase.data_dimension = meta_data.get("data_dimension", local_data["data_dimension"])
        testcase.path = local_data["path"]
        testcase.created_at = (
            datetime.strptime(meta_data["created_at"], "%Y-%m-%d %H:%M:%S")
            if "created_at" in meta_data
            else datetime.now()
        )
        testcase.uploader = meta_data.get("uploader", "System")

        # 提交更改
        db.session.commit()
        print(f"同步 Testcase {testcase_id} 的 meta 数据完成。")

    def _import_data_v1(self, source_path:str, target_path:str=None) -> None:
        if not target_path:
            target_path = self.data_path
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"源路径不存在：{source_path}")
        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
        
        # 遍历源路径中的所有文件夹
        for folder_name in os.listdir(source_path):
            folder_path = os.path.join(source_path, folder_name)
            if os.path.isdir(folder_path):
                original_json_path = os.path.join(folder_path, f"{folder_name}.json")
                if not os.path.exists(original_json_path):
                    print(f"跳过：未找到同名 JSON 文件：{original_json_path}")
                    continue

                # 加载原始 JSON 数据
                with open(original_json_path, "r", encoding="utf-8") as f:
                    original_data = json.load(f)

                # 构建目标文件夹路径
                target_folder_path = os.path.join(target_path, folder_name)
                os.makedirs(target_folder_path, exist_ok=True)

                # 创建 meta.json
                meta_data = self._create_meta_json(original_data)
                meta_path = os.path.join(target_folder_path, "meta.json")
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(meta_data, f, indent=4, ensure_ascii=False)

                # 创建 v1.json
                v1_data = self._create_v1_json(original_data)
                v1_path = os.path.join(target_folder_path, "v1.json")
                with open(v1_path, "w", encoding="utf-8") as f:
                    json.dump(v1_data, f, indent=4, ensure_ascii=False)

                print(f"迁移完成：{folder_name}")
    
    def _create_meta_json(self, original_data):
        """
        从原始数据生成 meta.json。
        :param original_data: 原始 JSON 数据
        :return: meta.json 数据
        """
        metadata = original_data.get("metadata", {})
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "data_resource": metadata.get("resource", ""),
            "data_type": metadata.get("data_type", ""),
            "data_dimension": metadata.get("test_dimension", ""),
            "description": metadata.get("data_note", ""),
            "uploader": metadata.get("uploader", "Administrator"),
            "answer_mode": metadata.get("answer_mode", ""),
            "created_at": created_at,
        }
    
    def _create_v1_json(self, original_data):
        """
        从原始数据生成 v1.json。
        :param original_data: 原始 JSON 数据
        :return: v1.json 数据
        """
        data_content = original_data.get("data_content", {})
        return {"data_content": data_content}
    

if __name__ == '__main__':
    dm = DataManager()
    dm._import_data_v1(r'D:\GreatLibrarianFrontend\Backend\App\data\data_save', r'C:\Users\H3C\WorkSpace\SAITEC_BenchHub\assets\data')
