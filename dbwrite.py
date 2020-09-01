import sys
import logging
import pymysql
import os
from ast import literal_eval

#rds settings
rds_host  = os.environ['db_url']
name = os.environ['db_user']
password = os.environ['db_password']
db_name = os.environ['db_name']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def write_to_db(firstname,lastname):
    with conn.cursor() as cur:
        cur.execute("create table IF NOT EXISTS applicationdata (ID int AUTO_INCREMENT NOT NULL, firstname varchar(255), lastname varchar(255), PRIMARY KEY (ID));")
        cur.execute('insert into applicationdata (firstname,lastname) values(%s,%s)',(firstname,lastname))
        conn.commit()
    conn.commit()

    return "Added data to RDS MySQL table"
