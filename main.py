import requests
import time


TOKEN_USER = '40ded58740ded58740ded5877543c7ef12440de40ded587265b13062271608f02ab200a'
VERSION = '5.199'
DOMAIN = 'it_roll'


group_count_response = requests.get(
    'https://api.vk.com/method/groups.getMembers',
    params={
        'access_token': TOKEN_USER,
        'v': VERSION,
        'group_id': DOMAIN,
    }
)
count = group_count_response.json()['response']['count']

id_data = []

for i in range(0, count+1, 1000):
    group_response = requests.get(
        'https://api.vk.com/method/groups.getMembers',
        params={
            'access_token': TOKEN_USER,
            'v': VERSION,
            'group_id': DOMAIN,
            'offset': i
        }
    )
    id_datas = group_response.json()['response']['items']
    id_data.append(id_datas)
    time.sleep(0.1)

for user_id in id_data[0]:
    try:
        member_response = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'access_token': TOKEN_USER,
                'v': VERSION,
                'user_id': user_id,
                'fields': 'counters, city, last_seen'
            }
        )
        data = member_response.json()['response'][0]
        member_friends_response = requests.get(
            'https://api.vk.com/method/friends.get',
            params={
                'access_token': TOKEN_USER,
                'v': VERSION,
                'user_id': user_id,
            }
        )
        friends_data = member_friends_response.json()['response']['count']
        unix_last_seen_date = float(data['last_seen']['time'])
        time_struct = time.gmtime(unix_last_seen_date)
        last_seen_date = time.strftime("%B %d %Y %H:%M:%S", time_struct)
        print(
            f'Ссылка: https://vk.com/id{data["id"]} '
            f'| Фамилия: {data["last_name"]} '
            f'| Имя: {data["first_name"]} '
            f'| Город: {data["city"]["title"]}'
            f'| Последнее посещение {last_seen_date} '
            f'| Колл-во друзей: {friends_data}'
            f'| Колл-во фото: {data["counters"]["photos"]}'
            f'| Колл-во пабликов: {data["counters"]["groups"]}'
        )
    except KeyError:
        pass
