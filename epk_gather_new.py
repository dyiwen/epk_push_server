#!-*-coding:utf8-*-

import os
import datetime
import time
from tools import re_job, string_toDatetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers




def tran_json(init_list,index_):
	actions = []
	for line in init_list:
		# print line
		line = line.decode('utf8')
		result = re_job(r'(.*?)\s\[(.*?)\]\s(\w+)\s([\s\S]+)',line)
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
	print actions
	print len(actions)
	#////////////////////////////////////////////////////////////
	helpers.bulk(client=es,actions=actions,raise_on_error=True,request_timeout=30)
	# for ok,response in helpers.streaming_bulk(es,actions):
	# 	if not ok:
	# 		print(response)
	print '发送完毕'
	#///////////////////////////////////////////////////////////



def init_list(name_,path_):
	# i = 1
	for file_ in os.listdir(path_):
		print file_
		index_ = re_job(r'tqlh(.*?).20',file_)[0]
		print name_+index_
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
				result = re_job(xx,line)
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
			print match_y+match_n
			print len(match_y+match_n)
			tran_json(match_y+match_n,name_ + index_)
			break



if __name__ == '__main__':
	es=Elasticsearch(hosts='39.108.223.105',port=9200)
	init_list("tqlh","/home/dyiwen/workspace/elasticsearch/python-es/logs")