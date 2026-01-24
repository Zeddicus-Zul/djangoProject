#!/bin/bash
set -e

# Configuration
PROJECT_ID=${PROJECT_ID:-portfoliosite-468605}
REGION=${REGION:-us-west1}
SERVICE_NAME=${SERVICE_NAME:-gun-sounds}
IMAGE_NAME=${IMAGE_NAME:-gun-sounds}
REPO=${REPO:-gun-sounds}

echo "Using Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"

# Set the project
gcloud config set project ${PROJECT_ID}

# Create Artifact Registry repository if it doesn't exist
echo "Ensuring Artifact Registry repository exists..."
gcloud artifacts repositories create ${REPO} \
  --repository-format=docker \
  --location=${REGION} \
  --description="Docker repository for gun sounds app" \
  2>/dev/null || echo "Repository already exists"

# Build using Cloud Build (no local Docker needed)
echo "Building image using Cloud Build..."
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}:latest

echo "Build complete! Image: ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}:latest"
echo ""
echo "Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}:latest \
  --region ${REGION} \
  --platform managed

echo "Deployment complete!"
