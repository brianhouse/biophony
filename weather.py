#!/usr/bin/env python3

import requests, json, time
from housepy import config, log, util



while True:

    # current conditions
    try:
        url = "http://api.wunderground.com/api/%s/conditions/q/MA/North_Adams.json" % config['wunderground']
        response = requests.get(url)
        data = response.json()['current_observation']
        # log.info(json.dumps(data, indent=4))
        entry = {'t_utc': util.timestamp(), 'type': 'weather', 'temp_f': data['temp_f'], 'wind_mph': data['wind_mph']}
        log.info(json.dumps(entry, indent=4))
        response = requests.post(config['server'], json=entry)
        log.info(response)
    except Exception as e:
        log.error(log.exc(e))

    time.sleep(60)




# # hourly
# url = "http://api.wunderground.com/api/%s/hourly/q/MA/North_Adams.json" % config['wunderground']
# response = requests.get(url)
# data = response.json()
# log.info(json.dumps(data, indent=4))

