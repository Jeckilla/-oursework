import requests
from pprint import pprint
from my_token import access_token as vk_token
from access_token import ya_token as TOKEN
import json
from tqdm import tqdm


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': vk_token,
            'v': '5.131'
        }

    def photo_vk(self, ID):
        URL = 'https://api.vk.com/method/photos.get'

        params_photo = {
            'owner_id': ID,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1
        }
        res = requests.get(URL, params={**self.params, **params_photo}).json()
        all_photos = res['response']['items']
        photos_for_upload = []
        photos_for_upload_sort = sorted(photos_for_upload, reverse=True)
        for i in all_photos:
            for j in i['sizes']:
                for k, t in j.items():
                    if k == 'type' and (t == 'w' or t == 'z'):
                        url_photo = (j['url'])
                        date = str(i['date'])
                        likes = str(i['likes']['count'])
                        size = str(j['type'])
                        title_jpg = likes + '_' + date + '.jpg'
                        photos_best = {
                            title_jpg: url_photo,
                            'size': size
                        }
                        photos_for_upload.append(photos_best)
                        with open(f'{title_jpg}', 'wb') as file:
                            response = requests.get(url_photo)
                            file.write(response.content)
        return photos_best

vk_user = VkUser()
print = vk_user.photo_vk(325754)