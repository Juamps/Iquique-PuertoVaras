__author__ = 'jp'

from instagram.client import InstagramAPI
from instagram import client, subscriptions
import xml.etree.ElementTree as ET
# import requests
# from requests.packages.urllib3.exceptions import InsecurePlatformWarning
import codecs # handle utf8 characters

# disable annoying warnings
# requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

# client id and secret from instagram.com/developer
client_id = 'a6309285db6e406b808d518a7ba58f1b'
client_secret = '358332f04523411d823afc5ee326d5a8'
redirect_uri = 'http://juanpablo.jp'
access_token = '31469534.a630928.bd099cb3b35448f9a0c5883fb36915ee'
user_id = '31469534'  # me
'''
to get access token
curl -F 'client_id=a6309285db6e406b808d518a7ba58f1b' \
    -F 'client_secret=358332f04523411d823afc5ee326d5a8' \
    -F 'grant_type=authorization_code' \
    -F 'redirect_uri=http://juanpablo.jp' \
    -F 'code=63af9a28c24f4ac7a7265ef54136380e' \
    https://api.instagram.com/oauth/access_token
'''

CONFIG = {
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri
}

unauthenticated_api = client.InstagramAPI(**CONFIG)

# coordinates from Google Maps
iquique_lat = -20.232250
iquique_lon = -70.134902
iquique_tags = "iquique"


puertovaras_lat = -41.317345
puertovaras_lon = -72.984192
puertovaras_tags = "puertovaras"

filename_loc = "iquique_loc"
filename_tag = "iquique_tag"

per_page = 250  # 1-250; documentation says 500 but tried it and only get up to 250 per page

headers = ["id", "title", "description", "date taken", "photopage", "photostatic"]
all_photos = []


def get_photo_info(photo):
    '''
    :param page: will extract all the photos from this page
    :return: returns an xml.etree._Element with added url and camera attributes and appends exif data as children
    '''
        # photo = page[0]
        # print ET.dump(photo)
    ans = False
    photo_info = None
    cont = 0

    photo_id = photo.get('id')
    try:
        # get info data on images
        photo_info = flickr.photos.getInfo(photo_id=photo_id)[0]
        # ET.dump(photo_info)
        # if len(photo_info.find("tags")) > 0:
        #     ans = True


        # print ET.dump(photo)
        # photo_tree = ET.ElementTree(photo)
        # photo_tree.write('fotos_iquique.xml')
        ans = True
    except flickrapi.exceptions.FlickrError as e:
        print "[!]", e
        # print ET.dump(exif)
    finally:
        pass
    # print ET.dump(page)
    return ans, photo_info


def append_photo_info(photo):

    photo_data = []
    # generate static url
    #https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
    # to retrieve original file
    # format = photo.get('originalformat')
    #https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{o-secret}_o.(jpg|gif|png)
    photo_id = photo.get('id')
    farm_id = photo.get('farm')
    server_id = photo.get('server')
    secret = photo.get('secret')
    static_url = "https://farm"+farm_id+".staticflickr.com/"+server_id+"/"+photo_id+"_"+secret+".jpg"

    # headers = ["id", "title", "description", "date taken", "photopage", "photostatic"]
    # append data to local array
    photo_data.append(photo.attrib["id"])

    # clean and validate title before append
    title = photo.find("title").text
    if title:
        title = " ".join(title.splitlines())
        title = "\"" + title + "\""
    photo_data.append(title)
    # clean and validate description before append
    description = photo.find("description").text
    if description is not None:
        description = " ".join(description.splitlines())
        description = "\"" + description + "\""
    photo_data.append(description)
    photo_data.append(photo.find("dates").attrib["taken"].split(' ')[0])

    for url in photo.find("urls"):
        if url.attrib["type"] == "photopage":
            photo_data.append(url.text)
    photo_data.append(static_url)

    tags = photo.find("tags")
    if tags is not None:
        for tag in tags:
            photo_data.append(tag.text)

    # check for None elements and replace with string
    photo_data = ["None" if not attr else attr for attr in photo_data]
    # append to aggregate
    all_photos.append(photo_data)


def append_page_info(page):
    cont = 1
    for photo in page:
        print "[+] Getting info for photo", cont
        photo_info = get_photo_info(photo)
        if photo_info[0]:
            append_photo_info(photo_info[1])
        else:
            print "[!] No tags, skipping... \n    Photo id:", photo_info[1].attrib["id"]
        # print "[+]", cont, "photos from this page done."
        cont += 1



def dump_to_csv():
    filename = filename_loc
    # find maximum number of args per photo
    max_args = 0
    for photo in all_photos:
        l = len(photo)
        if l > max_args:
            max_args = l

    max_tags = max_args - len(headers)

    for i in range(0, max_tags):
        headers.append("tag")
    try:
        print "\n[+] Writing CSV file..."
        with codecs.open(filename+".csv", "wb", "utf-8") as f:
            file_headers = ",".join(headers)
            f.write(file_headers + "\n")
            for photo in all_photos:
                file_attributes = ",".join(photo)
                f.write(file_attributes + "\n")
        print "[!] DONE!"
    except IOError as e:
        print "[!] ERROR! Could not write file: ", e.message

if __name__ == '__main__':
    api = InstagramAPI(access_token=access_token, client_secret=client_secret)
    media_ids, next = api.tag_recent_media(tag_name='instadogs', count=80)
    for media_id in media_ids:
        print media_id

