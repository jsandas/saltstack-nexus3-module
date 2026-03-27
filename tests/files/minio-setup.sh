#!/bin/sh

ACCESS_KEY="AKIAIOSFODNN7EXAMPLE"
SECRET_KEY="wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY"
MINIO_HOST="http://minio:9000"
BUCKET_NAME="nexus3"

# Wait for MinIO to be ready
until curl -s $MINIO_HOST/minio/health/live >/dev/null; do
  echo "Waiting for MinIO to be ready..."
  sleep 1
done

# Create bucket if it doesn't exist
mc alias set local $MINIO_HOST $ACCESS_KEY $SECRET_KEY
mc mb --ignore-existing local/$BUCKET_NAME
