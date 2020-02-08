# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.ConfigParser()
config.read('login.config')

engine = create_engine('mysql://%s:%s@%s:3306/%s' % (
    config['SQL']['user'],
    config['SQL']['pass'],
    config['SQL']['host'],
    config['SQL']['name']))

Session = sessionmaker(bind=engine)

Base = declarative_base()
