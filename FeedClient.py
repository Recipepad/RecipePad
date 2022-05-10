import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
# from config import Config


class FeedClient:
    def __init__(self, config):
        client = cosmos_client.CosmosClient(
            config.cosmos_uri,
            {'masterKey': config.cosmos_key},
            user_agent="CosmosDBPythonQuickstart",
            user_agent_overwrite=True
        )

        feed_db = client.get_database_client("feed")
        self.follow_container = feed_db.get_container_client("follow")

    def get_follower_uids(self, uid):
        key = str(uid)
        try:
            response = self.follow_container.read_item(item=key, partition_key=key)
            value = response.get("follower_uids")
        except exceptions.CosmosHttpResponseError as e:
            value = []
        return value

    def add_follower_uid(self, uid, follower_uid):
        follower_uids = self.get_follower_uids(uid)
        if follower_uids is None:
            follower_uids = [follower_uid]
        elif follower_uid not in follower_uids:
            follower_uids.append(follower_uid)

        body = self._construct_follower_body(str(uid), follower_uids)
        self.follow_container.upsert_item(body=body)

    def remove_follower_uid(self, uid, follower_uid):
        follower_uids = self.get_follower_uids(uid)

        if follower_uids is None or (follower_uid not in follower_uids):
            return

        follower_uids.remove(follower_uid)
        body = self._construct_follower_body(str(uid), follower_uids)
        self.follow_container.upsert_item(body=body)

    def _construct_follower_body(self, key, val):
        return {
            "id": key,
            "follower_uids": val
        }


# if __name__ == "__main__":
#     config = Config()
#     c = FeedClient(config)
#     c.remove_follower_uid(1, 4)
#     print(c.get_follower_uids(1))