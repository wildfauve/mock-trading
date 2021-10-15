# Mock Trading

## Running DynamoDB Locally

Use the docker image supplied by AWS.

Checking out the tables:

```
aws dynamodb list-tables --endpoint-url http://localhost:8000
```

Checkout some of the tables using `dy`

e.g.

```
dy scan -t broker -o json -r local
```
