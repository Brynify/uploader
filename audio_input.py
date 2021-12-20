import platform
import subprocess
import os
import tempfile
import sound_lib
from sound_lib import input, recording

class AudioInput(object):
	def __init__(self,window):
		self.window=window
		self.is_recording=False
		self.input = input.Input()
		self.recordingname=""
		self.filename=""
		self.name=""

	def encode(self,filename, quality=4.5):
		system = platform.system()
		if system == "Windows":
			subprocess.call(r'"%s" -q %r "%s"' % ("oggenc2.exe", quality, filename))
			return self.filename.replace(".wav",".ogg")
		elif system == "Darwin":
			os.system("afconvert -f mp4f -d aac -c 2 -s 3 --mix \""+filename+"\" \""+self.filename.replace(".wav",".m4a")+"\"")
			return self.filename.replace(".wav",".m4a")
		else:
			print("Converting not implimented for this operating system. WAV file incoming.")
			return self.filename

	def start_recording(self):
		self.filename = self.window.confpath+"/recording.wav"
		with open(self.filename,"wb"):
			pass
		self.recording = self.recording(self.filename)
		self.recording.play()

	def stop_recording(self):
		self.recording.stop()
		self.recording.free()
		self.recordname=self.filename
		self.filename=self.encode(self.filename)


#Internal Functions
	def cleanup(self):
		os.remove(self.filename)
		os.remove(self.recordname)
		self.is_recording=False

	def recording(self,filename):
		val = recording.WaveRecording(filename=filename)
		return val