import configparser
import logging
import os
import sys

from sqlalchemy import URL,create_engine

logger = logging.getLogger(__name__)

class ConfigInfo:

    def __init__(self, cfgfilename):
        """

        :param cfgfilename:
        """
        self.filename = cfgfilename
        print('运行参数：', sys.argv)
        for arg in sys.argv:
            if arg.startswith('--config'):
                self.filename = arg.split('=')[1]
        configfile = os.path.abspath(self.filename)
        config = configparser.ConfigParser()
        if os.path.exists(configfile):
            config.read(configfile, encoding='utf-8')
        else:
            print(f"配置文件 {configfile} 未找到")
            raise FileNotFoundError(configfile)

        print(type(config))
        self.config = config


    def create_db_engine(self):
        __db_user = self.config['db']['user']
        __db_pass = self.config['db']['pass']
        __db_host = self.config['db']['host']
        __db_port = self.config['db']['port']
        __db_database_name = self.config['db']['database_name']
        dburl = URL.create('mysql+pymysql', username=__db_user, password=__db_pass, host=__db_host,
                           database=__db_database_name, port=__db_port, query={"charset": 'utf8'})
        logger.warning('%s %s', type(dburl), dburl)
        xmdb_engine = create_engine(dburl)
        return xmdb_engine