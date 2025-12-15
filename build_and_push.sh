#!/bin/bash
set -e

PROJECT_ID=${PROJECT_ID:-portfoliosite-468605}
REGION=${REGION:-us-west1}
IMAGE_NAME=${IMAGE_NAME:-gun-sounds}
REPO=${REPO:-gun-sounds}
REGISTRY="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}"

echo "Building Docker image -> ${REGISTRY}:latest"
docker build -t ${REGISTRY}:latest .

echo "Pushing to Artifact Registry..."
docker push ${REGISTRY}:latest

echo "✅ Image built and pushed: ${REGISTRY}:latest"
