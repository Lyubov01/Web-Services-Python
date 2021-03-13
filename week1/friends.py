import requests
import json
from datetime import datetime


class User:
    def __init__(self, uid):
        self.uid = uid
        self.token = '9edcc23b9edcc23b9edcc23b209eaa191d99edc9edcc23bfe90cb9b8eee27396f82c394'

    @property
    def get_user_id(self):
        r = json.loads(requests.get("https://api.vk.com/method/users.get?user_ids={0}&fields=bdate&"
                                   "access_token=17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711&"
                                   "v=5.71".format(self.uid)).text)
        k = r['response'][0]['id']
        return k

    @property
    def get_user_friends(self):
        friends = json.loads(requests.get("https://api.vk.com/method/friends.get?user_id={0}&fields=bdate&"
                     "access_token=17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711&"
                     "v=5.71".format(self.get_user_id)).text)
        return friends['response']['items']

    @staticmethod
    def is_valid(date):
        if len(date.split('.')) == 3:
            return True
        return False

    @property
    def get_friends_birthday(self):
        birthdays = list()
        for friend in self.get_user_friends:
            if friend.get('bdate', None) is not None and User.is_valid(friend.get('bdate')):
                birthdays.append(friend.get('bdate'))
        return birthdays

    @property
    def get_friends_age_now(self):
        ages_list = list()
        for date_ in self.get_friends_birthday:
            date_ = date_.split('.')

            age = datetime.now().year - int(date_[2])
            ages_list.append(age)
        return ages_list


def calc_age(uid):
    user = User(uid)
    ages = user.get_friends_age_now
    return_dict = {}
    for age in ages:
        if age in return_dict.keys():
            return_dict[age] += 1
        else:
            return_dict[age] = 1

    tuple_list = [(key, value) for key, value in return_dict.items()]
    tuple_list.sort(key=lambda x:(x[1], -x[0]), reverse=True)
    return tuple_list


if __name__ == '__main__':

    print(calc_age('reigning'))
