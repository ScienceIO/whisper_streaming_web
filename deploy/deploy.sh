#!/bin/sh


# ------------------------------------------------------------------------------
#   Copyright (C) 2024 Veradigm LLC. All rights reserved.
#   @Filename: deploy.sh
#   @Author: Peng Wei
#   @Date: 2024-07-23
#   @Email: peng.wei@veradigm.com
#   @Description: 
# ------------------------------------------------------------------------------


# Set variables using environment variables with default values
SUBSCRIPTION_ID="${SUBSCRIPTION_ID:-f21c56c2-6802-4722-a757-2785b91b19a9}"
RESOURCE_GROUP="${RESOURCE_GROUP:-ml_workspace_east_us_2}"
WORKSPACE_NAME="${WORKSPACE_NAME:-ml_workspace_east_us_2}"
ENDPOINT_NAME="${ENDPOINT_NAME:-ambient-audio-realtime-endpoint}"
ACR_NAME="${ACR_NAME:-dev85ec8a04}"
IMAGE_NAME="${IMAGE_NAME:-ambient_audio_realtime}"
IMAGE_TAG="${IMAGE_TAG:-0.1}"
INSTANCE_TYPE="${INSTANCE_TYPE:-Standard_NC4as_T4_v3}"

# Install Python dependencies
pip install azure-ai-ml azure-identity pytest httpx

# Run the Python deployment script with the defined variables
python deploy_endpoint.py \
    --subscription-id "$SUBSCRIPTION_ID" \
    --resource-group "$RESOURCE_GROUP" \
    --workspace-name "$WORKSPACE_NAME" \
    --endpoint-name "$ENDPOINT_NAME" \
    --acr-name "$ACR_NAME" \
    --image-name "$IMAGE_NAME" \
    --image-tag "$IMAGE_TAG" \
    --instance-type "$INSTANCE_TYPE"
