# -*- coding: utf-8 -*-

import os

# Create if not exists config file and dir for database

user_config = os.getenv('HOME') + '/.changelog_to_slack.ini'
user_data_dir = os.getenv('HOME') + '/.changelog_to_slack'

if not os.path.exists(user_config):
    changelog_to_slack_config = os.path.join(os.path.dirname(__file__),'config/changelog_to_slack.ini')
    changelog_to_slack_config = open(changelog_to_slack_config).read()
    with open(user_config, 'w') as fh:
        fh.write(changelog_to_slack_config)

if not os.path.exists(user_data_dir):
    os.makedirs(user_data_dir)