SOURCE=postgres YEAR=2025 MONTH=01 DAY=03 meltano run tap-postgres target-parquet

SOURCE=csv YEAR=2025 MONTH=01 DAY=01 meltano run tap-csv target-parquet


meltano
meltano lock --update --all
meltano install

airflow
meltano invoke airflow:initialize
meltano invoke airflow users create -u admin@localhost -p password --role Admin -e admin@localhost -f admin -l admin

streamlit app
http://172.19.0.3:8501

webserver
se: Error: Already running on PID 15 (or pid file '/project/orchestrate/airflow/airflow-webserver.pid' is stale
make down
sudo lsof -i tcp:8080
sudo kill -9 PID -- se houver algo usando porta 8080
deletar o arquivo airflow-webserver.pid
make up
