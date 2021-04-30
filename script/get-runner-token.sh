#!/bin/bash
set -e

RUNNER_API_ACCESS_TOKEN=$1
API_URL=$2
ORG_NAME=$3

RUNNER_TOKEN=$(curl -s \
        -X POST \
        -H "Accept: application/vnd.github.v3+json" \
        -H "authorization: Bearer ${RUNNER_API_ACCESS_TOKEN}" \
        ${API_URL}/orgs/${ORG_NAME}/actions/runners/registration-token \
    | jq -r .token
)
echo -n $RUNNER_TOKEN