SOURCE=postgres YEAR=2025 MONTH=01 DAY=03 meltano run tap-postgres target-parquet

SOURCE=csv YEAR=2025 MONTH=01 DAY=01 meltano run tap-csv target-parquet


meltano
meltano lock --update --all
meltano install

airflow
meltano invoke airflow:initialize
meltano invoke airflow users create -u admin@localhost -p password --role Admin -e admin@localhost -f admin -l admin
