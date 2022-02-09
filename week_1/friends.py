import re
import requests
import datetime
import json


def calc_age(uid):
    now = datetime.datetime.now()
    now_year = now.strftime('%Y')
    match = re.findall(r'^\d+$', str(uid))
    payload = {'v': '5.81',
               'access_token': '3e68c8273e68c8273e68c827b23e120d3f33e683e68c8275fb13b8cdf02e1a9dbf82625',
               'user_ids': uid
               }
    payload1 = {'v': '5.81',
               'access_token': '3e68c8273e68c8273e68c827b23e120d3f33e683e68c8275fb13b8cdf02e1a9dbf82625',
               'user_id': uid,
               'fields': 'bdate'
               }
    if match:
        pass
    else:
        req = requests.get('https://api.vk.com/method/users.get', params=payload)
        obj = json.loads(req.text)
        # print(obj.text)
        obj = [i['id'] for i in obj['response']]
        payload['user_ids'] = int(*obj)
        payload1['user_id'] = int(*obj)
    req = requests.get('https://api.vk.com/method/users.get', params=payload)
    # print(req.content)
    # print(req.text)
    # print(payload)
    req1 = requests.get('https://api.vk.com/method/friends.get', params=payload1)
    # print(req1.text)
    # print(req1.status_code)
    obj = json.loads(req1.text)
    # print(obj.get('error', ''))
    # print(type(obj))
    if not obj.get('error', ''):
        # print(obj['response']['items'])
        bdate = []
        pattern = re.compile(r'\d{1,2}\.\d{1,2}\.(\d{4})')
        for i in obj['response']['items']:
            # print(i)
            fdate = i.get('bdate', '')
            match = re.findall(pattern, fdate)
            if match:
                age = int(now_year) - int(*match)
                bdate.append(age)
        # print(bdate)
        unique_age = set(bdate)
        distribution_ages_friends = {}
        for i in unique_age:
            distribution_ages_friends[i] = 0
        # print(distribution_ages_friends)
        for i in bdate:
            if i in distribution_ages_friends.keys():
                distribution_ages_friends[i] += 1
        # print(distribution_ages_friends)
        result = list(distribution_ages_friends.items())
        return sorted(result, key=lambda x: (-x[1], x[0]))
    return obj

if __name__ == '__main__':
    res = calc_age('sanjose77')
    print(res)




