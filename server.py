from bottle import route, get,post, run, template, static_file, request, FileUpload
import os
from importlib.machinery import SourceFileLoader
from serverutil import log
import waitress
from settings import getSettings
import time
import cutter

@get("/<pth:path>")
def static(pth):
	log("Static file requested: " + pth)
	return static_file(pth,root="")


@get("")
@get("/")
def mainpage():
	keys = request.query
	log("Requesting main page")
	return SourceFileLoader("mainpage","mainpage.py").load_module().GET(keys)

@get("/xhttp")
def xhttp():
	keys = request.query
	log("XHTTP Request")
	return cutter.GET(keys)

@post("/upload")
def upload():
	try:
		keys = request.query
		filename = keys.get("name")
		filename = cutter.cleanfilename(filename)
		cut_from, cut_to = keys.get("cutfrom"), keys.get("cutto")
		filetype = filename.split(".")[-1]
		if filetype not in ["mkv","mp4","avi"]: return "ERROR_FILETYPE"
		FileUpload(request.body,name=None,filename=None).save("queue/" + filename)
		return cutter.add(filename,start=cut_from,end=cut_to)
	except:
		return "ERROR_GENERIC"


port = getSettings("SERVER_PORT")[0]

run(host='::', port=port, server='waitress')
