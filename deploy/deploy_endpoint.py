#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

# ------------------------------------------------------------------------------
#   Copyright (C) 2024 Veradigm LLC. All rights reserved.
#   @Filename: deploy.py
#   @Author: Peng Wei
#   @Date: 2024-07-23
#   @Email: peng.wei@veradigm.com
#   @Description: 
# ------------------------------------------------------------------------------

import argparse
from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
  Environment,
  ManagedOnlineDeployment,
  ManagedOnlineEndpoint,
  OnlineRequestSettings,
)
from azure.identity import DefaultAzureCredential
from datetime import datetime
arg_parser = argparse.ArgumentParser(description="Deploy an Azure ML endpoint and deployment.")

arg_parser.add_argument("--subscription-id", type=str, required=True, help="Azure subscription ID")
arg_parser.add_argument("--resource-group", type=str, required=True, help="Azure resource group name")
arg_parser.add_argument("--workspace-name", type=str, required=True, help="Azure ML workspace name")
arg_parser.add_argument("--endpoint-name", type=str, required=True, help="Azure ML endpoint name")
arg_parser.add_argument("--acr-name", type=str, required=True, help="Azure Container Registry name")
arg_parser.add_argument("--image-name", type=str, required=True, help="Docker image name")
arg_parser.add_argument("--image-tag", type=str, required=True, help="Docker image tag")
arg_parser.add_argument("--instance-type", type=str, required=True, help="Azure ML instance type")

args = arg_parser.parse_args()


def deploy(args):
    # The credential is required
    credential = DefaultAzureCredential()
    # The MLClient configures Azure ML 
    ml_client = MLClient(
        credential=credential,
        subscription_id=args.subscription_id,
        resource_group_name=args.resource_group,
        workspace_name=args.workspace_name,
    )
    
    endpoint = ManagedOnlineEndpoint(
        name = args.endpoint_name,
        auth_mode="key",  # We use a key for authentication
    ) 
    # Create the endpoint
    ml_client.online_endpoints.begin_create_or_update(endpoint).result()
     
    environment = Environment(
        name=f"{args.image_name}-env",
        image=f"{args.acr_name}.azurecr.io/{args.image_name}:{args.image_tag}",
        inference_config={
            "scoring_route": {
                "port": 8000,
                "path": "/transcribe",
            },
            "liveness_route": {
                "port": 8000,
                "path": "/health",
            },
            "readiness_route": {
                "port": 8000,
                "path": "/ready",
            },
        },
    )
    
    # Configure the deployment
    deployment = ManagedOnlineDeployment(
        name=f"ambient-audio-dp-{datetime.now():%y%m%d%H%M%S}",  # Add the current time to make it unique
        endpoint_name=endpoint.name,
        model=None,
        environment=environment,
        instance_type=args.instance_type,
        instance_count=1,  # we only use 1 instance
        request_settings=OnlineRequestSettings(request_timeout_ms=180000),
    )
    
    # create the online deployment.
    ml_client.online_deployments.begin_create_or_update(deployment).result()

if __name__ == "__main__":
    deploy(args)
