#!/bin/bash
set -e

# Configuration
REGISTRY="ghcr.io"
OWNER="bengeek06"
REPO="pm-auth-api"
IMAGE="${REGISTRY}/${OWNER}/${REPO}"
SHA_SHORT=$(git rev-parse --short HEAD)
BRANCH=$(git branch --show-current)

echo "Building Docker image for ${REPO}..."
echo "Branch: ${BRANCH}"
echo "Commit: ${SHA_SHORT}"

# Build production image
echo ""
echo "Building production image..."
docker build \
  --target production \
  --tag "${IMAGE}:sha-${SHA_SHORT}" \
  --tag "${IMAGE}:${BRANCH}" \
  .

# Tag as latest if on main branch
if [ "$BRANCH" = "main" ]; then
  echo ""
  echo "Tagging as latest (main branch)..."
  docker tag "${IMAGE}:sha-${SHA_SHORT}" "${IMAGE}:latest"
fi

# Push all tags
echo ""
echo "Pushing images to ${REGISTRY}..."
docker push "${IMAGE}:sha-${SHA_SHORT}"
docker push "${IMAGE}:${BRANCH}"

if [ "$BRANCH" = "main" ]; then
  docker push "${IMAGE}:latest"
fi

echo ""
echo "✅ Successfully pushed:"
echo "  - ${IMAGE}:sha-${SHA_SHORT}"
echo "  - ${IMAGE}:${BRANCH}"
if [ "$BRANCH" = "main" ]; then
  echo "  - ${IMAGE}:latest"
fi
