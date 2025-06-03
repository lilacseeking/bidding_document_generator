from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    content = Column(Text)
    file_path = Column(String(255))
    file_size = Column(Integer)
    file_type = Column(String(50))
    version = Column(String(20))
    status = Column(String(20))
    is_template = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))

    # 关系
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_documents")
    updater = relationship("User", foreign_keys=[updated_by], back_populates="updated_documents") 