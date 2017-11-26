from sqlalchemy import Column, create_engine, Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:111111@localhost:3306/wh_spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

class Insurer(Base):
    # 表的名字:
    __tablename__ = 'insurer'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    orgName = Column(String(255))
    orgType = Column(String(50))
    orgAddress = Column(String(255))
    cat = Column(String(50))
    tel = Column(String(100))
    leader = Column(String(100))
    capital = Column(String(100))
    registerAddress = Column(String(255))
    state = Column(String(100))
    catalog = Column(String(100))
    url = Column(String(255))


def insert(insurer):
    session=DBSession()
    session.add(insurer)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

def findOnByUrl(url):
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    ret = session.query(Insurer).filter(Insurer.url == url).first()
    # 关闭Session:
    session.close()
    return ret

def update(insurer):
    session = DBSession()
    session.merge(insurer)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()