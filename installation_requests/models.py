"""Models."""

import datetime
import enum

from sqlalchemy import Column, DateTime, DECIMAL, Enum, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base


class RequestStatusEnum(enum.Enum):
    """RequestStatusEnum."""

    NEW = "NEW"
    PENDING = "PENDING"
    CLOSED = "CLOSED"
    CANCELED = "CANCELED"


class Base(object):
    """Base."""

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )


DeclarativeBase = declarative_base(cls=Base)


class InstallationRequest(DeclarativeBase):
    """InstallationRequest."""

    __tablename__ = "installation_requests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    status = Column(Enum(RequestStatusEnum), nullable=False)
    budget = Column(DECIMAL(18, 2), nullable=False)
    equipment_type = Column(String, nullable=False)
    equipment_brand = Column(String)
    equipment_model = Column(String)
    comment = Column(Text)
