#!/bin/bash
set -e

RUNNER_API_ACCESS_TOKEN=$1
API_URL=$2
# Expects to be `{owner}/{repo}`
REPO_NAME=$3

# API ref: https://docs.github.com/en/enterprise-server@3.0/rest/reference/actions#create-a-registration-token-for-a-repository
RUNNER_TOKEN=$(curl -s \
        -X POST \
        -H "Accept: application/vnd.github.v3+json" \
        -H "authorization: Bearer ${RUNNER_API_ACCESS_TOKEN}" \
        ${API_URL}/repos/${REPO_NAME}/actions/runners/registration-token \
    | jq -r .token
)
echo -n $RUNNER_TOKEN