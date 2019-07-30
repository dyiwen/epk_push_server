#!-*-coding:utf8-*-

import re
import docker
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


def docker_info():
        client = docker.from_env()
        container_names = [i.attrs['Name'].lstrip('/')  for i in client.containers.list()]
        for i in client.containers.list():
                print i.attrs
        print container_names



if __name__ == '__main__':
        docker_info()
