#!-*-coding:utf8-*-
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import datetime
import time
import json
import os
import re

es=Elasticsearch(hosts='172.16.0.23',port=9200)
#-------------------------------------------------------------------------------------------
def string_toDatetime(st):
	#print("把字符串转成datetime: ", datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S"))
	return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")

def re_find(xx,source_):
	rex = re.compile(xx)
	result = rex.findall(source_)
	return result

def delete_action(index_):   #清空index下所有日志
	query = {'query': {'match_all': {}}}
	# allDoc = es.search(index='log_level', doc_type='doc', body=query)
	del_result = es.delete_by_query(index=index_, body=query, doc_type='doc', request_timeout = 30)
	print del_result

def delete_index(index_):   #删除标签
	cmd = "curl -XDELETE 'http://172.16.0.23:9200/{}'".format(index_)
	print os.popen(cmd).read()
#-------------------------------------------------------------------------------------------
if __name__ == '__main__':
	delete_action('tqlh_web')