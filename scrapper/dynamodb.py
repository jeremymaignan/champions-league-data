import boto3

class DynamoDB():
    def __init__(self, url, region):
        client = boto3.resource(
            'dynamodb',
            endpoint_url=url,
            region_name=region
        )
        self.tables = {
            "matches": client.Table("matches"),
            "clubs": client.Table("clubs")
        }

    def batch_insert(self, items, tablename):
        with self.tables[tablename].batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
