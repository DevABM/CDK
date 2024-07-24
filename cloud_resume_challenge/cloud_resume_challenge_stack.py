from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
)
from constructs import Construct

class CloudResumeChallengeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 Bucket for website hosting
        bucket = s3.Bucket(self, "ResumeBucket",
                           website_index_document="index.html",
                           public_read_access=True,
                           block_public_access=s3.BlockPublicAccess.BLOCK_ACLS,
                           removal_policy=RemovalPolicy.DESTROY)

        # DynamoDB Table for visitor count
        table = dynamodb.Table(self, "VisitorTable",
                               partition_key={"name": "ID", "type": dynamodb.AttributeType.STRING},
                               removal_policy=RemovalPolicy.DESTROY)

        # Lambda Function to update visitor count
        update_visitor_count_function = _lambda.Function(self, "UpdateVisitorCountFunction",
                                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                                         handler="lambda_function.lambda_handler",
                                                         code=_lambda.Code.from_asset("lambda"),
                                                         environment={
                                                             "TABLE_NAME": table.table_name,
                                                             "PRIMARY_KEY": "ID",
                                                         })

        # Grant Lambda permissions to read/write to the DynamoDB table
        table.grant_read_write_data(update_visitor_count_function)

        # API Gateway to expose the Lambda function
        api = apigateway.RestApi(self, "ResumeApi",rest_api_name="Resume Service",
                                 description="This service updates the visitor count.")

        get_visitor_count_integration = apigateway.LambdaIntegration(update_visitor_count_function,
                                                                     request_templates={"application/json": '{"statusCode": "200"}'})

        api.root.add_method("GET", get_visitor_count_integration)  # GET /

        # Output the S3 bucket URL
        CfnOutput(self, "BucketURL", value=bucket.bucket_website_url)

