
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
import json
import time

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Enum,
    DECIMAL,
    DateTime,
    Boolean,
    UniqueConstraint,
    PrimaryKeyConstraint,
    Index
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(
    "mysql+pymysql://root:root@127.0.0.1:3306/jiuquan_warehouse?charset=utf8mb4",
    # "mysql+pymysql://tom@127.0.0.1:3306/db1?charset=utf8mb4", # 无密码时
    # 超过链接池大小外最多创建的链接
    max_overflow=0,
    # 链接池大小
    pool_size=5,
    # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
    pool_timeout=10,
    # 多久之后对链接池中的链接进行一次回收
    pool_recycle=1,
    # 查看原生语句（未格式化）
    echo=True
)

# 绑定引擎
Session = sessionmaker(bind=engine)
# 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# 内部会采用threading.local进行隔离
session = scoped_session(Session)

class Metrics(Base):
    # 数据库中存储的表名
    __tablename__ = "dim_metrics"
    metrics_id = Column(Integer,name = 'metrics_id' , primary_key=True, autoincrement=True, comment='指标id')
    metricsx_class_id = Column(String(64), primary_key=True, autoincrement=True, comment='指标分类编码')
    metricsx_class_code = Column(String(64), primary_key=True, autoincrement=True, comment='指标分类编码')
    metricsx_class_name = Column(String(64), primary_key=True, autoincrement=True, comment='指标分类编码')
    metrics_code = Column(String(64), primary_key=True, autoincrement=True, comment='指标分类编码')
    metrics_name = Column(String(64), primary_key=True, autoincrement=True, comment='指标分类编码')
    metrics_unit = Column(String(64), primary_key=True, autoincrement=True, comment='指标分类编码')
    
    def __str__(self):
        return f"object : <metrics_id:{self.metrics_id} metricsx_class_name:{self.metricsx_class_name}>"

class DwsMsEnterpriseMetricsMonth(Base):
    __tablename__ = 'dws_ms_enterprise_metrics_month'
    region_id = Column(String(64), comment='指标分类编码')
    month_id = Column(Integer, comment='月份ID')
    metrics_id = Column(String(64), comment='指标ID')
    ytm_value = Column(DECIMAL(28,8) , comment='本年累计值')
    last_ytm_value = Column(DECIMAL(28,8) , comment='本年累计值')
    ytm_ybr = Column(DECIMAL(28,8) , comment='本年累计值')
    #PrimaryKeyConstraint('region_id', 'month_id', 'metrics_id')
    
    __table_args__ = (
         PrimaryKeyConstraint('region_id', 'month_id', 'metrics_id'),
         {}
     )
    
    def __str__(self):
        return f"object : <region_id:{self.region_id} month_id:{self.month_id} metrics_id:{self.metrics_id}>"

# 融资信息表
class FactEnterpriseFinancingQuarter(Base):
    __tablename__ = 'fact_enterprise_financing_quarter'
    
    enterprise_id = Column(String(64))
    financing_date = Column(String(64))
    product_name = Column(String(64))
    financing_schedule = Column(String(64))
    valuation_amount = Column(String(64))
    financing_amount = Column(String(64))
    investment_institution = Column(String(64))
    
    __table_args__ = (
        PrimaryKeyConstraint('enterprise_id','financing_date','product_name'),
        {}
    )
    
    def __str__(self):
        return f"object : <enterprise_id:{self.enterprise_id} financing_date:{self.financing_date} product_name:{self.product_name}>"

def readJsonData(fileName):
    #fileName = 'cookies.json'
    with open(fileName, encoding='utf-8') as a:
        cookies = json.load(a)
        return cookies


if __name__ == "__main__":
    
    region_id = '620900000000'
    month_id = 202306
    jiuquan_data_dict = { '市场主体数量' : 286424 , '个体工商户数量' : '209369' , '企业数量':63329 , '创新型中小企业数量' : 108 }
    jiuquan_metrics_mapping_dict = dict()
    
    # 省级专精特新数量  ,  市级专精特新数量   ,   专精特新小巨人      DirectoryName、ApproveClassDesc
    honorData = readJsonData('honor_data.json')
    province_count = 0
    city_count = 0
    little_giant = 0
    for index,value in enumerate(honorData):
        level_str = value.get('ApproveClassDesc')
        directory_name = value.get('DirectoryName')
        if level_str == '省级':
            province_count += 1
        if level_str == '市级':
            city_count += 1
        if directory_name == '专精特新“小巨人“企业':
            little_giant += 1
    
    print("省级专精特新数量 : " + str(province_count))
    print("市级专精特新数量 : " + str(city_count))
    print("专精特新小巨人: " + str(little_giant))
    jiuquan_data_dict['省级专精特新数量'] = province_count
    jiuquan_data_dict['市级专精特新数量'] = city_count
    jiuquan_data_dict['专精特新小巨人'] = little_giant
    
    all_result =  session.query(Metrics).all()
    for row in all_result:
        jiuquan_metrics_mapping_dict[row.metrics_name] = row.metrics_id
    
    all_jiuquan_data_dict = []
    for key,value in jiuquan_data_dict.items():
        obj = DwsMsEnterpriseMetricsMonth(
            region_id=region_id,
            month_id=month_id,
            metrics_id=jiuquan_metrics_mapping_dict[key],
            ytm_value=value,
            last_ytm_value=0.0,
            ytm_ybr=0.0
        )
        all_jiuquan_data_dict.append(obj)
    print('----   分割线  ----')
    #session.add_all(all_jiuquan_data_dict)
    #session.commit()
    
    finanacing_data = readJsonData('financing_data.json')
    finanacing_data_list = []
    for index,value in enumerate(finanacing_data):
        #strTime = value.get('Date').strftime("%Y-%m-%d")
        strTime = time.strftime("%Y/%m/%d", time.localtime(value.get('Date')))

        financing_obj = FactEnterpriseFinancingQuarter(
            enterprise_id = value.get('CreditCode'),
            financing_date = strTime,
            product_name = value.get('ProductName'),
            financing_schedule = value.get('Round'),
            valuation_amount = value.get('Valuation'),
            financing_amount = value.get('Amount'),
            investment_institution = value.get('Investment')
        )
        finanacing_data_list.append(financing_obj)
    session.add_all(finanacing_data_list)
    session.commit()