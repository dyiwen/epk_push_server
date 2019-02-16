#!-*-coding:utf8-*-

import ConfigParser
import os

cf = ConfigParser.ConfigParser()
cf.read("./server.conf")


def log_yard():
	return cf.get("LOG","environment")


def log_path():
	return cf.get("LOG","log_path")