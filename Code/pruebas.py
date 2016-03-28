# __author__ = 'jp'
import flickrapi
# import xml.etree.ElementTree as ET
#
# # disable annoying warnings
# import requests
# from requests.packages.urllib3.exceptions import InsecurePlatformWarning
# requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
#
# api_key = 'd084eb2e2daad51f9263ecdeb92b46df'
# api_secret = 'a0ee0b4031819e5c'
#
#
# flickr = flickrapi.FlickrAPI(api_key, api_secret)
# flickr.authenticate_via_browser(perms='read')
#
# # photo_id = "8350901100"
# photo_id = "24925669191"
#
# photo_info = flickr.photos.getInfo(photo_id=photo_id)
# print "\n\ngetInfo()"
# ET.dump(photo_info)
#
# ## returns only tags from photos
# # photo_list = flickr.tags.getListPhoto(photo_id=photo_id)
# # print "\n\n\ngetListPhoto()"
# # ET.dump(photo_list)
#
#
# print "\n\n\n"
# tree = ET.ElementTree(photo_info)
# root = tree.getroot()
# photo = root[0]
# # print photo.tag
# # print photo.attrib
#
# photo_data = []
# headers = ["id", "title", "description", "date taken", "photopage", "photostatic"]
# photo_data.append(photo.attrib["id"])
# photo_data.append(photo.find("title").text)
# photo_data.append(photo.find("description").text)
# photo_data.append(photo.find("dates").attrib["taken"].split(' ')[0])
#
# for url in photo.find("urls"):
#     if url.attrib["type"] == "photopage":
#         photo_data.append(url.attrib["type"]+": " + url.text)
# photo_data.append("pendingURL")
#
# for tag in photo.find("tags"):
#     photo_data.append(tag.text)
#
# print len(headers)
# print headers
# print len(photo_data)
# print photo_data
# print len(photo.find("tags"))
# # for tag in photo.find("tags"):
# #     print tag.text,
#
# photo_data = []
#
#
# # a = [1,2,3]
# # b = [1,2]
# # c = [1,2,3,4,5]
# #
# # photo_data = [a,b,c]
# #
# #
# # print len(max(photo_data))
#
# # #
# # # print len(max(a, b, c, key=len))
#
#

data = [['a','b'], ['a','c'], ['b','d']]
search = 'c'
print any(e[0] == search for e in data)

