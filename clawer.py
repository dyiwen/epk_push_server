#!-*-coding:utf8-*-

import os
import datetime
import time
import re
import subprocess
import socket
import traceback
from tools import re_job, string_toDatetime
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
			search_result = os.popen("docker ps -a | grep '{}' | awk {'print $13'}".format(container_name)).read()
			if container_name in search_result:
				p = subprocess.Popen("docker logs -f --since='2019-07-08' {}".format(container_name), shell=True,
					stdout=subprocess.PIPE,stderr=subprocess.PIPE,)

				n = 0
				match_y = []
				match_n = []
				line_list = []
				time_list = []

				while 1:
					line = p.stdout.readline()
					if line:
						# out('{}容器的日志{}'.format(container_name,line))
						n += 1

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
							out("#"*60)
							out('容器{} 发送了 {} 条数据，到es'.format(container_name,len(actions)))
							out("#"*60)
							line_list = []
						elif all([num_result==0,num_list==1]):
							if len(match_y) == 1:
								actions = self.format_(match_y,index)
								self.post_(actions)
								out("#"*60)
								out('容器{} 发送了 {} 条数据，到es'.format(container_name,len(actions)))
								out("#"*60)
								match_y = []
							elif len(match_y) > 1:
								match_y.pop()
								actions = self.format_(match_y,index)
								self.post_(actions)
								out("#"*60)
								out('容器{} 发送了 {} 条数据，到es'.format(container_name,len(actions)))
								out("#"*60)
								match_y = []
								line_list.append(line)
							elif all([num_result==0,num_list>1]):
								line_list.append(line)
					else:
						if 'Exited' in os.popen("docker ps -a | grep '{}'|awk {'print $9'}".format(container_name)).read():
							break
			else:
				time.sleep(5)










if __name__ == '__main__':
        a = ESearch('172.18.204.170',9200,'qc_back_prod_1')
        a.main('c29f82edf11f',4)
