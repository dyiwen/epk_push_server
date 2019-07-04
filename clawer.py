#!-*-coding:utf8-*-

import os
import datetime
import time
import re
import subprocess
import socket
from tools import re_job, string_toDatetime
# from elasticsearch import Elasticsearch
# from elasticsearch import helpers


class ESearch(object):
	"""docstring for ClassName"""
	def __init__(self, host,port,index):
		self.es = Elasticsearch(host,port)
		self.index_ = index
		self.myaddr = socket.gethostbyname(myname)
		self.myname = socket.getfqdn(socket.gethostname())


	def post_(self,actions):
		helpers.bulk(client=self.es,actions=actions,raise_on_error=True,request_timeout=30)



	def format_(self,init_list,index_):
		actions = []
		for line in init_list:
			# print line
			line = line.decode('utf8')
			xx = r'(.*?)\s+(\w+\s\d+)\s---\s\[(.*?)\]\s(.*)\s([\d\D]*)'
			result = re_job(xx,line)
			# print result
			time_ = string_toDatetime(result[0][0][:-4]) + datetime.timedelta(hours=-8)
			action = {'_op_type':'index',
			'_index':index_,
			'_type':'doc',
			# '_id':i,
			'_source':{
			u'日期':time_,
			u'等级':result[0][1],
			u'线程名称':result[0][2],
			u'服务器主机名':myname,
			u"服务器ip":myaddr,
			'message':line
			},
			'fields':{
			"@timestamp":[time_]}}
			# i += 1
			actions.append(action)
		#print actions
		#print len(actions)
		#////////////////////////////////////////////////////////////
		return actions
		# helpers.bulk(client=self.es,actions=actions,raise_on_error=True,request_timeout=30)






	def main(self,file_path,time_out=10):
		# with open(file_path) as f:
			# for line in f:
				# print(line)
		p = subprocess.Popen('tail -f {}'.format(file_path), shell=True,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE,)


		n = 0
		match_y = []
		match_n = []
		line_list = []
		time_list = []

		while 1:
			line = p.stdout.readline()
			now = time.time()
			
			if line:
				time_list = []
				n += 1

				# xx = r'(.*?)\s+(\w+\s\d+)\s---\s\[(.*?)\]\s(.*)\s([\d\D]*)'
				xx = r"^\d{4}-\d{2}-\d{2}\s"
				result = re_job(xx,line)
				print(result)
				print('-'*70)
				num_result, num_str, num_list = len(result), len(line_list)
				if all([num_result!=0,num_list==0]):
					match_y.append(line)
					line_list.append(line)
				elif all([num_result!=0,num_list==1]):
					match_y.append(line)
					line_list = []
					line_list.append(line)
				elif all([num_result!=0,num_list>1]):
					match_y.append(line)
					match_n.append(''.join(line_list))
					line_list = []
				elif all([num_result==0,num_list!=1]):
					line_list.append(line)
				elif all([num_result==0,num_list==1]):
					line_list.append(line)
					match_y.pop()

			else:
				time.sleep(0.5)
				time_list.append(now)

			if time_list[-1] - time_list[0] > time_out:
				actions = self.format_(match_y+match_n,self.index_)
				sel.post_(actions)
				
				n = 0
				match_y = []
				match_n = []
				line_list = []




		



def read(file_path):
	with open(file_path,encoding='UTF-8') as f:
		n = 0
		match_y = []
		match_n = []
		line_str = ""
		line_list = []
		for line in f:
			# f = list(f)
			# print(f)
			n += 1
			print(line)
			xx = r'(.*?)\s\s(\w+\s\d+)\s---\s\[(.*?)\]\s(.*)'
			# xx = r"^\d{4}-\d{2}-\d{2}\s"
			result = re_job(xx,line)
			print(result)
			if len(result) != 0:
				print(string_toDatetime(result[0][0][:-4]) + datetime.timedelta(hours=-8))
			print('-'*70)
			num_result, num_str, num_list = len(result), len(line_str), len(line_list)
			if all([num_result!=0,num_str==0]):
				line_list.append(line)
				match_y.append(line)
			elif all([num_result==0,num_list!=0,num_str==0]):
				line_str = line_list[-1] + line
				if line_list[-1] in match_y:
					match_y.remove(line_list[-1])
				line_list = []
			elif all([num_result==0,num_list==0,num_str!=0]):
				line_str += line
			elif all([num_result!=0,num_str!=0,num_list==0]):
				match_y.append(line)
				if line_str not in match_n:
					match_n.append(line_str)
				line_str = ''
				line_list.append(line)
			if n == 1000:
				break
		print(match_n) 
		print('-'*10)
		print(len(match_n))
		print(match_n[3])


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
		u'服务器主机名':myname,
		u"服务器ip":myaddr,
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




def test(time_out=10):
	print(time_out)
	# a = ['5','4','3','2','1']
	# a.pop()
	# b = a.append('1')
	# print(a)
	# b = []
	# while 1:
	# 	a = time.time()
	# 	b.append(a)
		# time.sleep(2)
		# c = time.time()
		# print(b)
		# b.append(c)
		# print(b[0],b[-1])
		# print(b[-1]-b[0]>1)
		# if b[-1]-b[0]>5:
		# 	print(b[-1],b[0])
		# 	break
		# if b[-1] - b[0] > 5:
			# break


def read2(file_path):
	with open(file_path,encoding='UTF-8') as f:
		n = 0
		match_y = []
		match_n = []
		line_str = ""
		line_list = []
		for line in f:
			# f = list(f)
			# print(f)
			n += 1
			print(line)
			# xx = r'(.*?)\s\s(\w+\s\d+)\s---\s\[(.*?)\]\s(.*)'
			xx = r'(.*?)\s+(\w+\s\d+)\s---\s\[(.*?)\]\s(.*)\s([\d\D]*)'
			# xx = r"^\d{4}-\d{2}-\d{2}\s"
			result = re_job(xx,line)
			print(result)
			# break
			num_result, num_str, num_list = len(result), len(line_str), len(line_list)
			if all([num_result!=0,num_list==0]):
				match_y.append(line)
				line_list.append(line)
			elif all([num_result!=0,num_list==1]):
				match_y.append(line)
				line_list = []
				line_list.append(line)
			elif all([num_result!=0,num_list>1]):
				match_y.append(line)
				match_n.append(''.join(line_list))
				line_list = []
			elif all([num_result==0,num_list!=1]):
				line_list.append(line)
			elif all([num_result==0,num_list==1]):
				line_list.append(line)
				match_y.pop()

			if n >= 1000:
				break 

		# print(match_n)
		# print('-'*50)
		# print(len(match_n))
		# print(match_n[1])
		# result = re_job(xx,match_n[2])
		# print(result)
				
			




if __name__ == '__main__':
	# test()
	# main()
	# read('D:\\代码\\日志解析\\nohup.out')
	read2('D:\\代码\\日志解析\\nohup.out')
	# print(time.time())
	# print(type(time.time()))