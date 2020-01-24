#import mysql.connector as mysql
import pymysql
import time
import json

master_timer_start = time.time()

###################################################################
client_config = {'unix_socket':'/var/run/mysqld/mysqld.sock',
                'database':'test_wos_cut_full'}

db = pymysql.connect(**client_config)
cursor = db.cursor()

# print the table names
sql_query = 'SHOW tables'
cursor.execute(sql_query)

for element in cursor:
    print(element)

cursor.close()
db.close()


###################################################################
# add index to SOURCE field of publications

start_time = time.time()

db = pymysql.connect(**client_config)
cursor = db.cursor()

sql_query = 'CREATE FULLTEXT INDEX pub_source_idx ON publications (source)'
cursor.execute(sql_query)

cursor.close()
db.commit()
db.close()

end_time = time.time()
print('elapsed s: {}'.format(end_time - start_time))



###################################################################
# add index to wos_id field of publications

start_time = time.time()

db = pymysql.connect(**client_config)
cursor = db.cursor()

sql_query = 'CREATE INDEX wos_id_idx ON publications (wos_id(50))'
cursor.execute(sql_query)

cursor.close()
db.commit()
db.close()

end_time = time.time()
print('elapsed s: {}'.format(end_time - start_time))

###################################################################
# add index to PUBYEAR field of publications

start_time = time.time()

db = pymysql.connect(**client_config)
cursor = db.cursor()

sql_query = 'CREATE INDEX pub_year_idx ON publications (pubyear)'
cursor.execute(sql_query)

cursor.close()
db.commit()
db.close()

end_time = time.time()
print('elapsed s: {}'.format(end_time - start_time))



###################################################################
# contributors:  first name, last name, wos_id

start_time = time.time()

db = pymysql.connect(**client_config)
cursor = db.cursor()

sql_query = 'CREATE INDEX first_name_idx ON contributors (first_name(50))'
cursor.execute(sql_query)

cursor.close()
db.commit()
db.close()

end_time = time.time()
print('elapsed s: {}'.format(end_time - start_time))



###################################################################
start_time = time.time()

db = pymysql.connect(**client_config)
cursor = db.cursor()

sql_query = 'CREATE INDEX last_name_idx ON contributors (last_name(50))'
cursor.execute(sql_query)

cursor.close()
db.commit()
db.close()

end_time = time.time()
print('elapsed s: {}'.format(end_time - start_time))


###################################################################
start_time = time.time()

db = pymysql.connect(**client_config)
cursor = db.cursor()

sql_query = 'CREATE INDEX wos_id_idx ON contributors (wos_id(50))'
cursor.execute(sql_query)

cursor.close()
db.commit()
db.close()

end_time = time.time()
print('elapsed s: {}'.format(end_time - start_time))


###################################################################
# institutions - country, wos_id

start_time = time.time()

db = pymysql.connect(**client_config)
cursor = db.cursor()

sql_query = 'CREATE FULLTEXT INDEX country_idx ON institutions (country(50))'
cursor.execute(sql_query)

cursor.close()
db.commit()
db.close()

end_time = time.time()
print('elapsed s: {}'.format(end_time - start_time))


###################################################################
start_time = time.time()

db = pymysql.connect(**client_config)
cursor = db.cursor()

sql_query = 'CREATE INDEX wos_id_idx ON institutions (wos_id(50))'
cursor.execute(sql_query)

cursor.close()
db.commit()
db.close()

end_time = time.time()
print('elapsed s: {}'.format(end_time - start_time))


###################################################################
start_time = time.time()

db = pymysql.connect(**client_config)
cursor = db.cursor()

sql_query = 'CREATE INDEX source_idx ON the_references (wos_id(50))'
cursor.execute(sql_query)

cursor.close()
db.commit()
db.close()

end_time = time.time()
print('elapsed s: {}'.format(end_time - start_time))


###################################################################
start_time = time.time()

db = pymysql.connect(**client_config)
cursor = db.cursor()

sql_query = 'CREATE INDEX target_idx ON the_references (uid(50))'
cursor.execute(sql_query)

cursor.close()
db.commit()
db.close()

end_time = time.time()
print('elapsed s: {}'.format(end_time - start_time))


###################################################################
db = pymysql.connect(**client_config)
cursor = db.cursor()
sql_query = 'DESCRIBE test_wos'
cursor.execute(sql_query)

for el in cursor:
    print(el)
    
###################################################################

# TODO add indices as needed to speed up test queries

db.close()

###################################################################

master_timer_stop = time.time()
total_elapsed = master_timer_stop - master_timer_start
print('total elapsed time during ingestion: {} s'.format(total_elapsed))

timing_info = {'indexing_time': total_elapsed}
with open('indexing_timer.json','w') as f:
    json.dump(timing_info, f)
               
        
        