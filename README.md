# Analytics DB Benchmark

A comparison between different databases for reporting and analytics use-cases

### Databases being compared

* MySQL
* Clickhouse

### Random Data

* Use the `random-data/populatemysql.py` script to populate the MySQL DB with random data.
* Once MySQL is populated with enough data, export the data and import it into Clickhouse

### Useful commands

* Extract data from MySQL to a TSV file
```shell
mysql --user=glovo --password=glovo --host=0.0.0.0 --port=33060 --database=glovo -Bse "select * from product_issues" > product_issues.tsv
```
* Import data from a TSV file to clickhouse.
```shell
cat product_issues.tsv | clickhouse client --host=0.0.0.0 --port=19000 --user=glovo --password=glovo --query="INSERT INTO glovo.product_issues FORMAT TabSeparated"
```