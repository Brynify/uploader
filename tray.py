import wx.adv
from wx import Icon
TRAY_TOOLTIP = 'Uploader'
TRAY_ICON = 'icon.png'

def create_menu_item(menu, label, func):
	item = wx.MenuItem(menu, -1, label)
	menu.Bind(wx.EVT_MENU, func, id=item.GetId())
	menu.Append(item)
	return item

class TaskBarIcon(wx.adv.TaskBarIcon):
	def __init__(self, frame):
		self.frame = frame
		super(TaskBarIcon, self).__init__()
		self.set_icon(None)
		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

	def CreatePopupMenu(self):
		menu = wx.Menu()
		if self.frame.IsShown():
			create_menu_item(menu, 'Hide window', self.OnShowHide)
		else:
			create_menu_item(menu, 'Show window', self.OnShowHide)
		create_menu_item(menu, 'Quick Upload...', self.frame.QuickUpload)
		create_menu_item(menu, 'Exit', self.on_exit)
		return menu

	def on_left_down(self, event):
		self.OnShowHide(event)

	def OnShowHide(self, event):
		self.frame.ToggleWindow()

	def on_exit(self, event, blah=True):
		self.Destroy()
		if blah:
			self.frame.OnClose(event)

	def set_icon(self, path):
#		icon = wx.Icon(wx.Bitmap(path))
		self.SetIcon(Icon(), TRAY_TOOLTIP)