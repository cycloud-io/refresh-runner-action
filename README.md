Github Action for refreshing dummy self hosted runner.

- Create or refresh dummy runner for target organization.

# Background

When you are using managed self-hosted-runner solution such as myshoes, you need to add dummy runner to the target organization/repository.

However, because dummy runner is in offline states, Github sever will remove the dummy runner after one month. This removal will cause managed self-hosted-runner to work.

`refresh-runner-action` solves the problem by creating or refreshing the target dummy runner by running short-lived runner. By running the action periodically, you can keep the dummy runner refreshed and avoid being removed.


# Usage

## Inputs

- Required
  - `org-name`: Target organization name. (ex. lab)
  - `github-access-token`: Github access token to use.
      - Following scope/permission is required depending on solutions you use:
          - Personal Access Token: `admin:org` scope is required for the target organization.
          - OAuth Apps: `admin:org` scope is required for the target organization.
          - GitHub Apps: `organization_self_hosted_runners: write` permission for the target organization. ([REST API Link](https://docs.github.com/en/enterprise-server@3.0/rest/reference/apps#create-an-installation-access-token-for-an-app))
      - Always use secret environment (ex. `${{ secrets.SECRET_NAME }}`). **NEVER SET THIS VALUE AS PLAIN TEXT.**
- Optional
  - `runner-version`: Runner version to use. (default: `2.272.0`)
  - `runner-name`: Name of the dummy runner to be created/refreshed. (default: `managed-dummy-runner`)

For complete action definition, see [action.yaml](./action.yaml)

## Workflow Example

Following example shows how to use `refresh-runner-action` in your repository's workflow.

- For the first wokrlfow run, you must prepare your own dummy runner. Without this, it can't run the workflow that uses `refresh-runner-action`.
- You need to checkout `refresh-runner-action` before using it.
    - Current GHE Server v3.0 doesn't support Github Marketplace. Until it is supported, we must checkout the action files into the repository that runs workflows.
- You must set following field to appropriate values.
    - org-name
    - github-access-token

```yaml
name: refresh-dummy-runner

on:
  schedule:
    # Running weekly is recommended. 
    # (Runner will be removed if offline state continues for a month)
    - cron: '0 6 * * 1'

  workflow_dispatch:

jobs:
  refresh:
    runs-on: [ self-hosted ]

    steps:
      - name: Check out refresh-runner-action repository
        uses: actions/checkout@v2
        with:
          repository: lab/refresh-runner-action
          ref: v1
          path: ./.github/actions/refresh-runner-action

      - name: Refresh runner
        uses: ./.github/actions/refresh-runner-action
        with:
          # NOTE: Set to appropriate organization name.
          org-name: lab
          # NOTE: Add `RUNNER_API_ACCESS_TOKEN` secret to the repository.
          github-access-token: ${{ secrets.RUNNER_API_ACCESS_TOKEN }}
```


# Future Plan

Following features will be added **if there are certain demands.**

- Support repository scope runner.
- Support GHE Cloud.
