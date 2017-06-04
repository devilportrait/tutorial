import json
import requests
from lxml import etree
import datetime
import time

if __name__ == '__main__':

    def current_milli_time():
        return int(round(time.time() * 1000))

    # current_milli_time = lambda: int(round(time.time() * 1000))
    print current_milli_time()
