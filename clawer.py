#!-*-coding:utf8-*-

import os
import datetime
import time
import re
import subprocess
import socket
import traceback
from tools import re_job, string_toDatetime, docker_info
from logger_ import out, err
from elasticsearch import Elasticsearch
from elasticsearch import helpers


class ESearch(object):
	"""docstring for ClassName"""
	def __init__(self, host,port):
		self.es = Elasticsearch(host=host,port=port)
		# self.index_ = index
		self.myname = socket.getfqdn(socket.gethostname())
		self.myaddr = socket.gethostbyname(self.myname)


	def post_(self,actions):
		helpers.bulk(client=self.es,actions=actions,raise_on_error=True,request_timeout=30)



	def format_(self,init_list,index_):
		actions = []
		for line in init_list:
			#print line
			line = line.decode('utf8')
			xx = r'(.*?)\s+(\w+\s\d+)\s---\s\[(.*?)\]\s(.*)\s([\d\D]*)'
			result = re_job(xx,line)
			#print result
			time_ = string_toDatetime(result[0][0][:-4]) + datetime.timedelta(hours=-8) 
			action = {'_op_type':'index',
			'_index':index_,
			'_type':'doc',
			# '_id':i,
			'_source':{
			u'日期':time_,
			u'等级':result[0][1],
			u'线程名称':result[0][2],
			u'服务器主机名':self.myname,
			u"服务器ip":self.myaddr,
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






	def main(self,container_name,index,time_out=10):
		# with open(file_path) as f:
			# for line in f:
				# print(line)
		while 1:
			container_list = docker_info()
			if container_name in container_list:
				out('开始收集容器 {} 的日志'.format(container_name))
				cmd = "docker logs -f --since='{}' {}".format(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'),container_name)
				p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)

				match_y = []
				match_n = []
				line_list = []

				while 1:
					line = p.stdout.readline()
					if line:
						# out('{}容器的日志{}'.format(container_name,line))

						# xx = r'(.*?)\s+(\w+\s\d+)\s---\s\[(.*?)\]\s(.*)\s([\d\D]*)'
						xx = r"^\d{4}-\d{2}-\d{2}\s"
						result = re_job(xx,line)
						#print(result)
						out('-'*70)
						num_result, num_list = len(result), len(line_list)
						if all([num_result!=0,num_list==0]):
							match_y.append(line)
							line_list.append(line)
						elif all([num_result!=0,num_list==1]):
							match_y.append(line)
							line_list = []
							line_list.append(line)
						elif all([num_result!=0,num_list>1]):
							match_y.append(line)
							actions = self.format_([''.join(line_list)],index)
							self.post_(actions)
							out('异常:容器{} 发送了 {} 条数据，到es'.format(container_name,len(actions)))
							line_list = []
							line_list.append(line)
						elif all([num_result==0,num_list==1]):
							if len(match_y) == 1:
								match_y.pop()
								line_list.append(line)
							if len(match_y) > 1:
								match_y.pop()
								actions = self.format_(match_y,index)
								self.post_(actions)
								out('正常:容器{} 发送了 {} 条数据，到es'.format(container_name,len(actions)))
								match_y = []
								line_list.append(line)
						elif all([num_result==0,num_list>1]):
							line_list.append(line)
					else:
						container_list = docker_info()
						if container_name not in container_list:
							out('发现 {} 服务关闭，等待重启服务'.format(container_name))
							break
						else:
							pass

			else:
				time.sleep(1)










if __name__ == '__main__':
        a = ESearch('172.18.204.170',9200,'qc_back_prod_1')
        a.main('c29f82edf11f',4)
