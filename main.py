import requests
import time


TOKEN_USER = '40ded58740ded58740ded5877543c7ef12440de40ded587265b13062271608f02ab200a'
VERSION = '5.199'
DOMAIN = 'streaminside'

group_response = requests.get(
    'https://api.vk.com/method/groups.getMembers',
    params={
        'access_token': TOKEN_USER,
        'v': VERSION,
        'group_id': DOMAIN,
    }
)
id_data = group_response.json()['response']['items']

try:
    for user_id in id_data:
        member_response = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'access_token': TOKEN_USER,
                'v': VERSION,
                'user_ids': user_id,
                'fields': 'counters, city, last_seen'
            }
        )
        data = member_response.json()['response'][0]
        print(
            f'Фамилия: {data["last_name"]} Имя: {data["first_name"]}'
        )
        time.sleep(0.1)
except KeyError:
    pass
