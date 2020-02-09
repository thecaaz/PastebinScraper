import datetime
from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, Column
from base import Base

class Paste(Base):
    __tablename__ = 'pastebin_paste'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String)
    language = Column(String)
    content = Column(String)
    href = Column(String)