from flask import jsonify, current_app, request
from app.services.benchmarks import DataManager
from app.models.testcase import Testcase, Version
from app.extensions import cache
from . import benchmarks_bp


@benchmarks_bp.route('/sync', methods=['POST'])
def sync_data():
    """
    同步本地数据和数据库数据的接口。
    """
    try:
        # 初始化 DataManager
        data_manager = DataManager()

        
        data_manager.sync()

        return jsonify({"success": True, "message": "数据同步完成"}), 200

    except Exception as e:
        current_app.logger.error(f"[benchmarks] Sync error: {e}")
        # 捕获异常并返回错误信息
        return jsonify({"success": False, "message": str(e)}), 500

@benchmarks_bp.route('/testcases', methods=['GET'])
def get_testcases():
    """
    获取 Testcase 列表及其版本数据，根据条件筛选。
    """
    try:
        # 获取查询参数
        filters = {
            key: request.args.get(key)
            for key in ['id', 'data_resource', 'data_dimension', 'description']
            if request.args.get(key) is not None
        }
        page = int(request.args.get('page', -1))  # 获取页码
        page_size = int(request.args.get('page_size', 10))  # 获取每页大小

        # 使用 DataManager 获取数据
        data_manager = DataManager()
        testcases_with_versions = data_manager.get_testcases(filters, page=page, page_size=page_size)

        return jsonify({"success": True, "data": testcases_with_versions}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@benchmarks_bp.route('/testcases/<string:id>/<string:version>', methods=['POST'])
def modify_version(id, version):
    """
    对某个 Testcase 的版本进行软修改。
    :param id: Testcase 的 ID
    :param version: 要操作的版本号
    """
    try:
        # 获取请求中的数据
        data = request.json
        operation = data.get("operation")  # "modify"
        modifications = data.get("modifications")  # 修改内容

        if operation != "modify":
            return jsonify({"success": False, "message": "Invalid operation. Must be 'modify'."}), 400

        if not modifications:
            return jsonify({"success": False, "message": "Modifications data is required for modify operation."}), 400

        # 使用 DataManager 完成操作
        data_manager = DataManager()
        data_manager.soft_modify_version(id, version, modifications)

        return jsonify({"success": True, "message": f"Version {version} modified for Testcase {id}."}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@benchmarks_bp.route('/testcases/<string:id>', methods=['DELETE'])
def delete_version(id):
    """
    对某个 Testcase 的版本进行软删除。
    :param id: Testcase 的 ID
    """
    try:
        # 获取请求参数
        version = request.args.get('version')  # 要删除的版本号，为 None 则删除所有版本

        # 使用 DataManager 完成删除操作
        data_manager = DataManager()
        data_manager.soft_delete_version(testcase_id=id, version=version)

        if version:
            message = f"Version {version} deleted for Testcase {id}."
        else:
            message = f"All versions deleted for Testcase {id}."

        return jsonify({"success": True, "message": message}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@benchmarks_bp.route('/testcases', methods=['POST'])
def add_testcase():
    """
    新增 Testcase 接口。
    请求体中需要提供一个文件夹路径，包含 meta.json 和至少一个版本文件（如 v1.json）。
    """
    try:
        # 获取请求体中的文件夹路径
        data = request.json
        folder_path = data.get('folder_path')

        if not folder_path:
            return jsonify({"success": False, "message": "folder_path is required"}), 400

        # 调用 DataManager 的方法
        data_manager = DataManager()
        res = data_manager.add_testcase(folder_path)
        res["folder_path"] = folder_path
        
        return jsonify({"success": True, "data": res}), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@benchmarks_bp.route('/dimensions', methods=['GET'])
def get_unique_dimensions():
    """
    获取所有唯一的 data_dimension 值，支持缓存。
    """
    cache_key = "unique_data_dimensions"
    
    # 从缓存中获取结果
    dimensions = cache.get(cache_key)
    if dimensions is not None:
        current_app.logger.info("从缓存中获取 unique data_dimensions")
        return jsonify({"success": True, "data": dimensions}), 200

    # 如果缓存不存在，从数据库查询
    current_app.logger.info("从数据库查询 unique data_dimensions")
    try:
        dimensions = list(set(version.data_dimension for version in Version.query.all()))
        cache.set(cache_key, dimensions)  # 缓存结果
        return jsonify({"success": True, "data": dimensions}), 200
    except Exception as e:
        current_app.logger.error(f"获取 unique data_dimensions 失败: {e}")
        return jsonify({"success": False, "message": str(e)}), 500