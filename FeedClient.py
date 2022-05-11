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
        self.news_container = feed_db.get_container_client("news")
        self.following_container = feed_db.get_container_client("following")

    def get_follower_uids(self, uid):
        key = str(uid)
        try:
            response = self.follow_container.read_item(item=key, partition_key=key)
            value = response.get("follower_uids")
        except exceptions.CosmosHttpResponseError as e:
            value = []
        return value

    def get_news_rids(self, uid):
        key = str(uid)
        try:
            response = self.news_container.read_item(item=key, partition_key=key)
            value = response.get("rids")
        except exceptions.CosmosHttpResponseError as e:
            value = []
        return value

    def get_following_uids(self, uid):
        key = str(uid)
        try:
            response = self.following_container.read_item(item=key, partition_key=key)
            value = response.get("following_uids")
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

    def add_following_uid(self, uid, following_uid):
        following_uids = self.get_following_uids(uid)
        if following_uids is None:
            following_uids = [following_uid]
        elif following_uid not in following_uids:
            following_uids.append(following_uid)

        body = self._construct_following_body(str(uid), following_uids)
        self.following_container.upsert_item(body=body)

    def remove_follower_uid(self, uid, follower_uid):
        follower_uids = self.get_follower_uids(uid)

        if follower_uids is None or (follower_uid not in follower_uids):
            return

        follower_uids.remove(follower_uid)
        body = self._construct_follower_body(str(uid), follower_uids)
        self.follow_container.upsert_item(body=body)

    def remove_following_uid(self, uid, following_uid):
        following_uids = self.get_following_uids(uid)

        if following_uids is None or (following_uid not in following_uids):
            return

        following_uids.remove(following_uid)
        body = self._construct_following_body(str(uid), following_uids)
        self.following_container.upsert_item(body=body)

    def remove_news_rid(self, uid, rid):
        rid = int(rid)
        rids = self.get_news_rids(uid)

        if rids is None or (rid not in rids):
            return

        rids.remove(rid)
        body = self._construct_news_body(str(uid), rids)
        self.news_container.upsert_item(body=body)

    def _construct_follower_body(self, key, val):
        return {
            "id": key,
            "follower_uids": val
        }

    def _construct_news_body(self, key, val):
        return {
            "id": key,
            "rids": val
        }

    def _construct_following_body(self, key, val):
        return {
            "id": key,
            "following_uids": val
        }


# if __name__ == "__main__":
#     config = Config()
#     c = FeedClient(config)
#     # c.remove_follower_uid(1, 4)
#     # c.remove_news_rid(1, 1)
#     c.remove_following_uid(4, 3)
#     print(c.get_following_uids(4))