from setuptools import setup, find_packages


setup(
    name="changelog_to_slack",
    version="0.0.1",
    author="Mikhail Petrov",
    author_email="azalio@azalio.net",
    description="Check new software version and send to slack channel",
    license="BSD",
    url="https://github.com/azalio/changelog_to_slack",
    packages=find_packages(),
    include_package_data=True,
    package_data={'changelog_to_slack': ['config/*.ini']},
    keywords='slack software_update',
    zip_safe=False,
    install_requires=['slacker>=0.9.50', 'requests>=2.18.2', 'umsgpack>=0.1.0'],
    entry_points={
        'console_scripts': [
            'changelog_to_slack = changelog_to_slack.changelog_to_slack:main',
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
