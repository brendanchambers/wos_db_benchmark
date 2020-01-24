# Instructions for creating the database:

### 1. Ingest

### 2. Add indexes

### 3. Run test queries





# connection info
### this is for running on RCC midway2



Example configuration file
_________________________________________________
[mysqld]
socket=/project2/jevans/study_dbs/mysql/.sql.sock
datadir=/project2/jevans/study_dbs/mysql/mysql_data
max_connections=56
max_allowed_packet=16G
innodb_buffer_pool_size=512M
net_read_timeout=1000

[client]
socket=/project2/jevans/study_dbs/mysql/.sql.sock
max_allowed_packet=1G
_________________________________________________












MySQL config file:  .shared.cnf

Socket:   .sql.sock


In a compute node:
Launch mysql server:
  mysqld --defaults-file=/project2/jevans/study_dbs/mysql/.shared.cnf &
In a different terminal on the same compute node:
Launch mysql client:
  mysql --defaults-file=/project2/jevans/study_dbs/mysql/.shared.cnf &


More information:
Check out the great mysql on RCC tutorial from Jeff Tharsen explaining more setup info and
peculiarities.
