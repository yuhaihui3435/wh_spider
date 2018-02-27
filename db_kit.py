from sqlalchemy import Column, create_engine, Integer, String, TEXT, distinct,func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://ab:*(&^%$)(*&^%$%*KJU@39.106.213.166:43333/wh_bx',pool_size=100, pool_recycle=3600, )
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
    reg_name = Column(String(255))

class INOCC(Base):
    __tablename__='b_insurance_occ'

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    pCode = Column(String(20))
    code = Column(String(20))
    name = Column(String(100))
    insurance = Column(String(100))



def insert(obj):
    session = DBSession()
    session.add(obj)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()


def findOnByUrl(url, type):
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    ret = session.query(Insurer).filter(Insurer.url == url, Insurer.ty).first()
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


def findMFOnByUrl(url, tpe):
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    ret = session.query(Mf).filter(Mf.url == url,
                                   # Mf.type==tpe
                                   ).first()
    # 关闭Session:
    session.close()
    return ret

def existCheck(code,insurance):
    session = DBSession()
    ret=session.query(INOCC).filter(INOCC.code==code,INOCC.insurance==insurance).all()

    return 'yes' if len(ret)>0 else 'no'



def findAll(model, val):
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    ret = session.query(model).filter(model.catalog == val).all()
    # 关闭Session:
    session.close()
    return ret


def findMfAll():
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    ret = session.query(Mf.phone, Mf.zip_code, Mf.ads, Mf.scope, Mf.expiry_date, Mf.mng_unit, Mf.reg_num, Mf.tel,
                        Mf.legal, Mf.reg_org, Mf.reg_time, Mf.reg_name, func.count(distinct(Mf.url))).group_by(Mf.url).filter().all()
    # 关闭Session:
    session.close()
    return ret
