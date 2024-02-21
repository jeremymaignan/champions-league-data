MATCHES_TABLE_NAME="matches"
CLUBS_TABLE_NAME="clubs"
REGION="us-west-2"

# Wait for DynamoDB Local to be ready
until aws dynamodb list-tables  --region $REGION --endpoint-url $DYNAMO_ENDPOINT > /dev/null 2>&1; do
    echo "Waiting for DynamoDB Local to be ready..."
    sleep 1
done

# Check if the table already exists
aws dynamodb describe-table --region $REGION --endpoint-url $DYNAMO_ENDPOINT --table-name $MATCHES_TABLE_NAME > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # Table does not exist, so create it
    aws dynamodb create-table \
        --region $REGION \
        --table-name $MATCHES_TABLE_NAME \
        --attribute-definitions \
            AttributeName=home_team_id,AttributeType=S \
            AttributeName=away_team_id,AttributeType=S \
            AttributeName=date,AttributeType=S \
        --key-schema \
            AttributeName=home_team_id,KeyType=HASH \
            AttributeName=date,KeyType=RANGE \
        --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
        --global-secondary-indexes \
            IndexName=AwayTeamIndex,KeySchema=["{AttributeName=away_team_id,KeyType=HASH}","{AttributeName=date,KeyType=RANGE}"],Projection="{ProjectionType=ALL}",ProvisionedThroughput="{ReadCapacityUnits=5,WriteCapacityUnits=5}" \
        --endpoint-url $DYNAMO_ENDPOINT
    echo "DynamoDB table $MATCHES_TABLE_NAME created."
else
    echo "Table $MATCHES_TABLE_NAME already exists."
fi

# Check if the table already exists
aws dynamodb describe-table --region $REGION --endpoint-url $DYNAMO_ENDPOINT --table-name $CLUBS_TABLE_NAME > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # Table does not exist, so create it
    aws dynamodb create-table \
        --region $REGION \
        --table-name $CLUBS_TABLE_NAME \
        --attribute-definitions \
            AttributeName=id,AttributeType=S \
        --key-schema \
            AttributeName=id,KeyType=HASH \
        --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
        --endpoint-url $DYNAMO_ENDPOINT
    echo "DynamoDB table $CLUBS_TABLE_NAME created."
else
    echo "Table $CLUBS_TABLE_NAME already exists."
fi

# Start the scrapper
cd /var/app/scrapper/ && time python3.7 main.py && echo "Messages loaded" || echo "Fail to load messages"
