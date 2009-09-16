# What is PyTadaList?

[Ta-da List](http://tadalist.com) has no API.  It's exceptionally useful as an easy-to-share todo list manager.  However, it's not particularly extensible since there's no official API.  That said, there are ways to work with a website without an API.  Unfortunately, this often means trying to figure out how the requests work internally and scraping web pages.  PyTadaList takes that approach in order to provide some means of accessing and updating Ta-da lists.

PyTadaList is built using Python and various other technologies available to Python.  It is, by it's nature, a hack.  However, until the Ta-da List website changes, it's a hack that works.

## PyTadaList requirements

* Mac OS X 10.5+ and Safari (requirement explained below)
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

## Why Mac OS X?

PyTadaList currently requires Mac OS X (10.5+, although I've only tested on 10.6 and it might work on 10.4) simply because I was lazy.  I didn't want to have to worry about authentication with Ta-da List so I used a cheap hack that I've used dozens of times before in my own scripts.  Basically, if you're authenticated in Safari, most of the Cocoa methods that retrieve data from the web will also be authenticated.  This saved me the headache of worrying about that at the moment and let me focus on writing the other code.  In the future, I'll return and do proper authentication unless someone beats me to it.

## How to use PyTadaList

PyTadaList should be able to be dropped into any Python script, but there's one bit of setup necessary.  If you've never logged in to Ta-da List through Safari, you'll need to do so (see "Why Mac OS X?").  Also, only the account that's logged in can access the lists.  This will change in a future version when proper logging credentials are implemented.  I've also tried to provide meaningful docstrings that demonstrate using PyTadaList.  Once you're set up, things are fairly easy:

	api = TadaAPI('username')
	lists = api.lists
	items = lists[0].items
	print items[0].content

## Contact information

[Grayson Hansard](mailto:info@fromconcentratesoftware.com)  
[From Concentrate Software](http://www.fromconcentratesoftware.com/)