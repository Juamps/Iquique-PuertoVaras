__author__ = 'jp'

import flickrapi
import xml.etree.ElementTree as ET

# disable annoying warnings
import requests
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
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
per_page = 10  # 1-250; documentation says 500 but tried it and only get up to 250 per page



def get_photo_info(page):
    '''
    :param page: will extract all the photos from this page
    :return: returns an xml.etree._Element with added url and camera attributes and appends exif data as children
    '''
        # photo = page[0]
        # print ET.dump(photo)
    cont = 0
    for photo in page:
        try:
            # get photo info
            photo_id = photo.get('id')
            farm_id = photo.get('farm')
            server_id = photo.get('server')
            secret = photo.get('secret')
            photo_url = "https://farm"+farm_id+".staticflickr.com/"+server_id+"/"+photo_id+"_"+secret+".jpg"
            photo.attrib['url'] = photo_url

            #https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg

            # to retrieve original file
            # format = photo.get('originalformat')
            #https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{o-secret}_o.(jpg|gif|png)

            # get EXIF data on images
            exif = flickr.photos.getExif(photo_id=photo_id)[0]
            photo.attrib['camera'] = exif.get('camera')
            for element in exif:
                photo.append(element)


            # print ET.dump(photo)
            # photo_tree = ET.ElementTree(photo)
            # photo_tree.write('fotos_iquique.xml')
        except flickrapi.exceptions.FlickrError as e:
            print "[!]", e
            # print ET.dump(exif)
        finally:
            cont += 1
            print "[+]", cont, "photos from this page done."
    # print ET.dump(page)
    return page

if __name__ == '__main__':
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    flickr.authenticate_via_browser(perms='read')

    root = ET.fromstring("<photos></photos>")

    #accuracy (Optional) Recorded accuracy level of the location information.
    #World level is 1, Country is ~3, Region ~6, City ~11, Street ~16.
    #Current range is 1-16. Defaults to 16 if not specified.
    extras = 'original_format,geo'
    photo_page_iquique = flickr.photos.search(lat=iquique_lat, lon=iquique_lon, accuracy=11,
                                          per_page=per_page, page=1,  # default page = 1
                                          extras=extras)

    # photo_page_puertovaras = flickr.photos.search(lat=puertovaras_lat, lon=puertovaras_lon, accuracy=11,
    #                                       per_page=per_page, page=1,  # default page = 1
    #                                       extras=extras)

    #Check if query was successful
    if photo_page_iquique.get('stat') == 'ok':
        current_page = photo_page_iquique[0]
        tot_pages = 1
        # get number of total pages in results
        # tot_pages = int(current_page.get('pages'))
        page_num = 1
        print '[+] Request ok'
        while page_num <= tot_pages:
            print "[+] Fecthing page", page_num, "of", tot_pages
            current_page = flickr.photos.search(lat=iquique_lat, lon=iquique_lon, accuracy=11,
                                          per_page=per_page, page=page_num,  # default page = 1
                                          extras=extras)[0]
            photos = get_photo_info(current_page)
            for photo in photos:
                root.append(photo)
            page_num += 1
        print "[+] Done!"

        photo_tree = ET.ElementTree(root)
        photo_tree.write('fotos_puertovaras.xml')
        # ET.dump(current_page)
    # print len(photo_page_iquique[0]) # 250
    #
    # for photo in photo_page_iquique[0]:
    #     print photo.get('title')
    # print (photo_page_iquique[0][0])

    # ET.dump(photo_page_iquique)

    # photos = flickr.photos.search(user_id='20154996@N00', per_page='10')
    # sets = flickr.photosets.getList(user_id='20154996@N00')

    #######
    ################
    #######
    #Get photos
    #See number of pages
    #For each one, get page ??
    #Store photo data
    #For each photo id get metadata
    #Store metadata ((((((CSV FILE??))))))