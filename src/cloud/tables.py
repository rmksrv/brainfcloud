import sqlalchemy
from sqlalchemy.ext import declarative

import cloud.schemas
import cloud.constants


Base = declarative.declarative_base()


class BvmInstance(Base):
    __tablename__ = "bvm_instances"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    state = sqlalchemy.Column(sqlalchemy.Enum(cloud.schemas.BvmState), nullable=False)
    stored_at = sqlalchemy.Column(sqlalchemy.String(cloud.constants.BVM_STORAGE_MAX_PATH_LENGTH))
