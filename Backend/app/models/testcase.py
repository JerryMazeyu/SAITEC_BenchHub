from app.extensions import db
from datetime import datetime

class Testcase(db.Model):
    __tablename__ = 'testcases'

    id = db.Column(db.String(32), primary_key=True)  # 与本地文件夹名一致
    description = db.Column(db.Text, nullable=True)  # Testcase 描述
    data_resource = db.Column(db.String(50), nullable=False)  # 数据来源
    data_type = db.Column(db.String(50), nullable=False)  # 数据类型（多模态、单模态）
    data_dimension = db.Column(db.String(50), nullable=False)  # 数据模式（常识、推理）
    path = db.Column(db.String(255), nullable=False)  # 本地存储根目录路径
    created_at = db.Column(db.DateTime, default=datetime.now())  # 创建时间

    # 关系
    versions = db.relationship('Version', back_populates='benchmark', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Testcase(id={self.id}, name={self.name}, data_type={self.data_type})>"


class Version(db.Model):
    __tablename__ = 'versions'

    id = db.Column(db.Integer, primary_key=True)  # 自增主键
    testcase_id = db.Column(db.String(32), db.ForeignKey('testcases.id'), nullable=False)  # 外键
    version = db.Column(db.String(20), nullable=False)  # 版本号，例如 `v1`, `v2`
    update_time = db.Column(db.DateTime, nullable=False)  # 版本更新时间
    transform_method = db.Column(db.Text, nullable=True)  # 变形方法描述
    data_type = db.Column(db.String(50), nullable=False)  # 数据类型（多模态、单模态）
    data_dimension = db.Column(db.String(50), nullable=False)  # 数据模式（常识、推理）

    # 关系
    testcases = db.relationship('Testcase', back_populates='versions')

    def __repr__(self):
        return f"<Version(testcase_id={self.testcase_id}, version={self.version})>"
