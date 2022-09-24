from __future__ import unicode_literals
import youtube_dl
from youtube_dl.postprocessor.common import PostProcessor

class CustomPP(PostProcessor):
	def run(self, information):
                # Do something
		print(information['filepath']+' conversion finised')
		return [], information  # return files ot delete, modified information


