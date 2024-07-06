import time
import requests

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


TOKEN = (
    '40ded58740ded58740ded5877543c7ef12440de40ded587265b13062271608f02ab200a'
)
VERSION = '5.199'

Window.size = (1600, 1400)
Window.clearcolor = (20/255, 20/255, 20/255, 1)
Window.title = 'VK_Parser'


def group_count(group_name):
    '''Сбор общего числа подписчиков паблика'''
    group_count_response = requests.get(
        'https://api.vk.com/method/groups.getMembers',
        params={
            'access_token': TOKEN,
            'v': VERSION,
            'group_id': group_name,
        }
    )
    count = group_count_response.json()['response']['count']
    return count


def group_response(group_name, count):
    '''Сбор id подписчиков'''
    id_data = []
    for i in range(0, count+1, 1000):
        group_response = requests.get(
            'https://api.vk.com/method/groups.getMembers',
            params={
                'access_token': TOKEN,
                'v': VERSION,
                'group_id': group_name,
                'offset': i
            }
        )
        id_datas = group_response.json()['response']['items']
        id_data.append(id_datas)
        time.sleep(0.1)
        return id_data


def user_response(id_data):
    '''Сбор всей необходимой информации'''
    result = []
    while True:
        for user_id in id_data[0]:
            try:
                member_response = requests.get(
                    'https://api.vk.com/method/users.get',
                    params={
                        'access_token': TOKEN,
                        'v': VERSION,
                        'user_id': user_id,
                        'fields': 'counters, city, last_seen'
                    }
                )
                data = member_response.json()['response'][0]
                member_friends_response = requests.get(
                    'https://api.vk.com/method/friends.get',
                    params={
                        'access_token': TOKEN,
                        'v': VERSION,
                        'user_id': user_id,
                    }
                )
                friends_data = member_friends_response.json()[
                    'response'
                ][
                    'count'
                ]
                unix_last_seen_date = float(data['last_seen']['time'])
                time_struct = time.gmtime(unix_last_seen_date)
                last_seen_date = time.strftime(
                    "%B %d %Y %H:%M:%S", time_struct
                )
                response = [
                    f'Ссылка: https://vk.com/id{data["id"]}'
                    f' | Фамилия: {data["last_name"]}'
                    f' | Имя: {data["first_name"]}'
                    f' | Город: {data["city"]["title"]}'
                    f' | Последнее посещение {last_seen_date}'
                    f' | Колл-во друзей: {friends_data}'
                    f' | Колл-во фото: {data["counters"]["photos"]}'
                    f' | Колл-во пабликов: {data["counters"]["groups"]}'
                ]
                result.extend(response)
            except KeyError:
                pass
            if user_id == id_data[-1]:
                return False
        return ('\n'.join(result))


class MyApp(App):
    '''Инициализация интерфейса'''
    def __init__(self):
        super().__init__()
        self.group_name_input = TextInput(
            hint_text='Введите короткое имя или id паблика',
            multiline=False,
            size_hint=(1.0, 0.05),
        )
        self.output = TextInput(
            hint_text='Результат', multiline=True, readonly=True
        )
        self.button = Button(
            text='Подтвердить',
            size_hint=(1.0, 0.05),
            background_color=(1, 1, 1, 1)
        )
        self.group_name_input.bind(text=self.on_text)
        self.button.bind(on_press=self.click)

    def on_text(self, *args):
        group_name = self.group_name_input
        print(group_name.text)

    def click(self, event):
        group_name = self.group_name_input
        count = group_count(group_name.text)
        id_data = group_response(group_name.text, count)
        response = user_response(id_data)
        if response is not None:
            self.output.text = response
        else:
            self.output.text = 'Нет информации'

    def build(self):
        box = BoxLayout(orientation='vertical')
        box.add_widget(self.group_name_input)
        box.add_widget(self.button)
        box.add_widget(self.output)
        return box


if __name__ == "__main__":
    MyApp().run()
