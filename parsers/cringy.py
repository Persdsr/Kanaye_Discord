import random

import requests


def get_memes():
    token = '175e41cf175e41cf175e41cf94144fc1de1175e175e41cf742b1c35e95cf87e30174d8c'
    version = 5.131
    domain = 'cringey'

    offset_list = [0, 19, 38, 57, 76, 95, 114, 133, 152, 171, 190, 209, 228, 247, 266, 285, 304]
    ofs = random.randint(0, 16)
    offset = offset_list[ofs]

    r = requests.get('https://api.vk.com/method/wall.get',
                     params={
                         'access_token': token,
                         'v': version,
                         'domain': domain,
                         'offset': offset
                     })

    data = r.json()['response']['items']
    photo = 0
    post_i = data[random.randint(0, 19)]

    try:
        for i in post_i['attachments'][0]['photo']['sizes']:
            if i['type'] == 'z':
                photo = i['url']
            elif i['type'] == 'y':
                photo = i['url']
    except:
        print('Неизвестная ошибка')

    return photo


