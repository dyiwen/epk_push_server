#!-*-coding:utf8-*-
import random
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import datetime
import time
import json
import os
import re

es=Elasticsearch(hosts='',port=)
#-----------------------------------------------------------------------------------------------
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
	del_result = es.delete_by_query(index=index_, body=query, doc_type='doc')
	print del_result

def delete_index(index_):   #删除标签
	cmd = "curl -XDELETE 'http://172.16.0.23:9200/{}'".format(index_)
	print os.popen(cmd).read()

def index_action():
    es.index(index="my-index", doc_type="doc", id=42, body={"any": "data", "timestamp": datetime.datetime.now()})
#-----------------------------------------------------------------------------------------------

def tran_json(init_list,index_):
	actions = []
	for line in init_list:
		# print line
		line = line.decode('utf8')
		result = re_find(r'(.*?)\s\[(.*?)\]\s(\w+)\s([\s\S]+)',line)
		# print result
		time_ = string_toDatetime(result[0][0][:-4]) + datetime.timedelta(hours=-8)
		action = {'_op_type':'index',
		'_index':index_,
		'_type':'doc',
		# '_id':i,
		'_source':{
		u'日期':time_,
		u'对象':result[0][1],
		u'请求':result[0][2],
		'message':line
		},
		'fields':{
		"@timestamp":[time_]}}
		# i += 1
		actions.append(action)
	# print actions
	print len(actions)
	#////////////////////////////////////////////////////////////
	helpers.bulk(client=es,actions=actions,raise_on_error=True,request_timeout=30)
	# for ok,response in helpers.streaming_bulk(es,actions):
	# 	if not ok:
	# 		print(response)
	print '发送完毕'
	#///////////////////////////////////////////////////////////


def init_list(path_):
	# i = 1
	for file_ in os.listdir(path_):
		print file_
		index_ = re_find(r'(.*?).2018',file_)[0]
		with open(os.path.join(path_,file_)) as f:
			match_y = []
			match_n = []
			# print type(f)
			f = list(f)
			# print list(f)
			# time.sleep(5)
			line_str = ""
			line_list = []
			for line in f:
				# print line.decode('utf8')
				# line = line.decode('utf8')
				xx = r"^\d{4}-\d{2}-\d{2}\s"
				result = re_find(xx,line)
				num_result, num_str, num_list = len(result), len(line_str), len(line_list)
				if num_result <> 0 and num_str == 0:
					line_list.append(line)
					match_y.append(line)
				elif num_result == 0 and num_list <> 0 and num_str == 0:
					line_str = line_list[-1] + line
					if line_list[-1] in match_y:
						match_y.remove(line_list[-1])
					line_list = []
					# print line_list[-1]
					# break
				elif num_result == 0 and num_list == 0 and num_str <> 0:
					line_str += line
				elif num_result <> 0 and num_str <> 0 and num_list == 0:
					match_y.append(line)
					if line_str not in match_n:
						match_n.append(line_str)
					line_str = ''
					line_list.append(line) 
			print '报错',len(match_n)
			print "*"*50
			# print len(match_y)
			# print "-"*50
			# for j in match_n:
			# 	print j
			# 	print '-'*50
		tran_json(match_y+match_n,index_)
		time.sleep(5)

if __name__ == '__main__':
	init_list('/home/dyiwen/workspace/elasticsearch/python-es/logs')
