# -*- coding: utf-8 -*-
import os
import sys
import shutil
import importlib
from zipfile import ZipFile
from distutils.sysconfig import get_python_lib

import xlsconfig

DEPENDENCIES = {
	"xlrd" : "xlrd-master.zip",
	"xlwt" : "xlwt-master.zip",
	"openpyxl" : "openpyxl-2.4.4.zip",
}

def check_plugin():
	plugins = ("openpyxl", )
	need_restart = False
	for name in plugins:
		try:
			importlib.import_module(name)
		except ImportError, e:
			print "错误：没有发现插件：'%s'，尝试自动安装 ..." % (name, )

			ret = install(name)
			print "-" * 60
			print "安装插件%s： '%s'" % ("成功" if ret else "失败", name, )

			if not ret: return False

			need_restart = True

	if need_restart: print "请重启导表工具"
	return True

def install(name):
	path = DEPENDENCIES.get(name)
	if path is None:
		print "错误：没有找到安装包：'%s'" % (name, )
		return

	output_path = xlsconfig.TEMP_PATH

	setup_path = os.path.join(output_path, os.path.splitext(path)[0])
	if os.path.exists(setup_path):
		shutil.rmtree(setup_path, True)

	path = os.path.join(xlsconfig.DEPENDENCY_PATH, path)
	with ZipFile(path, "r") as zf:
		zf.extractall(output_path)

	if not os.path.exists(os.path.join(setup_path, "setup.py")):
		print "错误：没有找到安装文件：'%s/setup.py'" % setup_path
		return False

	old_cwd = os.getcwd()
	os.chdir(setup_path)
	try:
		_install_in_path()
	except:
		os.chdir(old_cwd)
		traceback.print_exc()
		return False

	os.chdir(old_cwd)

	for fname in os.listdir(get_python_lib()):
		if fname.startswith(name):
			return True

	return False

def _install_in_path():
	print os.getcwd()

	cmd = """python setup.py build > build.log"""
	os.system(cmd)

	cmd = """python setup.py install > install.log"""
	sudo(cmd)

def sudo(cmd):
	if sys.platform != "win32":
		cmd = "sudo " + cmd

	#print cmd
	os.system(cmd)
