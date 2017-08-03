#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import umsgpack
from slacker import Slacker

slack = Slacker('xoxb-57729-fbI2sJhNImcQ290w11FjhREf')
software = {'linux_kernel': 'https://www.kernel.org/releases.json',
            }
database = 'changelog-to-slack.bin'

def send_to_slack(data):
    result = slack.chat.post_message('#admins', u'Ура! Появилась новая версия {name}!\n'
                                       u'Версия: {version}\n'
                                       u'Дата релиза: {date}'
                                       u'Лог изменений: {changelog}\n'.format(name=data['name'], version=data['version'],
                                                                    changelog=data['changelog_url'],
                                                                    date=data['date']),
                            as_user=True)
    if result:
        store_log(data['name'], data['version'])


def get(url):
    try:
        r = requests.get(url)
    except requests.exceptions:
        return False
    if r.status_code == 200:
        return r
    else:
        return False


def linux_kernel(url):
    content = get(url)
    if content:
        json_content = content.json()
        latest_stable_ver = json_content['latest_stable']['version']
        for release in json_content['releases']:
            if release['version'] == latest_stable_ver:
                released = release['released']['isodate']
                changelog_url = release['changelog']
                return {'name':linux_kernel, 'version': latest_stable_ver, 'date': released, 'changelog_url': changelog_url}

    return False


def store_log(name, version):
    try:
        with open(database, 'ab+') as fh:
            data = umsgpack.unpack(fh)
            version_list = data
            data_to_pack = {'name': name, 'version': version}


def check_log(name, version):
    try:
        with open(database, 'rb') as fh:
            try:
                data = umsgpack.unpack(fh)
                software_list = data['name']
                if version in software_list:
                    return True
            except KeyError:
                pass
    except EnvironmentError as e:
        print(e)
    return False

def check_software(name, url):
    if name == 'linux_kernel':
        data = linux_kernel(url)
        if data:
            send_to_slack(data)





def main():
    for soft in software:
        check_software(soft, software[soft])


if __name__ == "__main__":
    main()