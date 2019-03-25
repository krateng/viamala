import os
from collections import namedtuple

videos = {}
    # key: filename
    # value: (from,to,percentagedone)

Video = namedtuple("Video",["starttime","endtime","percentage"])


#first startup, delete all leftover videofiles

for f in os.listdir("queue/"):
    if f != ".gitignore" and f!= "dummy": os.remove("queue/" + f)


def add(name,start=None,end=None):
    global videos

    if name in videos: return "ERROR_EXISTS"

    videos[name] = Video(start,end,0)
    return "SUCCESS"



def GET(k):
    if k.get("list") is not None:
        return videolist()



def videolist():
    global videos
    html = ""


    for file in videos:

        video = videos[file]

        name = file
        complete = (video.percentage == 100)


		#log("Listing video " + l['id'] + ", title " + l['title'] + ", size " + str(l['size']) + ", loaded to " + str(l['loaded']) + "%")
        if complete:
            html += "<a href='/done/" + name + "' download><div class='button-small save'>&nbsp;</div></a><a href='/done/" + name + "'><div class='button-small watch'>&nbsp;</div></a><div class='button-small delete' onclick='deleteVideo(\"" + name + "\")'>&nbsp;</div>" + name + "<br/>"
        else:
			##103 pixel in total
            TOTAL_PIXEL = 103
            pixel_yes = int(TOTAL_PIXEL * video.percentage / 100)
            pixel_no = TOTAL_PIXEL - pixel_yes
            html += "<div class='loadingbar-yes' style='width:" + str(pixel_yes) + "px'>&nbsp;</div><div class='loadingbar-no' style='width:" + str(pixel_no) + "px'>&nbsp;</div>" + name + "<br/>"



    return html
