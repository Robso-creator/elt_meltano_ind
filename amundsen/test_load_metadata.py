import yaml
from pyhocon import ConfigFactory
from databuilder.loader.file_system_neo4j_csv_loader import FsNeo4jCSVLoader
from databuilder.publisher.neo4j_csv_publisher import Neo4jCsvPublisher
from databuilder.transformer.base_transformer import NoopTransformer
from databuilder.task.task import DefaultTask
from databuilder.extractor.generic_extractor import GenericExtractor

# Ler o YAML
with open("table_metadata.yaml", "r") as file:
    table_metadata = yaml.safe_load(file)

# Criar configuração do Databuilder
config = ConfigFactory.from_dict({
    "extractor.generic.table_metadata": table_metadata
})

# Criar um extractor de metadados genérico
extractor = GenericExtractor()
extractor.init(conf=config)

# Criar tarefa de carga de dados no Amundsen
task = DefaultTask(extractor=extractor, transformer=NoopTransformer(), loader=FsNeo4jCSVLoader())

# Executar a tarefa
task.execute()

# Publicar no Neo4j
publisher = Neo4jCsvPublisher()
publisher.publish()
