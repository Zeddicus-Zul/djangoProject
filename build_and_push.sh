#!/bin/bash
set -e

# Env defaults
PROJECT_ID=${PROJECT_ID:-portfoliosite-468605}
REGION=${REGION:-us-west1}
IMAGE_NAME=${IMAGE_NAME:-gun-sounds}
REPO=${REPO:-gun-sounds}
REGISTRY="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}"

# Build Docker image
echo "Building Docker image: ${REGISTRY}:latest"
docker build -t "${REGISTRY}:latest" .

# Push to Artifact Registry
echo "Pushing image to Artifact Registry..."
docker push "${REGISTRY}:latest"

echo "Build and push complete!"
