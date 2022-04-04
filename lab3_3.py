import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta


def query_node_resources(n):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('NodesResources')
    response = table.query(
        KeyConditionExpression=Key('NodeId').eq(n)
    )
    return response['Items']


def query_node_resources_by_time(n, begin):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('NodesResources')
    response = table.query(
        KeyConditionExpression=Key('NodeId').eq(n) & Key('Timestamp').gt(begin.isoformat())
    )
    return response['Items']


def query_node_idle_cpu_by_time(n, begin, end):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('NodesResources')
    response = table.query(
        ProjectionExpression="IdleCpu",
        KeyConditionExpression=Key('NodeId').eq(n) & Key('Timestamp').between(begin.isoformat(), end.isoformat())
        # we can use between instead of gt
    )
    return response['Items']


def scan_nodes_with_high_load(t):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('NodesResources')
    # design the tables and queries, so you don't need the scan operation!
    # if you think you can solve the problem using the list of all the nodes (for example in KeyConditionExpression)
    # and a simple query, try it
    response = table.scan(
        ProjectionExpression="NodeId, #ts, IdleCpu",
        ExpressionAttributeNames={
            "#ts": "Timestamp"
        },
        FilterExpression=Attr('IdleCpu').lt(str(100 - t)),
        ReturnConsumedCapacity='TOTAL'
    )
    return response['Items'], response['ConsumedCapacity']


if __name__ == '__main__':
    node_id = 'node_with_id_0'

    # 1
    print(f"Data for the node {node_id}")
    records = query_node_resources(node_id)
    for r in records:
        print(r['NodeId'], "for", r['Timestamp'], "had", r['IdleCpu'] + "% idle cpu,",
              r['FreeMem'] + "% free memory and", r['FreeStorage'] + "% free storage")

    # 2
    how_far = 5
    print(f"Data for the node {node_id} for the last {how_far} min")
    current_time = datetime.now()
    five_min_earlier = current_time - timedelta(minutes=how_far)
    records = query_node_resources_by_time(node_id, five_min_earlier)
    for r in records:
        # print(r)  # this prints the whole record
        print(r['NodeId'], "for", r['Timestamp'], "had", r['IdleCpu'] + "% idle cpu,",
              r['FreeMem'] + "% free memory and", r['FreeStorage'] + "% free storage")

    # 3
    print(f"Idle cpu the node {node_id} for the last {how_far} min")
    current_time = datetime.now()
    five_min_earlier = current_time - timedelta(minutes=how_far)
    records = query_node_idle_cpu_by_time(node_id, five_min_earlier, current_time)
    for r in records:
        # print(r)  # this prints the whole record
        print(r['IdleCpu'] + "% idle cpu")

    # 4
    threshold = 20
    print(f"Nodes with the load higher than {threshold}%")
    # this one can be costly, we use scan instead of query
    records, consumed = scan_nodes_with_high_load(threshold)
    print(f"we consumed {consumed['CapacityUnits']} units for this scan")
    for r in records:
        print(r['NodeId'], "for", r['Timestamp'], "had", r['IdleCpu'] + "% idle cpu")
