# Note taking app - Serverless Project

This is a note taking app written in React.js and deployed on serverless backend. 

## Technologies

- AWS
- HTML & CSS
- JavaScript & React
- Python Boto3

```
aws cloudformation create-stack   --stack-name myserverlessappstack   --template-body https://code-for-note-functions-86.s3.amazonaws.com/db-bucket-lambda.yaml --capabilities CAPABILITY_IAM
```

```
https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https%3A%2F%2Fcode-for-note-functions-86.s3.amazonaws.com%2Fdb-bucket-lambda.yaml&stackName=myserverlessapp&param_CodeBucketName=code-for-note-functions-86&param_ApiCRUDResourceName=notes&param_ApiEmptyS3ResourceName=deleteObjects&param_LambdaRuntime=python3.12&param_ApiStageName=prod
```