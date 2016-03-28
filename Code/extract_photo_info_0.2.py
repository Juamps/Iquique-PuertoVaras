__author__ = 'jp'

import flickrapi
import xml.etree.ElementTree as ET
import requests
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
import codecs # handle utf8 characters
import sys

# disable annoying warnings
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

# keys must be obtained from http://www.flickr.com/services/api/keys/apply/
# a Yahoo! account is needed
api_key = 'd084eb2e2daad51f9263ecdeb92b46df'
api_secret = 'a0ee0b4031819e5c'

# coordinates from Google Maps
iquique_lat = -20.232250
iquique_lon = -70.134902
iquique_tags = "iquique"


puertovaras_lat = -41.317345
puertovaras_lon = -72.984192
puertovaras_tags = "puertovaras"

filename_loc = "iquique_loc_3"
filename_tag = "puertovaras_tag"

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

    # if any(ph[0] == photo_data for ph in all_photos):
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
    # else:
    #     print "[!] Photo already in collection"


def append_page_info(page):
    cont = 1
    for photo in page:
        print "\t[+] Getting info for photo", cont
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
    try:
        flickr = flickrapi.FlickrAPI(api_key, api_secret)
        flickr.authenticate_via_browser(perms='read')


        lat = iquique_lat
        lon = iquique_lon

        root = ET.fromstring("<photos></photos>")

        #accuracy (Optional) Recorded accuracy level of the location information.
        #World level is 1, Country is ~3, Region ~6, City ~11, Street ~16.
        #Current range is 1-16. Defaults to 16 if not specified.
        extras = 'original_format,geo'
        ## iquique
        photo_page = flickr.photos.search(lat=lat, lon=lon, accuracy=11,
                                              per_page=per_page, page=1,  # default page = 1
                                              extras=extras)
        ## tags
        # photo_page = flickr.photos.search(tags=iquique_tags, accuracy=11,
        #                                       per_page=per_page, page=1,  # default page = 1
        #                                       extras=extras)

        #Check if query was successful
        if photo_page.get('stat') == 'ok':
            current_page = photo_page[0]
            # get number of total pages in results
            tot_pages = int(current_page.get('pages'))
            page_num = 1
            print '[+] Request ok \n   ', tot_pages, "pages retrieved."
            # tot_pages = 3
            while page_num <= tot_pages:
                print "\n[+] Fecthing page", page_num, "of", tot_pages
                current_page = flickr.photos.search(lat=lat, lon=lon, accuracy=11,
                                              per_page=per_page, page=page_num,  # default page = 1
                                              extras=extras)[0]

                append_page_info(current_page)
                page_num += 1
            print "[!] DONE!"
    except:
        print "\n\n[!!] Unexpected error:", sys.exc_info()[0]
        # write info to CSV file
    finally:
        dump_to_csv()

        # ET.dump(current_page)
    # print len(photo_page_iquique[0]) # 250
    #
    # for photo in photo_page_iquique[0]:
    #     print photo.get('title')
    # print (photo_page_iquique[0][0])

    # ET.dump(photo_page_iquique)

    # photos = flickr.photos.search(user_id='20154996@N00', per_page='10')
    # sets = flickr.photosets.getList(user_id='20154996@N00')

    '''
    REVISAR
    '''
