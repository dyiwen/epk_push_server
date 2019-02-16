#!-*-coding:utf8-*-

import os
import datetime
import time
from logger_ import Log
from config_ import log_path, log_yard
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
		myname = socket.getfqdn(socket.gethostname())
		myaddr = socket.gethostbyname(myname)
		action = {'_op_type':'index',
		'_index':index_,
		'_type':'doc',
		# '_id':i,
		'_source':{
		u'日期':time_,
		u'对象':result[0][1],
		u'请求':result[0][2],
		u'本机用户':myname,
		u"本机ip":myaddr,
		'message':line
		},
		'fields':{
		"@timestamp":[time_]}}
		# i += 1
		actions.append(action)
	#print actions
	#print len(actions)
	#////////////////////////////////////////////////////////////
	helpers.bulk(client=es,actions=actions,raise_on_error=True,request_timeout=30)
	# for ok,response in helpers.streaming_bulk(es,actions):
	# 	if not ok:
	# 		print(response)
	#print '发送完毕'
	#///////////////////////////////////////////////////////////



def init_list(path_):
	# i = 1
	log_ = Log("log",'log/watcher.log')
	file_info_list = [(i,os.path.join(roots,i)) for roots, dirs, files in os.walk(path_) for i in files if "tqlh" in i]
	# print file_info_list
	for items_ in file_info_list:
		file_ = items_[0]
		index_ = re_job(r'tqlh(.*?).20',file_)[0]
		index_ = log_yard()+index_
		with open(items_[1]) as f:
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
			# time.sleep(5)
			#print match_y+match_n
			time.sleep(5)
			tran_json(match_y+match_n,index_)
			log_.info("发送成功,error {} 条,info {} 条,共 {} 条".format(len(match_y),len(match_n),len(match_y+match_n)))
			# time.sleep(5)



# if __name__ == '__main__':
# 	es=Elasticsearch(hosts='39.108.223.105',port=9200)
# 	init_list(log_path())