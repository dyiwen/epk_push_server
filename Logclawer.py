#!/usr/bin/env python
# encoding: utf-8

from multiprocessing import cpu_count,Process,JoinableQueue
from clawer import ESearch
from logger_ import err,warn,out
from dict_ import container_info
import traceback
import datetime
import time


class MutilServer(object):
	"""docstring for MutilServer"""
	def __init__(self):
		self.q = JoinableQueue()
		self.es = ESearch('172.18.204.170',9200)
		# self.input_list = input_list


	def Pushlog(self,item):
		try:
			startime = time.time()
			#out('开始收集 {} 的日志'.format(item))
			self.es.main(item,container_info[item])
			elapsed = (time.time() - startime)
			out('单次任务耗时 {}'.format(round(elapsed/60,2)))
		except:
			err('{} 日志收集接口报错'.format(item))
			err(traceback.format_exc())


	def Worker(self,i):
		while True:
			item = self.q.get()
			if item is None:
				break
			self.Pushlog(item)
			self.q.task_done()
			out("队列剩余 {} 个任务".format(str(self.q.qsize())))


	def Runner(self,input_list):
		try:
			startime = time.time()
			cpuCount = 3
			multiprocessing = []
			out("主服务开始运行...")

			for i in xrange(0,cpuCount):
				p = Process(target=self.Worker,args=(self.q,))
				p.daemon = True
				p.start()
				out("进程{}启动....".format(i))
				multiprocessing.append(p)

			for i in range(len(input_list)):
				self.q.put(input_list[i])
			self.q.join()

			for i in xrange(0,cpuCount):
				self.q.put(None)
			for p in multiprocessing:
				p.join()

			elapsed = (time.time() - startime)
			out("cpuCount: {} Finished with time:{}minutes".format(cpuCount, round(elapsed/60,2)))
		except:
			err(traceback.format_exc())



#get_out_id,get_in_num,monthlist
if __name__ == '__main__':
	input_list = container_info.keys()
	# es = ESearch('172.18.204.170',9200)
	MutilServer().Runner(input_list)
