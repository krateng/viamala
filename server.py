import os
import waitress
import time
import sys
import random

from bottle import route, get, post, run, static_file, request, FileUpload

import globals
import cutter
from logger import log
from settings import get_settings

@get("/videos/<filename>")
def video(filename):
	log("Video file requested: " + filename)
	return static_file(filename,root=os.path.join(globals.data_dir,"done"))
@get("/backgrounds/<filename>")
def backgrounds(filename):
	return static_file(filename,root=os.path.join(globals.data_dir,"backgrounds"))

@get("/<pth:path>")
def static(pth):
	return static_file(pth,root="./static")


@get("")
@get("/")
def mainpage():
	page_template = globals.jinjaenv.get_template('page.html.jinja')
	log("Requesting main page")
	localisation = get_settings()['localisation']
	try:
		background = random.choice(os.listdir(globals.user_folders['BACKGROUNDFOLDER']))
	except:
		background = ''
	return page_template.render({
		'localisation':localisation,
		#'localisation_json':json.dumps(localisation),
		'background':background
	})

@route("/xhttp")
def xhttp():
	keys = request.query
	log("XHTTP Request")
	return cutter.xhttp_handle(keys)

@post("/upload")
def upload():
	try:
		keys = request.query
		filename = keys.get("name")
		filename = cutter.cleanfilename(filename)
		cut_from, cut_to = keys.get("cutfrom"), keys.get("cutto")
		filetype = filename.split(".")[-1]
		if filetype not in ["mkv","mp4","avi"]: return "ERROR_FILETYPE"
		FileUpload(request.body,name=None,filename=None).save(os.path.join(globals.user_folders['QUEUEFOLDER'],filename))
		return cutter.add(filename,start=cut_from,end=cut_to)
	except:
		raise
		return "ERROR_GENERIC"

host = "0.0.0.0" if "--ipv4" in sys.argv else "::"
port = get_settings()['server']['PORT']

run(host=host, port=port, server='waitress')
