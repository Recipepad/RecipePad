import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions


class CosmosClient:
    def __init__(self, config):
        client = cosmos_client.CosmosClient(
            config.cosmos_uri,
            {'masterKey': config.cosmos_key},
            user_agent="CosmosDBPythonQuickstart",
            user_agent_overwrite=True
        )
        db = client.get_database_client(config.cosmos_db)
        self.container = db.get_container_client(config.cosmos_container)

    def get_rids(self, keyword):
        key = str(keyword)
        try:
            response = self.container.read_item(item=key, partition_key=key)
            value = response.get("rids")
        except exceptions.CosmosHttpResponseError as e:
            value = []
        return value

