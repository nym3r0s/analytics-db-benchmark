curl --location --request GET 'https://vpc-partner-dashboard-prod-6xzceyy35w5r2bpzrzx4osbsb4.eu-west-1.es.amazonaws.com/order/_search?size=2000&from=0&sort=creationTime:asc' \
--header 'Content-Type: application/json' \
--data-raw '{
    "query": {
        "bool": {
            "must": { 
                "range": {
                    "dispatchingTime": {
                        "gte": "now-10d/d",
                        "lt": "now+2d/d"
                    }
                }
            },
            "should": [
                {
                    "term": {
                        "storeAddressId": 43766
                    }
                },
                {
                    "term": {
                        "storeAddressId": 194449
                    }
                }, 
                {
                    "term": {
                        "storeAddressId": 191768
                    }
                },
                {
                    "term": {
                        "storeAddressId": 61698
                    }
                },
                {
                    "term": {
                        "storeAddressId": 72152
                    }
                } ,
                {
                    "term": {
                        "storeAddressId": 303049
                    }
                },
                {
                    "term": {
                        "storeAddressId": 289571
                    }
                },
                {
                    "term": {
                        "storeAddressId": 107689
                    }
                },
                {
                    "term": {
                        "storeAddressId": 61706
                    }
                },
                {
                    "term": {
                        "storeAddressId": 61469
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }
}'