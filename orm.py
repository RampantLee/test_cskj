from sqlalchemy import *
from sqlalchemy.orm import *
import pymysql
pymysql.install_as_MySQLdb()

database_setting = {
    'database_type': 'mysql',
    'connector': 'pymysql',
    'username': 'root',
    'password': '03151994lzqq',
    'host_name': 'localhost',
    'database_name': 'UserManager'
}

class User(object):
    def __init__(self, user_name, user_age, user_sex, user_score,user_subject):
        self.user_name = user_name
        self.user_age = user_age
        self.user_sex = user_sex
        self.user_score = user_score
        self.user_subject = user_subject


class UserManagerORM(object):
    def __init__(self):

        # engine = create_engine("mysql://scott:tiger@hostname/dbname",
        #                             encoding='latin1', echo=True)
        # echo标识用于设置通过python标准日志模块完成的SQLAlchemy日志系统，当开启日志功能，我们将能看到所有的SQL生成代码
        self.engine = create_engine(
            database_setting['database_type'] +
            "+" +
            database_setting['connector'] +
            "://" +
            database_setting['username'] +
            ":" +
            database_setting['password'] +
            "@" +
            database_setting['host_name'] +
            "/" +
            database_setting['database_name'], encoding='utf-8', echo=True
        )
        # 设置metadata并将其绑定到数据库引擎
        self.metadata = MetaData(self.engine)

        # 定义关联的表
        self.user_table = Table('user', self.metadata, autoload=True)

        # 创建map映射对象，与定义的类相关联
        mapper(User, self.user_table)

        # 创建一个会话类型
        self.Session = sessionmaker()

        # 将连接引擎注册给这个会话
        self.Session.configure(bind=self.engine)

        # 得到具体的包含连接引擎的会话
        self.session = self.Session()


    def CreateNewUser(self, user_info):
        new_user = User(
            user_info['user_name'],
            user_info['user_age'],
            user_info['user_sex'],
            user_info['user_score'],
            user_info['user_subject']

        )
        self.session.add(new_user)
        self.session.commit()

    def GetUserByName(self, user_name):
        return self.session.query(User).filter_by(user_name=user_name).all()[0]

    def GetAllUser(self):
        return self.session.query(User)

    def UpdateUserInfoByName(self, user_info):
        user_name = user_info['user_name']
        user_info_without_name = {'user_age': user_info['user_age'],
                                'user_sex': user_info['user_sex'],
                                'user_score': user_info['user_score'],
                                'user_subject': user_info['user_subject']
                                }
        self.session.query(User).filter_by(user_name=user_name).update(user_info_without_name)
        self.session.commit()

    def DeleteUserByName(self, user_name):
        user_need_to_delete = self.session.query(User).filter_by(user_name=user_name).all()[0]
        self.session.delete(user_need_to_delete)
        self.session.commit()


















