#!-*-coding:utf8-*-

import os

root = "/home/dyiwen/workspace/elasticsearch/python-es/logs"

files_ = [i for roots, dirs, files in os.walk(root) for i in files if "tqlh" in i]
# for roots, dirs, files in os.walk(root):
	# print files
print files_