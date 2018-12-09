#!-*-coding:utf8-*-
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime
import time
import json
import os
import re

es=Elasticsearch(hosts='39.108.223.105',port=9200)

def re_find(xx,source_):
	rex = re.compile(xx)
	result = rex.findall(source_)
	return result

def string_toDatetime(st):
	#print("把字符串转成datetime: ", datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S"))
	return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")

def get_target_file(path_):             #strptime
	date_now = datetime.strftime(datetime.now(), "%Y-%m-%d")
	# print date_now
	# print type(date_now)
	name_list = ['tqlh_web.%s'%date_now,'tqlh_web.warn.%s'%date_now,'tqlh_web.error.%s'%date_now]
	root_list = os.listdir(path_)
	target_file_list = [os.path.join(path_,j) for j in root_list for k in name_list if k in j]
	# print target_file_list
	return target_file_list
#'/home/dyiwen/workspace/elasticsearch/python-es/logs'
def update_info(path_): 
	dict = {}
	target_file_list = get_target_file(path_)
	for i in target_file_list:
		file_time = os.stat(i).st_mtime
		with open(i) as f:
			f.seek(0,2)
			row_num = f.tell()
		dict[i] = [file_time,row_num]
	return dict

def tran_json(init_list,index_):
	actions = []
	for line in init_list:
		# print line
		line = line.decode('utf8')
		result = re_find(r'(.*?)\s\[(.*?)\]\s(\w+)\s([\s\S]+)',line)
		# print result
		time_ = string_toDatetime(result[0][0][:-4])
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
	for ok,response in helpers.streaming_bulk(es,actions):
		if not ok:
			print(response)
	print '发送完毕'
	#///////////////////////////////////////////////////////////

def init_list(update_list,index_):
	match_y = []
	match_n = []
	line_str = ""
	line_list = []
	for line in update_list:
		xx = r"^\d{4}-\d{2}-\d{2}\s"
		result = re_find(xx, line)
		num_result, num_str, num_list = len(result), len(line_str), len(line_list)
		if num_result <> 0 and num_str == 0:
			line_list.append(line)
			match_y.append(line)
		elif num_result == 0 and num_list <> 0 and num_str == 0:
			line_str = line_list[-1] + line
		elif num_result <> 0 and num_str <> 0 and num_list == 0:
			match_y.append(line)
			match_n.append(line_str)
			line_str = ''
			line_list.append(line)
	print '报错',len(match_n)
	tran_json(match_y+match_n,index_)


#{file_name:[time,seek_num]}
def main(path_):
	update_dict = update_info(path_)
	while True:
		# time.sleep(3)
		current_dict = update_info(path_)
		for key_ in current_dict.keys():
			index_ = re_find(r'(.*?).2018',os.path.split(key_)[-1])[0]
			if current_dict[key_][0] != update_dict[key_][0]:
				with open(key_) as f:
					f.seek(int(update_dict[key_][1]),1)
					data = f.readlines()
					init_list(data,index_)
					print data
					print len(data),type(data),f.tell()
					row_num = f.tell()
					update_dict[key_] = [current_dict[key_][0],row_num]
			else:
				pass

if __name__ == '__main__':
	main('/home/dyiwen/workspace/elasticsearch/python-es/logs')