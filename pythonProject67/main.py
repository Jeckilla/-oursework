import requests
from pprint import pprint
from my_token import access_token as vk_token
from access_token import ya_token as TOKEN
import yadisk
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
        for i in all_photos:
            photos_best = {}
            for j in i['sizes']:
                for k, t in j.items():
                    if k == 'type' and t == 'x':
                        url_photo = (j['url'])
                        likes = str(i['likes']['count'])
                        size = str(j['type'])
                        title_jpg = likes + '.jpg'
                        photos_best[title_jpg] = url_photo
                        photos_best[size] = t

            return photos_best


class YaDiskUploader:
    def __init__(self, token: str):
        self.token = token
        self.url = 'https://cloud-api.yandex.net/v1/disk'

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_upload_link(self, disk_file_path, vk_url):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": disk_file_path, "url": vk_url}
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        href = data.get('href')
        return href

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename, href):
        href = self.get_upload_link(disk_file_path, vk_url)
        headers = self.get_headers()
        params = {'file_path': disk_file_path, 'url': vk_url, 'name': filename, 'overwrite': 'True'}
        response = requests.post(href, headers=headers, params=params)
        if response.status_code == 201:
            print('Success')
        else:
            print(response.status_code)


if __name__ == '__main__':
    ya = YaDiskUploader(token=TOKEN)
    vk_user = VkUser(token=vk_token, version='5.131')
    ID = input('Введите ID пользователя VK: ')
    y = yadisk.YaDisk(token=TOKEN)
    print(y.mkdir('Avatars_from_VK2'))
    for filename, vk_url in tqdm(vk_user.photo_vk(ID).items()):
        disk_file_path = (f'Avatars_from_VK2/{filename}')
        ya.upload_file_to_disk(disk_file_path, filename, vk_url)
        with open('all_url_load.txt', 'a') as f:
            for filename in vk_user.photo_vk(ID).items():
                f.write(f'\n {filename}')



