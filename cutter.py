import os
from collections import namedtuple
from threading import Thread

videos = []


#first startup, delete all leftover videofiles

for f in os.listdir("queue/"):
	if f != ".gitignore" and f!= "dummy": os.remove("queue/" + f)
for f in os.listdir("done/"):
	if f != ".gitignore" and f!= "dummy": os.remove("done/" + f)



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

	name = cleanfilename(name)

	if start is not None:
		start = start.split("-")
		start = [int(t) for t in start]
	if end is not None:
		end = end.split("-")
		end = [int(t) for t in end]

	if name in videos: return "ERROR_EXISTS"

	vid = {"file":name,"starttime":start,"endtime":end,"percentage":0}
	videos.append(vid)
	t = Thread(target=cut,args=(vid,))
	t.start()
	return "SUCCESS"



def GET(k):
	if k.get("list") is not None:
		return videolist()
	if k.get("delete") is not None:
		name = k.get("delete")
		global videos
		for v in videos:
			if v["file"] == name:
				os.remove("./done/" + name)
				os.remove("./queue/" + name)
				videos.remove(v)
				break



def cut(video):
	global videos
	cmd = "ffmpeg"
	if video["starttime"] is not None:
		cmd += " -ss " + ":".join([str(e) for e in video["starttime"]])
	cmd += " -i './queue/" + video["file"] + "'"
	if video["endtime"] is not None and video["starttime"] is None:
		cmd += " -to " + ":".join([str(e) for e in video["endtime"]])
	elif video["endtime"] is not None and video["starttime"] is not None:
		cmd += " -t " + ":".join([str(e) for e in diff(video["starttime"],video["endtime"])])
	cmd += " -c copy"
	cmd += " './done/" + video["file"] + "'"

	os.system(cmd)
	print(cmd)

	video["percentage"] = 100





def videolist():
	global videos
	html = ""


	for video in videos:

		name = video["file"]
		desc = []
		if video["starttime"] is not None:
			starttime = []
			(h,m,s) = video["starttime"]
			if h != 0: starttime.append(str(h))
			if len(starttime) != 0: starttime.append("0" + str(m) if m<10 else str(m))
			elif m>0: starttime.append(str(m))
			else: starttime.append("")
			starttime.append("0" + str(s) if s<10 else str(s))
			desc.append("from " + ":".join(starttime))
		if video["endtime"] is not None:
			endtime = []
			(h,m,s) = video["endtime"]
			if h != 0: endtime.append(str(h))
			if len(endtime) != 0: endtime.append("0" + str(m) if m<10 else str(m))
			elif m>0: endtime.append(str(m))
			else: endtime.append("")
			endtime.append("0" + str(s) if s<10 else str(s))
			desc.append("to " + ":".join(endtime))
		complete = (video["percentage"] == 100)

		showname = name + " (" + " ".join(desc) + ")"


		#log("Listing video " + l['id'] + ", title " + l['title'] + ", size " + str(l['size']) + ", loaded to " + str(l['loaded']) + "%")
		if complete:
			html += "<a href='/done/" + name + "' download><div class='button-small save'>&nbsp;</div></a><a href='/done/" + name + "'><div class='button-small watch'>&nbsp;</div></a><div class='button-small delete' onclick='deleteVideo(\"" + name + "\")'>&nbsp;</div>" + showname + "<br/>"
		else:
			##103 pixel in total
			TOTAL_PIXEL = 103
			pixel_yes = int(TOTAL_PIXEL * video["percentage"] / 100)
			pixel_no = TOTAL_PIXEL - pixel_yes
			html += "<div class='loadingbar-yes' style='width:" + str(pixel_yes) + "px'>&nbsp;</div><div class='loadingbar-no' style='width:" + str(pixel_no) + "px'>&nbsp;</div>" + showname + "<br/>"



	return html
