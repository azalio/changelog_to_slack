# -*- coding: utf-8 -*-
import requests
from slacker import Slacker
from slacker import Error as slacker_errors
import umsgpack
import sys, os
import datetime

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

config_path = os.getenv('HOME') + '/.changelog_to_slack.ini'
user_data_dir = os.getenv('HOME') + '/.changelog_to_slack'
config = configparser.ConfigParser()
config.read(config_path)

slack_token = config.get("slack", "slack_token")
slack = Slacker(slack_token)
slack_channel = config.get("slack", 'channel')
database = os.path.join(user_data_dir, 'changelog_to_slack.bin')


def get(url):
    """Get request object

    :param url: url where we can get information
    :return: request object or False if any errors
    """
    try:
        r = requests.get(url)
    except requests.exceptions:
        return False
    if r.status_code == 200:
        return r
    else:
        print("Some errors while request, http code is: {http_code}".format(r.status_code))
        return False


def send_to_slack(data):
    """Send message to Slack

    :param data: dict. Params: name of soft, version, release date, changelog url.
    :return: None
    """

    result = None
    if not check_log(data['name'], data['version']):
        try:
            result = slack.chat.post_message(slack_channel, u'Появилась новая версия *{name}*!\n'
                                                            u'Версия: *{version}*\n'
                                                            u'Дата релиза: *{date}*\n'
                                                            u'Лог изменений: {changelog}\n'.format(name=data['name'],
                                                                                                   version=data[
                                                                                                       'version'],
                                                                                                   changelog=data[
                                                                                                       'changelog_url'],
                                                                                                   date=data['date']),
                                             as_user=True)
        except slacker_errors as ex:
            if ex.message == 'invalid_auth':
                print("You need write to config file {config_file} correct slack token".format(config_file=config_path))
            elif ex.message == 'channel_not_found':
                print(
                    "You need write to config file {config_file} "
                    "correct slack channel and invite bot to this channel".format(
                        config_file=config_path))
            else:
                print("Got some errors: {error}".format(error=ex.message))

        if result:
            store_log(data['name'], data['version'])


def store_log(name, version):
    """Store information about release.

    :param name: name of soft
    :param version: soft version
    :return: None
    """
    data = extract_data()
    version_list = data.get(name, [])
    version_list.append(version)

    with open(database, 'wb') as fh:
        data[name] = version_list
        print(data)
        umsgpack.pack(data, fh)


def extract_data():
    """Get data dict from database.

    :return: data dict.
    """
    data = {}
    try:
        fh = open(database)
        data = umsgpack.unpack(fh)
        fh.close()
    except IOError:
        pass
    return data


def check_log(name, version):
    """Check for exists in database.

    :param name: name of soft
    :param version: soft version
    :return: True or False
    """
    data = extract_data()
    version_list = data.get(name)
    if version_list and version in version_list:
        return True
    return False


def linux_kernel():
    """Get data about linux kernel.

    :return: dict or False
    """
    url = 'https://www.kernel.org/releases.json'
    content = get(url)
    if content:
        json_content = content.json()
        latest_stable_ver = json_content['latest_stable']['version']
        for release in json_content['releases']:
            if release['version'] == latest_stable_ver:
                released = release['released']['isodate']
                changelog_url = release['changelog']
                return {'name': 'linux_kernel', 'version': latest_stable_ver, 'date': released,
                        'changelog_url': changelog_url}
    return False


def kubernetes():
    """Get data about k8s.

    :return: dict or False
    """
    url = config.get('urls', 'kubernetes')
    content = get(url)
    last_version = content.text.strip()
    changelog_url = 'https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG.md#' + last_version.replace('.', '')
    if content:
        return {'name': 'k8s', 'version': last_version, 'date': datetime.datetime.today().strftime('%Y-%m-%d'),
                'changelog_url': changelog_url}
    return False
