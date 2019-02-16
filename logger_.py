#!/usr/bin/env python
# encoding: utf-8

import time
import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
import re
 
class Log(object):
      '''日志类 '''
      def __init__(self, name, filename):
            self.filename = filename
            self.name = name    # 为%(name)s赋值
            self.logger = logging.getLogger(self.name)
            # 控制日志文件中记录级别
            self.logger.setLevel(logging.INFO)
            # 控制输出到控制台日志格式、级别
            # self.ch = logging.StreamHandler()
            self.thandler = TimedRotatingFileHandler(self.filename, when='D', interval=1, backupCount=5, )
            self.thandler.suffix = '%Y-%m-%d_%H-%M-%S.log'
            self.thandler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}.log$")
            # 定义日志文件中格式
            self.formatter = logging.Formatter('%(asctime)s %(name)s [line:%(lineno)d] %(levelname)s %(message)s')
            self.thandler.setFormatter(self.formatter)
            self.logger.addHandler(self.thandler)
            # self.logger.addHandler(self.ch)

      def info(self, msg):
          self.logger.info(msg)
          print msg

      def warning(self, msg):
          self.logger.warning(msg)
          print msg

      def error(self, msg):
          self.logger.error(msg)
          print msg

      def debug(self, msg):
          self.logger.debug(msg)
          print msg

      def close(self):
          self.logger.removeHandler(self.fh)

if __name__ == '__main__':
	a = Log('myapp1','log/watcher.log')
	while True:
		time.sleep(0.5)
		a.info('Test')