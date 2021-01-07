from xml.etree import ElementTree
import feedparser
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pickle

blog_urls = []
flag = 0

with open('engineering_blogs.opml', 'rt') as f:
    tree = ElementTree.parse(f)

for node in tree.findall('.//outline'):
    url = node.attrib.get('xmlUrl')
    if url:
        blog_urls.append(url)

try:
  with open('listfile.data', 'rb') as filehandle:
    data_array = pickle.load(filehandle)
    exists = True
except:
  data_array = []
  exists = False


for link in blog_urls:
    try:
        feeds = feedparser.parse(link)
        for x in range(0, len(feeds.entries)):
            data = {}
            data['title'] = feeds.entries[x].title

            refined_ar = ((BeautifulSoup(feeds.entries[x].summary, features="html.parser")).get_text()).split('.')[:10]
            data['description'] = ".".join(refined_ar)

            data['url'] = feeds.entries[x].link

            
            if(len(feeds.entries[x].published) == 29 or len(feeds.entries[x].published) == 31):
                dt = datetime.strptime((feeds.entries[x].published)[:24], '%a, %d %b %Y %H:%M:%S')
                data['published'] = f"{'%02d' % dt.day} {'%02d' % dt.month} {dt.year} {'%02d' % dt.hour}:{'%02d' % dt.minute}"
            elif (len(feeds.entries[x].published) == 25 or len(feeds.entries[x].published) == 24):
                dt = datetime.strptime((feeds.entries[x].published)[:19], '%Y-%m-%dT%H:%M:%S')
                data['published'] = f"{'%02d' % dt.day} {'%02d' % dt.month} {dt.year} {'%02d' % dt.hour}:{'%02d' % dt.minute}"
            else:
                continue
            
            if hasattr(feeds.entries[x], 'media_content'):
                data['image'] = feeds.entries[x].media_content
            else:
                data['image'] = ""

            if hasattr(feeds.entries[x].author_detail, 'name'):
                data['author_name'] = feeds.entries[x].author_detail.name
            else:
                data['author_name'] = ""

            if hasattr(feeds.entries[x].author_detail, 'href'):
                data['author_url'] = feeds.entries[x].author_detail.href
            else:
                data['author_url'] = ""
               

            if hasattr(feeds.entries[x], 'media_thumbnail'):
                data['author_icon'] = feeds.entries[x].media_thumbnail
            else:
                data['author_icon'] = "" 
            
            if bool(data) == True and dt.year >= 2021:
                if (exists == True and data not in data_array) or exists == False:
                    data_array.append(data)   
    
    except Exception as e:
        continue
    
new_array = sorted(data_array, key = lambda i: datetime.strptime(i['published'], "%d %m %Y %H:%M"), reverse=True)


with open('listfile.data', 'wb') as filehandle:
    pickle.dump(new_array, filehandle)
