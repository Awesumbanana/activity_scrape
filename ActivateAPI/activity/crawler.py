import requests
import pywikibot
import json
from bs4 import BeautifulSoup
import re


class Crawler:
    nominatim_base_url = 'https://nominatim.openstreetmap.org/'

    def __init__(self) -> None:
        self.osm_type = {'way': 'W', 'node':'N', 'relation':'R'}

    def extract_address_information(self, place_details, osm_details):
        address_information = {}
        coordinates = osm_details.get("centroid")
        address = osm_details.get('addresstags')

        address_information['address_latitude'] = coordinates.get('coordinates')[0]
        address_information['address_longitude'] = coordinates.get('coordinates')[1]
        address_information['address_city'] = address.get('city')
        address_information['address_line_1'] = place_details.get('display_name')
        address_information['address_zip'] = address.get('postcode')
        address_information['address_state'] = address.get('state')

        return address_information

    def get_image_author_and_license(self, wiki_url, caption):
        image_url = wiki_url + caption
        img_page = requests.get(image_url)
        soup = BeautifulSoup(img_page.content, "html.parser")
        author_table = soup.find('table', class_="fileinfotpl-type-information toccolours vevent mw-content-ltr")
        fields = author_table.find_all('tr')
        author = ''
        for field in fields:
            data = field.find_all('td')
            tag = []
            for data_field in data:
                tag.append(data_field.text)
            if 'Author' in tag:
                author = re.sub(r'http\S+', '', tag[1])

        license = ''
        license_table = soup.find('table', class_="layouttemplate licensetpl mw-content-ltr")
        fields = license_table.find_all('tr')
        for field in fields:
            data = field.find_all('td')
            tag = ''
            for data_field in data:
                tag = data_field.text
                search_text = 'This file is licensed under the '
                if search_text in tag:
                    license = tag.replace(search_text, '')
                    print(license)
                    break

        return author, license

    def query_wikimedia(self, category):
        images = {}
        wikimedia_url = "https://commons.wikimedia.org/wiki/"
        page_url = wikimedia_url + "Category:" + str(category).replace(" ", "_")
        page = requests.get(page_url)

        soup = BeautifulSoup(page.content, "html.parser")
        gallery = soup.find("ul", class_="gallery mw-gallery-traditional")
        gallery_images = gallery.find_all('li', class_="gallerybox")
        for image in gallery_images:
            picture = image.find('img').get('src')
            caption = image.find('a', class_='galleryfilename galleryfilename-truncate').get('title')
            author, license = self.get_image_author_and_license(wikimedia_url, caption)
            images[caption] = {'image_url':picture, 'caption': caption, 'author': author, 'license': license}
        return images
    
    def query_wikidata(self, wiki_id):
        wiki_details = {}
        claims_to_get = {'P856': "website", 'P373': 'commons_category'}
        site = pywikibot.Site("wikidata", "wikidata")
        repo = site.data_repository()
        item = pywikibot.ItemPage(repo, wiki_id)
        item_dict = item.get()
        claim_dict = item_dict["claims"]
        for claim in claims_to_get.keys():
            claim_list = claim_dict[claim]
            clm_trgt = ""
            for clm in claim_list:
                clm_trgt = clm.getTarget()
                if claim == 'P373':
                    images = self.query_wikimedia(clm_trgt)
                    wiki_details["images"] = json.dumps(images)
                break
        
            wiki_details[claims_to_get[claim]] = clm_trgt
        return wiki_details


    def extract_details(self, place_details, osm_type, osm_id):
        activity_details = {}
        payload = {'osmtype': osm_type, 'osmid': osm_id, 'format': 'json'}
        response = requests.get(self.nominatim_base_url + 'details.php', params=payload)
        osm_details = response.json()
        activity_details['activity_id'] = osm_details.get('place_id')
        activity_details['activity_name'] = osm_details.get('names').get('name')
        wiki_details = self.query_wikidata(osm_details.get('extratags').get('wikidata'))
        address_details = self.extract_address_information(place_details, osm_details)
        activity_details.update(address_details)
        activity_details.update(wiki_details)
        return activity_details

    def get_experience_data(self, query):
        payload = {'q': query, 'format': 'jsonv2', 'addressdetails': 1, 'limit': 1}
        r = requests.get(self.nominatim_base_url + 'search', params=payload)
        place_details = r.json()[0] 
        osm_type = self.osm_type.get(place_details.get('osm_type'))
        osm_id = str(place_details.get("osm_id"))
        experience_details = self.extract_details(place_details, osm_type, osm_id)
        return experience_details


    