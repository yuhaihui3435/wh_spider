from sqlalchemy import Column, create_engine, Integer,String,TEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:e)st$$1se(r991er@123.56.24.132:53306/wh_spider')
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
class Mf(Base):
    # 表的名字:
    __tablename__ = 'mfw'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    type = Column(String(20))
    catalog = Column(String(50))
    reg_time = Column(String(50))
    reg_org = Column(String(100))
    reg_num = Column(String(50))
    legal = Column(String(50))
    mng_unit = Column(String(100))
    expiry_date = Column(String(50))
    scope = Column(TEXT)
    ads = Column(String(255))
    zip_code = Column(String(50))
    tel = Column(String(100))
    phone = Column(String(100))
    url = Column(String(255))
    reg_name=Column(String(255))

def insert(obj):
    session=DBSession()
    session.add(obj)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

def findOnByUrl(url,type):
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    ret = session.query(Insurer).filter(Insurer.url == url,Insurer.ty).first()
    # 关闭Session:
    session.close()
    return ret

def update(obj):
    session = DBSession()
    session.merge(obj)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()


def findMFOnByUrl(url,tpe):
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    ret = session.query(Mf).filter(Mf.url == url,Mf.type==tpe).first()
    # 关闭Session:
    session.close()
    return ret

def findAll(model,val):
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    ret = session.query(model).filter(model.catalog == val).all()
    # 关闭Session:
    session.close()
    return ret