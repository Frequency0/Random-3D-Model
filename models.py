
from common import print_and_log, logger
from random import randint

class Thingiverse():

    def __init__(self, session, filter):
        self.session = session
        self.filter = filter

        self.item_url = None
        self.files_urls = None
        self.item_name = None
        self.item_user = None
        self.item_response = None
    
    def find_random_print(self, times_to_try):
        if self.session:
            for ind in range(0,times_to_try):
                print_and_log(ind, end='\r')
                if self.filter:
                    url = f'https://www.thingiverse.com/search?q={self.filter.lower()}&type=things&sort=relevant&page={randint(0,500)}'
                else:
                    url = f'https://www.thingiverse.com/search?type=things&sort=relevant&page={randint(0,500)}'
                logger.info(f'Search URL: {url}')
                response = self.session.get(url)
                res_code = response.status_code
                if res_code == 200:
                    response.html.render(sleep=2)
                    items_links = response.html.find('a.ThingCardBody__cardBodyWrapper--ba5pu')
                    for ind in range(0,len(items_links)-1):
                        chosen_url = items_links[randint(ind,len(items_links)-1)].attrs.get('href',None)
                        if chosen_url:
                            break
                    if 'thing:' in chosen_url:
                        self.item_url = chosen_url
                        return True
        return False

    def get_item_detail(self):
        if self.item_url:
            if not self.item_response:
                self.item_response = self.session.get(self.item_url+'/files')
                self.item_response.html.render(sleep=3)
            meta_tags = self.item_response.html.find('meta')
            title_tag = None
            for tag in meta_tags:
                property_type = tag.attrs.get('property', None)
                if property_type:
                    if property_type.lower() == f'og:title':
                        title_tag = tag

            if title_tag:
                title_tag_text = title_tag.attrs.get('content', None)
                title_beg = 0
                title_end = title_tag_text.find(' by ')
                user_beg = title_tag_text.find(' by ') + 4
                user_end = title_tag_text.find(' - Thingiverse')
                
                self.item_name = title_tag_text[title_beg:title_end]
                self.item_user = title_tag_text[user_beg:user_end]
                return True
        return False

    def get_printable_files(self):
        if self.item_url:
            if not self.item_response:
                self.item_response = self.session.get(self.item_url+'/files')
                self.item_response.html.render(sleep=3)
            files = self.item_response.html.find('a.ThingFile__download--2SUQd')
            list_of_links = {}
            for link in files:
                file_name = link.attrs.get('download', None)
                file_link = link.attrs.get('href', None)
                list_of_links[file_name] =  file_link
            self.files_urls = list_of_links
            return True
        else:
            return False

class Prusa():

    def __init__(self, session, filter):
        self.session = session
        self.filter = filter

        self.item_url = None
        self.files_urls = None
        self.item_name = None
        self.item_user = None
        self.item_response = None
    
    def find_random_print(self, times_to_try):
        if self.session:
            for ind in range(0,times_to_try):
                print_and_log(ind, end='\r')
                if self.filter:
                    filter_options = ['&o=popular', '&o=latest', '&o=rating', '']
                    url = f'https://www.prusaprinters.org/search/prints?q={self.filter.lower()}{filter_options[randint(0,len(filter_options)-1)]}'
                else:
                    url = f'https://www.prusaprinters.org/prints?o=random'
                logger.info(f'Search URL: {url}')
                response = self.session.get(url)
                res_code = response.status_code
                if res_code == 200:
                    response.html.render(sleep=3)
                    all_links = response.html.find('a')
                    items_links = []
                    for link in all_links:
                        if link.attrs.get('href', None):
                            if '/prints/' in link.attrs.get('href', None):
                                items_links.append(link)
                    for ind in range(0,len(items_links)-1):
                        chosen_url = ("https://www.prusaprinters.org" + 
                                    items_links[randint(0,len(items_links)-1)].attrs.get('href',None))
                        if chosen_url:
                            break
                    if '/prints/' in chosen_url:
                        self.item_url = chosen_url
                        return True
        return False

    def get_item_detail(self):
        if self.item_url:
            if not self.item_response:
                self.item_response = self.session.get(self.item_url+'/files')
                self.item_response.html.render(sleep=3)
            title_tag = self.item_response.html.find('title', first=True)

            if title_tag:
                title_tag_text = title_tag.text
                title_beg = 0
                title_end = title_tag_text.find(' by ')
                user_beg = title_tag_text.find(' by ') + 4
                user_end = title_tag_text.find(' |')
                
                self.item_name = title_tag_text[title_beg:title_end]
                self.item_user = title_tag_text[user_beg:user_end]
                return True

        return False

    def get_printable_files(self):
        if self.item_url:
            if not self.item_response:
                self.item_response = self.session.get(self.item_url+'/files')
                self.item_response.html.render(sleep=3)
            files = self.item_response.html.find('a.btn-download')
            list_of_links = {}
            for link in files:
                if link.attrs.get('href', None):
                    file_name = link.attrs.get('href', None)[link.attrs.get('href', None).rfind('/')+1:]
                    file_link = link.attrs.get('href', None)
                    list_of_links[file_name] =  file_link
            self.files_urls = list_of_links
            return True
        else:
            return False

available_services = {
    'thingiverse':Thingiverse,
    'prusa':Prusa,
}