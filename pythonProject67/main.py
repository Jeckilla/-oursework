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
        return photos_for_upload


class YaDiskUploader:
    def __init__(self, token: str):
        self.token = token
        self.url = 'https://cloud-api.yandex.net/v1/disk'

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": disk_file_path}
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        href = data.get('href')
        return href

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def create_folder(self, name_folder):
        url_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': name_folder}
        response = requests.put(url_folder, headers=headers, params=params)
        if response.status_code == 201:
            print(f'Success created folder {name_folder}')
        else:
            print(response.status_code)

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self.get_upload_link(disk_file_path=disk_file_path)
        headers = self.get_headers()
        params = {'file_path': disk_file_path, 'name': filename, 'overwrite': 'True'}
        response = requests.put(href, headers=headers, params=params, data=open(filename, 'rb'))
        if response.status_code == 201:
            print('Success')
        else:
            print(response.status_code)


if __name__ == '__main__':
    ya = YaDiskUploader(token=TOKEN)
    vk_user = VkUser(token=vk_token, version='5.131')

    ID = input('Введите ID пользователя VK: ')
    name_folder = input('Введите название папки для сохранения фото на Яндекс.Диск: ')
    photos = int(input('Введите количество фото, которые хотите загрузить: '))

    uploaded_photos = []
    ya.create_folder(name_folder)
    counter = 0
    for i in range(photos + 1):
        while counter <= i:
            for j in tqdm(vk_user.photo_vk(ID)):
                for filename, size in j.items():
                    disk_file_path = (f'{name_folder}/{filename}')
                    ya.upload_file_to_disk(disk_file_path, filename)

                    json_uploaded = {
                        "file_name": filename,
                        "size": size
                    }
                    uploaded_photos.append(json_uploaded)
                    counter += 1
                    print(j)

    with open('all_url_load.json', 'w') as f:
        json.dupm(uploaded_photos, f, indent=2, ensure_ascii=False)
