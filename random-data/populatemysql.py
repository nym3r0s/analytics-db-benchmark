from __future__ import print_function
import json
from concurrent.futures import ThreadPoolExecutor
import ordergenerator as gd
from faker import Faker
import pandas as pd
from collections import defaultdict 
from sqlalchemy import create_engine
from datetime import date, datetime, timedelta
from dateutil import parser
import numpy as np
import mysql_processor.processor as mysql_processor


fake = Faker()

mysql_host = 'localhost'
mysql_port = 33060

engine = create_engine('mysql+pymysql://glovo:glovo@localhost:33060/glovo', pool_size=100, echo=False)

buffer = []
storeIds = [fake.random_int(20, 30) for i in range(15)]

with ThreadPoolExecutor(1000) as executor:
    for storeId in storeIds:
        addressIds = [fake.random_int(storeId*10, storeId*10 + 10) for i in range(3)]
        for addressId in addressIds:
            print("Generating orders for store {}, address {}".format(storeId, addressId))
            for i in range(100000):
                buffer.append(gd.createOrder(storeId, addressId))
                if i % 2000 == 0:
                    executor.submit(mysql_processor.bulk, engine, buffer.copy())
                    buffer = []
            print("Completed generating orders")

cursor.close()
mysql_client.close()