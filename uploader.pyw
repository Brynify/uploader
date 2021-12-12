from keyboard_handler.wx_handler import WXKeyboardHandler
import tray
from LinkUI import ShowLink
import audio_input
from threading import Thread
import webbrowser
from tweak import Config
import os.path as path
import sys
import urllib
import application

import requests
import wx

# Globals

audio=audio_input.AudioInput()


class AudioUploader(wx.Frame):
	"""Application to allow uploading of audio files to SndUp"""
	def __init__(self, title):
		self.recording=False
		wx.Frame.__init__(self, None, title=title, size=wx.DefaultSize) # initialize the wx frame
		# load config.
		self.config = Config(name="uploader", autosave=True)
		# window events and controls
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.tray=tray.TaskBarIcon(self)
		self.handler=WXKeyboardHandler(self)
		self.handler.register_key("win+shift+u",self.ToggleWindow)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.select_file = wx.Button(self.panel, -1, "&Select File")
		self.select_file.Bind(wx.EVT_BUTTON, self.SelectFile)
		self.main_box.Add(self.select_file, 0, wx.ALL, 10)
		self.record = wx.Button(self.panel, -1, "&Record")
		self.record.Bind(wx.EVT_BUTTON, self.Record)
		self.main_box.Add(self.record, 0, wx.ALL, 10)
		self.upload = wx.Button(self.panel, -1, "&Upload")
		self.upload.Bind(wx.EVT_BUTTON, self.OnUpload)
		self.main_box.Add(self.upload, 0, wx.ALL, 10)
		self.upload.Hide()
		self.hide = wx.Button(self.panel, -1, "&Hide Window")
		self.hide.Bind(wx.EVT_BUTTON, self.ToggleWindow)
		self.main_box.Add(self.hide, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CLOSE, "&Close")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()

	def ToggleWindow(self,event=None):
		if self.IsShown():
			self.Show(False)
		else:
			self.Show(True)
			self.Raise()
			self.select_file.SetFocus()
	def OnUpload(self,event):
		self.UploadThread = Thread(target=self.StartUpload)
		self.UploadThread.start()

	def StartUpload(self):
		"""Starts an upload; only runs after a standard operating system find file dialog has been shown and a file selected"""
		self.select_file.Hide()
		self.upload.Hide()
		self.record.Hide()
		r=requests.post("https://www.sndup.net/post.php", files={"file":open(audio.filename,'rb')})
		try:
			wx.CallAfter(lambda: ShowLink(self,r.json()['url']))
		except:
			ShowLink(self,"Error: "+str(r.text))
		self.Reset()

	def Record(self,event):
		if self.recording==False:
			audio.start_recording()
			self.record.SetLabel("&Stop")
			self.select_file.Hide()
			self.upload.Hide()
			self.recording=True

		elif self.recording==True:
			audio.stop_recording()
			self.record.SetLabel("&Record")
			self.select_file.Show()
			self.upload.Show()
			self.recording=False
			audio.is_recording=True

	def SelectFile(self,event=None):
		"""Opens a standard OS find file dialog to find an audio file to upload"""
		openFileDialog = wx.FileDialog(self, "Select the audio file to be uploaded", "", "", "Audio Files (*.mp3, *.ogg, *.wav, *.flac, *.opus)|*.mp3; *.ogg; *.wav; *.flac; *.opus", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		if openFileDialog.ShowModal() == wx.ID_CANCEL:
			return False
		audio.filename= openFileDialog.GetPath()
		audio.name=path.basename(audio.filename)
		if audio.is_recording==True:
			audio.cleanup()
		self.record.Hide()

		self.upload.Show()

	def Reset(self, event=None):
		self.record.Show()
		self.upload.Hide()
		self.select_file.Show()
		self.select_file.SetFocus()
		if audio.is_recording==True:
			audio.cleanup()

	def QuickUpload(self,event=None):
		res=self.SelectFile()
		if res!=False: self.StartUpload()
		else: self.Reset()

	def OnClose(self, event):
		"""App close event handler"""
		if audio.is_recording==True:
			audio.cleanup()
		self.tray.on_exit(event,False)
		self.Destroy()

def ask(parent=None, message='', default_value=''):
	"""Simple dialog to get a response from the user"""
	dlg = wx.TextEntryDialog(parent, message)
	dlg.ShowModal()
	result = dlg.GetValue()
	dlg.Destroy()
	return result


app = wx.App(redirect=False)
window=AudioUploader(application.name+" "+application.version)
window.Show()
app.MainLoop()