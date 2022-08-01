from __future__ import print_function
import json
from concurrent.futures import ThreadPoolExecutor
import generateData as gd
from faker import Faker
import pandas as pd
from collections import defaultdict 
from sqlalchemy import create_engine
from datetime import date, datetime, timedelta
from dateutil import parser
import numpy as np


fake = Faker()

mysql_host = 'localhost'
mysql_port = 33060

mysql_client = mysql.connector.connect(user='glovo',
                                       password='glovo',
                                       database='glovo',
                                       host=mysql_host,
                                       port=mysql_port)
engine = create_engine('mysql://glovo:glovo@localhost:33060/glovo', echo=False)

buffer = []
storeIds = [fake.random_int(20, 30) for i in range(10)]

with ThreadPoolExecutor(1000) as executor:
    for storeId in storeIds:
        addressIds = [fake.random_int(90, 100) for i in range(3)]
        for addressId in addressIds:
            print("Generating orders for store {}, address {}".format(storeId, addressId))
            for i in range(10000):
                buffer.append(gd.createOrder(storeId, addressId))
                if i % 500 == 0:
                    # executor.submit(mysql_processor.bulk, mysql_client, buffer.copy())
                    mysql_processor.bulk(mysql_client, buffer)
                    buffer = []
            print("Completed generating orders")
                # if(len(buffer) % 1000 == 0):
                #     executor.submit(mysql_processor.processOrderBulk, mysql_client, [b for b in buffer])

cursor.close()
mysql_client.close()