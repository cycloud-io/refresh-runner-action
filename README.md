GitHub Action for refreshing dummy self hosted runner.
The action creates or refreshes dummy runner for target organization or target repository.

# Background

When you are using managed self-hosted-runner solution such as [myshoes](https://github.com/whywaita/myshoes), you'll need to add dummy runner to the target organization/repository.

However, because dummy runner is always in offline status, GitHub sever will remove the dummy runner after a month. This removal will cause managed self-hosted-runner to fail when trying to create new action runner.

`refresh-runner-action` solves the problem by creating or refreshing the target dummy runner by running short-lived runner. By running `refresh-runner-action` periodically, you can keep the dummy runner refreshed and avoid being removed by GitHub server.


# Usage

## Inputs

- Required
  - `org-name` or `repo-name`: Target organization or repository name.
      - Either name must be specified. You can't set both.
      - `org-name` example: cycloud-io
      - `repo-name` example: cycloud-io/my-repo
  - `github-access-token`: GitHub access token to use.
      - You must prepare the GitHub access token. The GitHub Actions' **default token `secrets.GITHUB_TOKEN` won't work.**
      - Check required scope/permission for the token [here](#required-scopepermission).
      - Always use secret environment (ex. `${{ secrets.SECRET_NAME }}`). **NEVER SET THIS VALUE AS PLAIN TEXT.**
- Optional
  - `runner-version`: Dummy runner version to use. If not specified, it will copy and use the version of the running runner.
      - **Not specifying runner-version is highly recommended because it uses the same runner version**. (Dummy runner may fail if versions differ)
  - `runner-name`: Name of the dummy runner to be created/refreshed. (default: `managed-dummy-runner`)

For complete action definition, see [action.yaml](./action.yaml)

## Workflow Example

Following GitHub Actions workflow example shows how to use `refresh-runner-action` in your repository's workflow.

- For the first wokrlfow run, you must prepare your own dummy runner. Without it you can't run the workflow that uses `refresh-runner-action`. See [official document](https://docs.github.com/en/enterprise-server@3.0/actions/hosting-your-own-runners/adding-self-hosted-runners) for detail.
- You must set following fields to appropriate values.
    - `org-name` or `repo-name` (Do not set both)
    - `github-access-token`

```yaml
name: refresh-dummy-runner

on:
  schedule:
    # Running weekly is recommended. 
    # (The dummy runner will be removed if offline status continues for a month)
    - cron: '0 6 * * 1'

  workflow_dispatch:

jobs:
  refresh:
    runs-on: [ self-hosted ]

    steps:
      - name: Refresh runner
        uses: cycloud-io/refresh-runner-action@v1
        with:
          # NOTE: Set either `org-name` or `repo-name`.
          org-name: cycloud-io
          #repo-name: cycloud-io/my-repo

          # NOTE: Add `RUNNER_API_ACCESS_TOKEN` secret to the repository.
          github-access-token: ${{ secrets.RUNNER_API_ACCESS_TOKEN }}
```


## Required scope/permission

Following scope/permission is required for `github-access-token`.

- Personal Access Token
    - For `org-name` - `admin:org` scope is required for target organization.
    - For `repo-name` - `repo` scope is required for target repository.

- OAuth Apps 
    - Same as Personal Access Token.

- GitHub Apps 
    - For `org-name` - `organization_self_hosted_runners: write` permission is required for target organization.
    - For `repo-name` - `administration: write` permission is required for target repository.
  

Related Links:

- [Self-hosted runner groups](https://docs.github.com/en/enterprise-server@3.0/rest/reference/actions#self-hosted-runner-groups)
- [Create an installation access token for an app](https://docs.github.com/en/enterprise-server@3.0/rest/reference/apps#create-an-installation-access-token-for-an-app)

