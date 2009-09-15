import objc
from Foundation import NSString, NSURL, NSURLConnection, NSMutableURLRequest
from BeautifulSoup import *
from urllib import urlopen, urlencode, quote
from os import system

class TadaAPI(object):
	"""TadaAPI is a simple entrance to access TadaList items.  It's a very basic wrapper around the HTTP
	requests and services that TadaList uses.  There is no official API, so this kind of hacks one together.
	
	TadaAPI is the starting point for working with TadaLists.  You must first create your TadaAPI and then work
	with the lists.  By (current) design, the API makes no attempt to authenticate with the server.  Instead,
	as a kludgy hack, TadaAPI uses OS X's Cocoa underpinnings to do all of the authentication.  Basically, if you're
	logged in to TadaList through Safari, then you're logged in through TadaAPI.
	
	To begin, pass your username to TadaAPI and then request an array of TadaLists:
		api = TadaAPI('ghansard')
		lists = api.lists"""
	def __init__(self, username):
		super(TadaMyLists, self).__init__()
		self.username = username
		self.lists = self._fetchLists()
		
	def _fetchLists(self):
		"""A private convenience function that uses BeautifulSoup (for parsing) and NSString (for authentication) 
		to make combing the HTML code from the main page of lists a bit easier."""
		page = NSString.stringWithContentsOfURL_(NSURL.URLWithString_("http://%s.tadalist.com/lists" % (self.username)))
		soup = BeautifulSoup(page)
		rawLists = soup.findAll('li')
		lists = []
		for rawList in rawLists:
			lists.append( TadaList(rawList.a['href'], rawList.a.contents[0], self) )
		return lists	

class TadaItem(object):
	"""TadaItem represents an entry on a TadaList list.  It isn't a simple string object because every TadaItem
	is represented by an id.  This id is used to alter or remove existing items.  Therefore, this is a small
	wrapper around a very simple object.
	
	Example:
		list = api.lists[0]
		item = list.items[0]
		txt = item.content
		itemID = item.id"""
	def __init__(self, content, iid, list):
		super(TadaItem, self).__init__()
		self.content = content
		self.id = iid
	
	def __str__(self):
		return self.content
		

class TadaList(object):
	"""TadaList represents a list of items.  The items are fetched on an as-need basis.  TadaLists are rather simple.
	They only contain a title and their items.  This code retains a few private attributes but nothing of any
	real use apart from the API.
	
	Example:
		list = api.lists[0]
		item = list.items[0]
		list.addItem('Write better TadaAPI documentation.')"""
	def __init__(self, href, title, api):
		super(TadaList, self).__init__()
		self.title = title
		self._href = href
		self._api = api
		self._items = None
	
	def __getattr__(self, name):
		if name == 'items':
			if not self._items: self._items = self._fetchItems()
			return self._items
		else:
			raise AttributeError

	def __str__(self):
		return {'title': self.title, 'items': [str(x) for x in self.items]}
	
	def _url(self):
		"This is a convenience method to quickly and easily put together a URL that points to the list's HTML page."
		return 'http://%s.tadalist.com%s' % (self._api.username, self._href)
	
	def _fetchItems(self, force=True):
		"""Private method that fetches attributes off of the list's page, parses the HTML (with BeautifulSoup),
		and then creates TadaItems.  This is called automatically when a user requests the 'items' of a TadaList."""
		page = NSString.stringWithContentsOfURL_(NSURL.URLWithString_(self._url()))
		soup = BeautifulSoup(page)
		lis = soup.findAll('li')
		items = []
		for li in lis: 
			items.append(TadaItem(li.form.contents[-1].strip(), li['id'], self))
		self.items = items
		return self.items
		
	def addItem(self, content):
		"""Add an item to the TadaList.  The content of the item should be a string.  Note that the TadaList will
		reset its list of items and request them again the next time you ask for them.  This is to make sure that
		the items remain in sync with the website.
		
		Example:
			list.addItem('Write better TadaAPI documentation.')"""
		url = self._url() + "/items"
		payload = urlencode({"item[content]":content})
		system("curl -d \"%s\" %s" % (payload, url))
		self._items = None # Reset so next call to items will be re-downloaded

def main():
	t = TadaAPI("ghansard")
	tips = t.lists[0]
	tips.addItem("This is a test")
	tips.items
	
	
if __name__ == '__main__':
	main()