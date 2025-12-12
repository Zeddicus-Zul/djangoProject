#!/bin/bash
set -e

PROJECT_ID="portfoliosite-468605"
REGION="us-west1"
STATIC_BUCKET="portfoliosite_static_bucket"
MEDIA_BUCKET="portfoliosite_media_bucket"

echo "Creating GCS buckets for Django static and media files..."

# Create static files bucket
echo "Creating bucket: $STATIC_BUCKET"
gcloud storage buckets create gs://$STATIC_BUCKET \
    --project=$PROJECT_ID \
    --location=$REGION \
    --uniform-bucket-level-access || echo "Static bucket may already exist"

# Create media files bucket
echo "Creating bucket: $MEDIA_BUCKET"
gcloud storage buckets create gs://$MEDIA_BUCKET \
    --project=$PROJECT_ID \
    --location=$REGION \
    --uniform-bucket-level-access || echo "Media bucket may already exist"

# Make buckets publicly readable
echo "Setting public read access on buckets..."
gcloud storage buckets add-iam-policy-binding gs://$STATIC_BUCKET \
    --member=allUsers \
    --role=roles/storage.objectViewer

gcloud storage buckets add-iam-policy-binding gs://$MEDIA_BUCKET \
    --member=allUsers \
    --role=roles/storage.objectViewer

echo "Buckets created and configured successfully!"
echo ""
echo "Static bucket: gs://$STATIC_BUCKET"
echo "Media bucket: gs://$MEDIA_BUCKET"
echo ""
echo "Next steps:"
echo "1. Upload your media files: ./upload_media_to_gcs.sh"
echo "2. Deploy to Cloud Run: gcloud builds submit --config=cloudmigrate.yaml"
