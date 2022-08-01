from __future__ import print_function
from opensearchpy import OpenSearch
import json
import mysql_processor.processor as mysql_processor
import mysql.connector
from concurrent.futures import ThreadPoolExecutor

elastic_host = 'vpc-partner-dashboard-prod-6xzceyy35w5r2bpzrzx4osbsb4.eu-west-1.es.amazonaws.com'
elastic_port = 443

elastic_client = OpenSearch(
    hosts=[{
        'host': elastic_host,
        'port': elastic_port
    }],
    http_compress=True,  # enables gzip compression for request bodies
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False)


body = {
    'query': {
        'bool': {
            'must': {
                'range': {
                    'dispatchingTime': {
                        'gte': 'now-10d/d',
                        'lt': 'now+2d/d'
                    }
                }
            },
            'should': [{
                'term': {
                    'storeAddressId': 43766
                }
            }, {
                'term': {
                    'storeAddressId': 194449
                }
            }, {
                'term': {
                    'storeAddressId': 191768
                }
            }, {
                'term': {
                    'storeAddressId': 61698
                }
            }, {
                'term': {
                    'storeAddressId': 72152
                }
            }, {
                'term': {
                    'storeAddressId': 303049
                }
            }, {
                'term': {
                    'storeAddressId': 289571
                }
            }, {
                'term': {
                    'storeAddressId': 107689
                }
            }, {
                'term': {
                    'storeAddressId': 61706
                }
            }, {
                'term': {
                    'storeAddressId': 61469
                }
            }],
            'minimum_should_match':
            1
        }
    }
}

mysql_host = 'localhost'
mysql_port = 33060

mysql_client = mysql.connector.connect(user='glovo',
                                       password='glovo',
                                       database='glovo',
                                       host=mysql_host,
                                       port=mysql_port)


def scroll(es, index, body, scroll, size, **kw):
    page = es.search(index=index, body=body, scroll=scroll, size=size, **kw)
    scroll_id = page['_scroll_id']
    hits = page['hits']['hits']
    while len(hits):
        yield hits
        page = es.scroll(scroll_id=scroll_id, scroll=scroll)
        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']

for hits in scroll(elastic_client, 'order', body, '10m', 2000):
    # Do something with hits here
        # print(json.dumps(hit, indent=4))
    parsed_hits = [doc['_source'] for doc in hits]
    with ThreadPoolExecutor(100) as executor:
        executor.submit(mysql_processor.processOrderBulk, mysql_client, parsed_hits)
        # mysql_processor.processOrderBulk(mysql_client, parsed_hits)

cursor.close()
mysql_client.close()