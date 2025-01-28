#!/bin/sh


# ------------------------------------------------------------------------------
#   Copyright (C) 2024 Veradigm LLC. All rights reserved.
#   @Filename: build.sh
#   @Author: Peng Wei
#   @Date: 2024-07-23
#   @Email: peng.wei@veradigm.com
#   @Description: 
# ------------------------------------------------------------------------------

docker buildx build --platform linux/amd64 --load .. -t ambient_audio_realtime --progress=plain

az acr login --name dev85ec8a04

docker tag ambient_audio_realtime dev85ec8a04.azurecr.io/ambient_audio_realtime:0.2

docker push dev85ec8a04.azurecr.io/ambient_audio_realtime:0.2
