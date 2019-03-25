import re
from serverutil import log
from settings import *
import json

def GET(k):


	#localisation = getSettingsDict("TEXT_TITLE","TEXT_SELECT","TEXT_HEADER","TEXT_VIDEO","TEXT_SUBMIT","TEXT_VIDEOLIST")
	localisation = getSettingsDictPrefix("TEXT_")

	page = """

<html>
  <head>
    <title>""" + localisation["TITLE"] + """</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="icon" type="image/png" href="favicon.png">

    <meta charset="utf-8">

	<link href="https://fonts.googleapis.com/css?family=Roboto+Mono" rel="stylesheet">
	<link href="https://fonts.googleapis.com/css?family=Pacifico" rel="stylesheet">
	<script type="text/javascript" src="portal.js"></script>

	<script>
		localisation = """ + json.dumps(localisation) + """
	</script>
  </head>
  <body onload="pageLoad()" ondragover="dragover(event)" ondrop="readFile(event)">
    <br>
    <h1>""" + localisation["HEADER"] + """</h1>

    	<div class="input" id="dropzone">""" + localisation["VIDEO"] + """:
			<!-- The actual file input field, not visible to avoid the ugly button -->
			<input type="file" id ="fileupload" style="display:none;" onchange="copyText()"/>
			<!-- A fake input field -->
			<input class="urlinput" id="fake_fileupload" placeholder='""" + localisation["DEFAULTVIDEO"] + """' readonly/>
			<label for="fileupload"><div class="button">""" + localisation["SELECT"] + """</div></label>
			<div class="button" onclick="uploadFile()">""" + localisation["SUBMIT"] + """</div>
		</div>
		<br/>
		<div class="input">
			<input id="from" type="checkbox" /> """ + localisation["TIME_START"] + """
				<input type="number" min=0 max=99 value=0 maxlength=2 id="from_hours" />:
				<input type="number" min=00 max=59 value=0 maxlength=2 id="from_minutes" />:
				<input type="number" min=00 max=59 value=0 maxlength=2 id="from_seconds" />

			<input id="to" type="checkbox" /> """ + localisation["TIME_END"] + """
				<input type="number" min=0 max=99 value=0 maxlength=2 id="to_hours" />:
				<input type="number" min=00 max=59 value=0 maxlength=2 id="to_minutes" />:
				<input type="number" min=00 max=59 value=0 maxlength=2 id="to_seconds" />
		</div>

    	<p id="status">&nbsp;</p>
    <br>
    <br>
    <br>
    <br>
    <br>

    <div class="category">""" + localisation["VIDEOLIST"] + """</div><br/>
    <div class="files" id="filelist">

    </div><br/>








  </body>


</html>



	"""


	return page
