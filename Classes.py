import datetime
from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, Column
from base import Base

class Paste(Base):
    __tablename__ = 'pastebin_paste'

    def __init__(self):
        self.time_of_detection = datetime.datetime.now()
        self.downloaded = False

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String)
    language = Column(String)
    content = Column(String)