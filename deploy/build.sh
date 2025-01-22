#!/bin/sh


# ------------------------------------------------------------------------------
#   Copyright (C) 2024 Veradigm LLC. All rights reserved.
#   @Filename: build.sh
#   @Author: Peng Wei
#   @Date: 2024-07-23
#   @Email: peng.wei@veradigm.com
#   @Description: 
# ------------------------------------------------------------------------------

docker buildx build --platform linux/amd64 --load --build-arg hf_token=$HF_TOKEN .. -t ambient_audio --progress=plain

az acr login --name dev85ec8a04

docker tag ambient_audio dev85ec8a04.azurecr.io/ambient_audio:0.1

docker push dev85ec8a04.azurecr.io/ambient_audio:0.1
