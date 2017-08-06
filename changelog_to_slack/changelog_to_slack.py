#!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils


def check_software():
    """Get function names from config[urls] and execute them.

    :return: None
    """
    for soft in utils.config.items('urls'):
        name = soft[0]
        data = getattr(utils, name)()
        if data:
            utils.send_to_slack(data)


def main():
    check_software()


if __name__ == "__main__":
    main()
