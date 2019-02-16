#!-*-coding:utf8-*-

import re
import datetime

def re_job(xx,source):
	rex = re.compile(xx)
	result = rex.findall(source)
	return result


def string_toDatetime(st):
	#print("把字符串转成datetime: ", datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S"))
	return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")
