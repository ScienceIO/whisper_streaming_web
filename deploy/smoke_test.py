#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

# ------------------------------------------------------------------------------
#   Copyright (C) 2024 Veradigm LLC. All rights reserved.
#   @Filename: smoke_test.py
#   @Author: Peng Wei
#   @Date: 2024-07-23
#   @Email: peng.wei@veradigm.com
#   @Description:
# ------------------------------------------------------------------------------
import io
import pytest
import httpx
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

SUBSCRIPTION_ID = "f21c56c2-6802-4722-a757-2785b91b19a9"
RESOURCE_GROUP = "ml_workspace_east_us_2"
WORKSPACE_NAME = "ml_workspace_east_us_2"
ENDPOINT_NAME = "ambient-audio-endpoint"


@pytest.fixture(scope="module")
def ml_client():
    return MLClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID,
        resource_group_name=RESOURCE_GROUP,
        workspace_name=WORKSPACE_NAME,
    )


@pytest.fixture(scope="module")
def endpoint_details(ml_client):
    endpoint_name = "ambient-audio-endpoint"
    deployment_name = ml_client.online_deployments.list(endpoint_name).next().name
    endpoint = ml_client.online_endpoints.get(name=endpoint_name)
    deployment = ml_client.online_deployments.get(
        name=deployment_name, endpoint_name=endpoint_name
    )
    endpoint_token = ml_client.online_endpoints.get_keys(name=endpoint_name).primary_key

    return {"endpoint": endpoint, "deployment": deployment, "token": endpoint_token}

def test_endpoint(ml_client, endpoint_details):
    headers = {
        "Authorization": f"Bearer {endpoint_details['token']}",
        #"Content-Type": "multipart/form-data",
        "azureml-model-deployment": endpoint_details["deployment"].name,
    }

    with open("data/sample.wav", "rb") as file:
        # Increase the timeout
        timeout = httpx.Timeout(1000.0)
        response = httpx.post(
                endpoint_details['endpoint'].scoring_uri,
                files={"file": ("sample.wav", file, "audio/wav")},
                data={"response_format": "json"},
                headers=headers,
                timeout=timeout,
            )

    try:
        response.raise_for_status()
        assert response.status_code == 200
        print(f"Endpoint response: {response.json()}")
        print("Smoke test passed successfully.")
    except Exception as e:
        print(f"Endpoint response error {response.status_code}: {response.text}")

        # Retrieve the logs for the failed deployment, so we can see what happened
        logs = ml_client.online_deployments.get_logs(
            name=endpoint_details["deployment"].name,
            endpoint_name=endpoint_details["endpoint"].name,
            lines=50,
        )
        print(logs)

        # Delete the failed deployment
        ml_client.online_deployments.begin_delete(
            name=endpoint_details["deployment"].name,
            endpoint_name=endpoint_details["endpoint"].name,
        ).result()

        pytest.fail(f"Deployment failed due to: {e}")
