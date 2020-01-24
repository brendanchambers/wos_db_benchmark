
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
