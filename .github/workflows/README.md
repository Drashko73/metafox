# MetaFOX CI/CD Pipeline

This document describes the CI/CD pipeline for the MetaFOX project.

## Overview

The pipeline automatically:

1. Builds Docker images for the MetaFOX API and Worker components
2. Publishes the images to Docker Hub
3. Deploys the updated images to a Kubernetes cluster

## Triggering the Pipeline

The pipeline can be triggered in three ways:

1. **Tag-based deployment**: Push a tag with format `v*.*.*` (e.g., `v1.0.0`)
2. **Manual trigger**: Use the GitHub Actions UI to manually run the workflow and specify a tag
3. **Main branch updates**: Pushing to the main branch will deploy with the 'latest' tag

## Required Secrets

The following secrets must be configured in your GitHub repository:

- `DOCKER_HUB_USERNAME`: Your Docker Hub username
- `DOCKER_HUB_TOKEN`: A Docker Hub personal access token
- `SERVER_IP`: The IP address of the server where the Kubernetes cluster is running
- `SERVER_USER`: The SSH username for the server
- `SSH_PASSWORD`: The SSH password for the server

## Docker Images

Images are published with two tags:
- The specific version tag you specified
- The `latest` tag

For example, if you push the tag `v1.2.3`, the following images will be published:
- `yourusername/metafox-api:1.2.3` and `yourusername/metafox-api:latest`
- `yourusername/metafox-worker:1.2.3` and `yourusername/metafox-worker:latest`

## Kubernetes Deployment

The pipeline assumes that you already have deployments named `api-deployment` and `worker-deployment` running in your Kubernetes cluster. The pipeline will update these deployments with the newly built images.
