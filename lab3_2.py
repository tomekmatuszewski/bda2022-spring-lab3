import time
import boto3
import psutil
from datetime import datetime
from random import randrange

start_time = time.time()

while True:
    # prepare data
    data = {
        'NodeId': 'node_with_id_' + str(randrange(10)),
        'Timestamp': datetime.now().isoformat(),
        'IdleCpu': str(psutil.cpu_times_percent(interval=1.0, percpu=False).idle),
        'FreeMem': str(100 - psutil.virtual_memory().percent),
        'FreeStorage': str(100 - psutil.disk_usage('/').percent)
    }
    # if you don't want to convert values to str, you can do the following instead
    # data = json.loads(json.dumps(data), parse_float=decimal.Decimal)
    # print('Current node resources: ', data)
    # PutItem
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('NodesResources')
    response = table.put_item(Item=data)
    print('Response from DynamoDB: ', response)
    # lock time
    time.sleep(10.0 - ((time.time() - start_time) % 10.0))
