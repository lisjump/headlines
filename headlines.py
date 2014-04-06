#!/usr/bin/python

import xmlparser, sqlite3, sys, globalvars
feeddir = globalvars.feeddir
cgilis = globalvars.cgilis
db = globalvars.db
js = globalvars.js
css = globalvars.css
handheldcss = globalvars.handheldcss
#-----------------------------------------------------------------

def links_box():
  print_box_top("Links", "links")
  print "<a href=\"http://www.wirelesscouch.net\">Wirelesscouch</a><BR>\n"
  print "<a href=\"/cgi-bin/comics/comics.pl\">Comics</a><BR>\n"
  print "<a href=\"http://www.amazon.com/?_encoding=UTF8&camp=1789&creative=390957&linkCode=ur2&tag=wwwwirelessco-20\">Amazon Shopping</a><BR>\n"
  print "<a href=\"http://www.amazon.com/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/154606011/?_encoding=UTF8&camp=1789&creative=390957&linkCode=ur2&tag=wwwwirelessco-20&tf=1\">Kindle Best Sellers</a><BR>"
  print "<a href=\"http://www.amazon.com/gp/feature.html/?ie=UTF8&camp=1789&creative=390957&docId=1000677541&linkCode=ur2&tag=wwwwirelessco-20\">Kindle Daily Deals</a><BR>"
  print_box_bottom()

def weather_box():
  print_box_top()
  print "<center>\n"
  print "<img class=\"weather\" src=\"http://hubshout.com/Weather2/?ZIP=87544&WDUC=2847326A432943CF&BColor=Bold_Blue\" border=\"0\">"
  print "</center>\n"
  print_box_bottom()

def addfeed_box(categories):
  print_box_top("Add Feed", "addfeed")
  print "<form action=\"%saddFeed.py\"  method=\"post\">" % cgilis
  print "<input name=\"feedurl\" id=\"feedurl\" class=\"feedurl\" type=\"textbox\" placeholder=\"Enter Feed URL\"><br><br>"
  print "<select id=\"category\" name=\"category\">"
  for catname in categories.keys():
    print "	<option value='%s'>%s</option>" % (catname, categories[catname]['gui'])
  print "</select>"
  print " or <input name=\"newcat\" id=\"newcat\" class=\"newcat\" type=\"textbox\" placeholder=\"New Category\"><br><br>"
  print "<input type=\"submit\">"
  print "</form>"
  print_box_bottom()

def standard_box(name, gui=""):
  print_box_top(gui, name)
  print_rdf(name)
  print_box_bottom()

#-----------------------------------------------------------------
def print_rdf(prefix):
  filename = str(prefix) + ".html"
  try:
    html = open(filename, 'r')
  except:
    return
  for line in html:
    print line
  html.close()
	
def print_box_top(title="", name=""):
    if title:
      if name:
        print "<div class=\"boxtitle\" id=\"" + name + "boxtitle\" onClick=\"CollapseBox('" + name + "box');\">" + title + "</div>\n"
        print "<div class=\"boxwithtitle\" id=\"" + name + "box\">\n"
      else: 
        print "<div class=\"boxtitle\">" + title + "</div>\n"
        print "<div class=\"boxwithtitle\">\n"
    else:
      print "<div class=\"box\">\n"

def print_box_bottom():
    print "</div>\n"

def print_page_top():
  print "<html>\n"
  print "<head>\n"
  print "<title>Headlines</title>\n"
  print "<script src=\"%s\" type=\"text/javascript\"></script>" % (feeddir + js)
  print "<link rel=\"stylesheet\" href=\"" + feeddir + css + "\" type=\"text/css\" media=\"screen\">\n"
  print "<link rel=\"stylesheet\" href=\"" + feeddir + handheldcss + "\" type=\"text/css\" media=\"only screen and (max-device-width:480px)\">\n"
  print "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>"
  print "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/htmlcharset=UTF-8\">"
  print "<META http-equiv=\"refresh\" content=\"1800\">"
  print "</head>\n"
  print "<body>\n"

def print_page_bottom():
  print "</body>\n"
  print "</html>\n"


def die_handler():
    print "Bah!\n"

#--------------------------------------------------------------------

def getDBCategories():
  conn = sqlite3.connect(db)
  c = conn.cursor()
  c.execute("select name, gui from categories")
  rawcats = c.fetchall()
  categories = {}
  for cat in rawcats:
    categories[str(cat[0])] = {}
    categories[str(cat[0])]['gui'] = str(cat[1])
  conn.close()
  return categories

#--------------------------------------------------------------------

print "Content-Type:text/html\n\n"
print_page_top()


standardCategories = ("news", "craftblogs", "craftfeeds", "comics", "recipes", "friendsandme")
try:
  categories = getDBCategories()
except:
  print str(sys.exc_info()[0])
  print str(sys.exc_info()[1])
  print str(sys.exc_info()[2])

# Left-hand column
# ----------------
print "<div class=\"left\">\n"
weather_box()
links_box()
addfeed_box(categories)
for category in categories:
  if category not in standardCategories:
    standard_box(category, categories[category]['gui'])
standard_box("news", "News")
print "</div>\n"

# Right-hand column
# -----------------
print "<div class=\"right\">\n"
standard_box("craftblogs", "Craft Blogs")
standard_box("craftfeeds", "Craft Feeds")
print "</div>\n"

# Center-hand column
# ------------------
print "<div class=\"center\">\n"
standard_box("comics", "Comics")
standard_box("recipes", "Recipes")
standard_box("friendsandme", "Friends and Me")
print "</div>\n"

print_page_bottom()


