#!/usr/bin/env bash

set -euo pipefail

AWS_REGION="${AWS_REGION:-ap-southeast-1}"
AWS_ACCOUNT_ID="${AWS_ACCOUNT_ID:-740595473620}"
IMAGE_NAME="${IMAGE_NAME:-haithichdi-backend}"
IMAGE_TAG="${IMAGE_TAG:-v8}"
LOCAL_IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"
REMOTE_IMAGE="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG}"

aws ecr get-login-password --region "${AWS_REGION}" \
  | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

docker build --platform linux/amd64 --provenance=false -t "${LOCAL_IMAGE}" -f backend/Dockerfile.lambda backend/
docker tag "${LOCAL_IMAGE}" "${REMOTE_IMAGE}"
docker push "${REMOTE_IMAGE}"

echo "Pushed ${REMOTE_IMAGE}"
