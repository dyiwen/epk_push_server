#!-*-coding:utf8-*-

import re
from datetime import datetime, date, timedelta

def re_job(xx,source):
	rex = re.compile(xx)
	result = rex.findall(source)
	return result


def string_toDatetime(st):
	#print("把字符串转成datetime: ", datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S"))
	return datetime.strptime(st, "%Y-%m-%d %H:%M:%S")

def Yesterdate_():
	yesterday = date.today() + timedelta(days = -1)
	return str(yesterday)

if __name__ == '__main__':
	print(Yesterdate_())
