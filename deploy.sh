#!/bin/bash
set -e

# Env defaults
PROJECT_ID=${PROJECT_ID:-portfoliosite-468605}
REGION=${REGION:-us-west1}
IMAGE_NAME=${IMAGE_NAME:-gun-sounds}
REPO=${REPO:-gun-sounds}
SERVICE=${SERVICE:-gun-sounds-app}
REGISTRY="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}"

# Build & push
./build_and_push.sh

# Deploy to Cloud Run
exec gcloud run deploy "$SERVICE" \
  --image "${REGISTRY}:latest" \
  --region "$REGION" \
  --platform managed
