import slack_g_cal
import os

from setuptools import setup, find_packages


def local_file(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read()


if __name__ == '__main__':

    setup(
        name='slack_g_cal',
        version=slack_g_cal.__version__,
        description='A slack bot that allows users to intuitively interact with their Google Calendars',
        long_description=local_file('README.md'),
        author='Wes Auyeung',
        url='https://github.com/wfa207/slack_g_cal',
        packages=find_packages(exclude=['*tests*']),
        include_package_data=True,
        classifiers=[
            'Programming Language :: Python',
        ],
    )
