# Note taking app with serverless backend

In this project, we will create a note taking app with serverless backend using AWS.

> [!CAUTION]
> This mini project simulates an environment and its architecture might lack some best practices. It is advised against using it for production environments. 

## Prerequisites
- AWS account 
- AWS cli in `us-east-1` with admin privileges 

## Architecture Overview

![Architecture for this project](lambda-dynamodb-p3.jpg)

## Technologies

- AWS
    - Lambda
    - S3
    - API Gateway
    - CloudFormation
    - CloudTrail
    - KMS
    - DynamoDB
- Python (Boto3)

## Project Hierachy

- `/CloudFormation-templates`: CloudFormation templates for the infrastructure
- `/lambda-code`: Source codes for CRUD and EmptyS3Bucket Lambda function
- `/zipped-codes`: Zip format of Lambda functions codes


> DISCLAIMER: This project repository only contains backend configurations. It does not contain frontend application but the backend will fit with any CRUD operations apps.

### 1. Create the infrastructure

I have created a public S3 bucket that contains CloudFormation templates and Lambda codes. 

We will create two stacks for this project: backend and CloudTrail. 

#### Create a stack that will deploy and enable CloudTrail for the account

This stack will create three main things:
- KMS keys 
- CloudTrail
- S3 bucket for CloudTrail logs

Since it's important to harden the security, the API logs will be encrypted both at-rest and on-flight. Apply the stack via cli:

```
aws cloudformation create-stack --stack-name mycloudtrailstack --template-body https://code-for-note-functions-86.s3.amazonaws.com/cloudtrail-kms-s3.yaml
```

If you don't have aws cli configured, you can apply it via <a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https%3A%2F%2Fcode-for-note-functions-86.s3.amazonaws.com%2Fcloudtrail-kms-s3.yaml&stackName=mycloudtrailstack">One-click deployment link</a>. 

#### Create a stack that will deploy backend services

In this project, we will use Lambda functions for CRUD operations, DynamoDB for storing metadata, and S3 bucket for storing media such as content or images.

```
aws cloudformation create-stack   --stack-name myserverlessappstack   --template-body https://code-for-note-functions-86.s3.amazonaws.com/serverless-backend.yaml --capabilities CAPABILITY_IAM
```

<a href="https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https%3A%2F%2Fcode-for-note-functions-86.s3.amazonaws.com%2Fserverless-backend.yaml&stackName=myserverlessappstack&param_CodeBucketName=code-for-note-functions-86&param_ApiCRUDResourceName=notes&param_ApiEmptyS3ResourceName=deleteObjects&param_LambdaRuntime=python3.12&param_ApiStageName=prod">One-click deployment</a> (This may need IAM role with admin privileges)

### 2. Test the APIs

I have enabled CORS for my API Gateway. You can adjust this configuration based on your usage. The CloudFormation template will output two invoke links: CRUD and EmptyBucket. 

Let's test these APIs. You can use different tools such as curl. However, I will use Postman since it is more convenient. 

Here's the sample of how POST API method looks like. 

![POST HTTP method](Postman-POST.jpg)

The expected query parameters that I have written in my Lmabda Codes are as follows:

- **CU function**
    - Name 
    - Content
- **READ function**
    - CreatedAt
    - Name
- **DELETE function**
    - CreatedAt
    - Name

You can adjust the lamda code based on your application use case.

Now, the `CULambdaFunction` stores the metadata(`CreatedAt` and `Name`)in the DynamoDB table and media(`Content`) in the S3 bucket. It's important to note that CloudFormation won't be able to delete a non-empty S3 bucket. 

I have written a python code that will be used by a Lambda function, and this will delete all the objects inside the S3 bucket that we created with CloudFormation. You can invoke this Lambda function via API Gateway as well:

![POST HTTP method for emptying bucket](Postman-POST-empty-bucket.jpg)


### 3. Clean up the resources

If you do not need the infrastructure anymore, you can clean up everything that we created earlier.

#### CloudTrail stack

This will delete everything *except* the S3 bucket. This will differ based on the environment and I think it's better to retain the bucket containing tracing information for any further use.

```
aws cloudformation delete-stack --stack-name mycloudtrailstack
```

#### Backend stack

```
aws cloudformation delete-stack --stack-name myserverlessappstack
```

