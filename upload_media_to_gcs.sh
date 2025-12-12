#!/bin/bash
set -e

MEDIA_BUCKET="portfoliosite-media-files"
MEDIA_DIR="media"

echo "Uploading media files to GCS bucket: $MEDIA_BUCKET"
echo ""

# Check if gcloud is available
if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI not found. Please install it first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if media directory exists
if [ ! -d "$MEDIA_DIR" ]; then
    echo "Error: $MEDIA_DIR directory not found"
    exit 1
fi

# Upload all files from media directory to GCS, preserving structure
echo "Uploading files from $MEDIA_DIR/..."
gcloud storage cp -r $MEDIA_DIR/* gs://$MEDIA_BUCKET/ 

echo ""
echo "Upload complete!"
echo "Files are now accessible at: https://storage.googleapis.com/$MEDIA_BUCKET/"
echo ""
echo "To view uploaded files:"
echo "gcloud storage ls gs://$MEDIA_BUCKET/ --recursive"
