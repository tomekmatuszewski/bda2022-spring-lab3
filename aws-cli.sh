#!/bin/sh
aws dynamodb create-table \
    --table-name NodesResources \
    --attribute-definitions \
      AttributeName=NodeId,AttributeType=S \
      AttributeName=Timestamp,AttributeType=S \
    --key-schema \
      AttributeName=NodeId,KeyType=HASH \
      AttributeName=Timestamp,KeyType=RANGE \
    --billing-mode PROVISIONED \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --table-class STANDARD

### to delete a table use the following
#aws dynamodb delete-table \
#    --table-name NodesResources

### you can even put an item using cli, but you need to explicitly define the types
#aws dynamodb put-item \
#    --table-name NodesResources \
#    --item \
#      '{
#        "NodeId": {"S": "abc123"},
#        "Timestamp": {"S": "2022-04-05T10:05:00"},
#        "IdleCpu": {"N": "89.2"},
#        "FreeMem": {"N": "54.3"},
#        "FreeStorage": {"N": "17.6"}
#      }'

### or query the table (and return consumed capacity)
#aws dynamodb query \
#  --table-name NodesResources \
#  --key-condition-expression "NodeId = :node" \
#  --expression-attribute-values "{ \":node\" : { \"S\" : \"node_with_id_0\" } }" \
#  --return-consumed-capacity TOTAL