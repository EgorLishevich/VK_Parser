import requests


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

for user_id in id_data:
    member_response = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': TOKEN_USER,
            'v': VERSION,
            'user_ids': user_id,
            'fields': 'counters'
        }
    )
    print(member_response.json())
