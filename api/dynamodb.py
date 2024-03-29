import boto3

class DynamoDB:
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

    def query_items(self, table, key_condition_expression, expression_attribute_values, index_name=None):
        all_items = []
        last_evaluated_key = None
        params = {
            'KeyConditionExpression': key_condition_expression,
            'ExpressionAttributeValues': expression_attribute_values,
        }
        while True:
            if index_name:
                params['IndexName'] = index_name
            if last_evaluated_key:
                params['ExclusiveStartKey'] = last_evaluated_key

            response = self.tables[table].query(**params)
            items = response.get('Items', [])
            all_items.extend(items)

            last_evaluated_key = response.get('LastEvaluatedKey')
            if not last_evaluated_key:
                break

        return all_items

    def scan_table(self, table):
        all_items = []

        scan_params = {}
        while True:
            response = self.tables[table].scan(**scan_params)
            items = response.get('Items', [])
            all_items.extend(items)

            last_evaluated_key = response.get('LastEvaluatedKey')
            if not last_evaluated_key:
                break

        return all_items
