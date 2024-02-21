import boto3
from utils import get_conf

class Dynamodb():
    def __init__(self, url, region):
        db = boto3.resource('dynamodb', endpoint_url=url, region_name=region)
        self.tables = {
            "matches": db.Table(get_conf("dynamodb_matches_table")),
            "clubs": db.Table(get_conf("dynamodb_clubs_table"))
        }

    def batch_insert(self, items, tablename):
        with self.tables[tablename].batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
