import boto3

ENDPOINT = "http://localhost:4566"
REGION   = "us-east-1"
CREDS    = dict(aws_access_key_id="test",
                aws_secret_access_key="test",
                region_name=REGION,
                endpoint_url=ENDPOINT)

def provision():
    s3  = boto3.client("s3", **CREDS)
    sqs = boto3.client("sqs", **CREDS)
    sns = boto3.client("sns", **CREDS)
    ddb = boto3.resource("dynamodb", **CREDS)

    s3.create_bucket(Bucket="clwaitoudguard-artifacts")
    sqs.create_queue(QueueName="order-queue")
    sqs.create_queue(QueueName="inventory-queue")
    sqs.create_queue(QueueName="order-queue-dlq")
    sns.create_topic(Name="notifications")
    ddb.create_table(
        TableName="orders",

        KeySchema=[{"AttributeName": "order_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "order_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )

if __name__ == "__main__":
    provision()
    print("Infrastructure ready.")
