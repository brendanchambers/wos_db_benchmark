import sqlalchemy
import pandas as pd
#import mysql.connector as mysql
import pymysql
import time
import os
import json

master_timer_start = time.time()


#########################################################################
#      specifies how to recognize the partial file splits:

with open("credentials.json",'r') as f:
    data = json.load(f)
    my_username = str(data['username'])
    my_pwd = str(data['password'])

data_dir = '/mnt/data/study_dbs/data/full_v1/'

pubs_substring = 'wos_cut_publications'  # postfixed with e.g. batch_0.csv
contrib_substring = 'wos_cut_contributors'
inst_substring = 'wos_cut_institutions'
ref_path = 'wos_cut_refs.csv'
wosIDs_path = 'wos_cut_wosids.csv'

# sql alchemy connection string:
db_name = 'test_wos_cut_full'
connect_string = "mysql+pymysql://{}:{}@localhost:/{}?unix_socket=/var/run/mysqld/mysqld.sock".format(my_username, my_pwd, db_name)


#########################################################################
# create the database

client_config = {'unix_socket':'/var/run/mysqld/mysqld.sock',
                'password': my_pwd}
db = pymysql.connect(**client_config)

print('creating database...')

cursor = db.cursor()
sql = "CREATE DATABASE {}".format(db_name)
try:
    cursor.execute(sql)
    print('successfully created.')
except Exception as e:
    print(e)
    print('error during creation of database')
cursor.close()
db.close()


#########################################################################
# build a dictionary for to keep track of file names, etc:

tables = {}
tables['publications'] = {'substring_filemarker':pubs_substring}
tables['contributors'] = {'substring_filemarker':contrib_substring}
tables['institutions'] = {'substring_filemarker':inst_substring}
tables['the_references'] = {'substring_filemarker':ref_path}
tables['wosIDs'] = {'substring_filemarker':wosIDs_path}


#########################################################################
# sort out the matching file splits

all_datafiles = os.listdir(data_dir)

for k, v in iter(tables.items()):
    
    print('processing {} ...'.format(k))
    start_time = time.time()
    
    tables[k]['files'] = [f for f in all_datafiles \
                          if (v['substring_filemarker'] in f)]
    DFs = []
    for filename in tables[k]['files']:
        path = os.path.join(data_dir,filename)
        #print(path)
        DFs.append(pd.read_csv(path, sep=','))

    # join dfs
    df = pd.concat(DFs, axis=0, ignore_index=True)        

    # insert into db
    sql_engine = sqlalchemy.create_engine(connect_string)
    df.to_sql(con=sql_engine,
             name=k,
             if_exists='replace',
             chunksize=50000)
        
    end_time = time.time()
    print('{} ingested in {} s'.format(k, end_time-start_time))

    
#########################################################################
master_timer_stop = time.time()
total_elapsed = master_timer_stop - master_timer_start
print('total elapsed time during ingestion: {} s'.format(total_elapsed))

timing_info = {'ingestion_time': total_elapsed}
with open('ingestion_timer.json','w') as f:
    json.dump(timing_info, f)
               