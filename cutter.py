import os
from threading import Thread
import subprocess

import globals


# unlike surselva, we don't keep tasks on disk here, just in memory!
videos = {}


QUEUEFOLDER = globals.user_folders['QUEUEFOLDER']
DONEFOLDER = globals.user_folders['DONEFOLDER']

#first startup, delete all leftover videofiles
for f in os.listdir(QUEUEFOLDER):
	os.remove(os.path.join(QUEUEFOLDER,f))
for f in os.listdir(DONEFOLDER):
	os.remove(os.path.join(DONEFOLDER,f))



def cleanfilename(filename):
	validchars = "'-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789. "
	filename = "".join(c for c in filename if c in validchars)
	while filename.count(".") > 1: filename.replace(".","",1)
	return filename

def diff(st,en):

	start = list(st)
	end = list(en)

	while len(start) != 1:
		start[1] += 60 * start[0]
		del start[0]
	while len(end) != 1:
		end[1] += 60 * end[0]
		del end[0]

	dif = [0]
	dif[0] = end[0] - start[0]

	while dif[0] > 59 and len(dif) < 3:
		dif.insert(0,dif[0])
		dif[0] = dif[1] // 60
		dif[1] = dif[1] % 60

	return dif


def add(name,start=None,end=None):
	global videos

	vidid = random.randint(1000000000,9999999999)
	name = cleanfilename(name)

	if start is not None:
		start = start.split("-")
		start = [int(t) for t in start]
	if end is not None:
		end = end.split("-")
		end = [int(t) for t in end]

	if name in videos: return "ERROR_EXISTS"

	vid = {"filename":name,"starttime":start,"endtime":end,"processed":0}
	videos[vidid] = vid
	t = Thread(target=cut,args=(vid,))
	t.start()
	return "SUCCESS"



def xhttp_handle(k):
	if k.get("list") is not None:
		return show_videos()
	if k.get("delete") is not None:
		vidid = k.get("delete")
		global videos
		vid = videos[vidid]
		os.remove(os.path.join(QUEUEFOLDER,vidid))
		os.remove(os.path.join(DONEFOLDER,vidid))
		del videos[vidid]



def cut(video):
	cmd = ["ffmpeg"]
	if video["starttime"] is not None:
		cmd += ["-ss",":".join([str(e) for e in video["starttime"]])]
	cmd += ["-i",os.path.join(QUEUEFOLDER,video['filename'])]
	if video["endtime"] is not None and video["starttime"] is None:
		cmd += ["-to",":".join([str(e) for e in video["endtime"]])]
	elif video["endtime"] is not None and video["starttime"] is not None:
		cmd += ["-t",":".join([str(e) for e in diff(video["starttime"],video["endtime"])])]
	cmd += ["-c","copy",os.path.join(QUEUEFOLDER,video['filename'])]

	print(cmd)
	subprocess.run(cmd)

	# right now we only have processed 0 and 100, but keeping this for
	# surselva uniformity
	video["processed"] = 100



def show_videos():
	template = globals.jinjaenv.get_template('videolist.html.jinja')
	return template.render(videos=videos)
