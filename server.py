import os
import waitress
import time

from bottle import route, get,post, run, template, static_file, request, FileUpload

import cutter
import globals
from logger import log
from settings import get_settings

@get("/<pth:path>")
def static(pth):
	log("Static file requested: " + pth)
	return static_file(pth,root="")


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


port = get_settings()["SERVER_PORT"]

run(host='::', port=port, server='waitress')
