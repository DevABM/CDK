#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cloud_resume_challenge.cloud_resume_challenge_stack import CloudResumeChallengeStack


app = cdk.App()
CloudResumeChallengeStack(app, "CloudResumeChallengeStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)


app.synth()
