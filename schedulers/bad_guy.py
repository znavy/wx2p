import time
import json
import pandas as pd
import requests as r

from lib.deploy import Deploy


def find_bad_guy(wecp):
    lte = int(time.time()*1000)
    gte = lte - (60*1000)
    range = {
        'range': {'@timestamp': {'format': 'epoch_millis', 'gte': gte, 'lte': lte}}}
    must = [range]
    size = 10
    threshold = 500

    params = {'aggs': {'3': {'terms': {'field': 'geoip.ip',
                                       'order': {'_count': 'desc'},
                                       'size': size}}},
              'query': {'filtered': {'filter': {'bool': {'must': must,
                                                         'must_not': []}},
                                     'query': {'query_string': {'analyze_wildcard': True, 'query': '*'}}}},
              'size': 0}

    url = 'http://10.0.0.28:9200/logstash-ows/nginx_ows/_search'

    try:
        resp = r.get(url, json=params)
        data = json.loads(resp.text)
        failed = data['_shards']['failed']
        total = data['hits']['total']
        if failed == 0 and total > 0:
            buckets = data['aggregations']['3']['buckets']

            # print data['aggregations']
            df = pd.DataFrame(buckets)
            ret = list(df[df['doc_count'] > threshold]['key_as_string'])

            if len(ret) > 0:
                access_token = wecp.get_access_token()
                content = 'Some bad guys are attacking us: \n' + '\n'.join(ret)
                wecp.send_msg2user(
                    access_token, content, to_user=['heruihong'], to_ptmt=None)
                _add_black_ip(ret)
    except:
        raise


def _add_black_ip(iplist):
    deploy = Deploy()
    for ip in iplist:
        deploy.black_ip(ip)


if __name__ == '__main__':
    find_bad_guy()
