import boto3


def create_nodes_resource_table():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName='NodesResources',
        KeySchema=[
            {
                'AttributeName': 'NodeId',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Timestamp',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'NodeId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Timestamp',
                'AttributeType': 'S'
            },
        ],
        BillingMode='PROVISIONED',
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
        TableClass='STANDARD'
    )
    return table


if __name__ == '__main__':
    node_resources_table = create_nodes_resource_table()
    print("Table status:", node_resources_table.table_status)
