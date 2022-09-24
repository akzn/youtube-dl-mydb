from __future__ import unicode_literals
import youtube_dl
from youtube_dl.postprocessor.common import PostProcessor

class TestPP(PostProcessor):
	def run(self, information):
                # Do something
		print(information['filepath'])
		return [], information  # return files ot delete, modified information


