# Windmill Sync Example

Example repo that demonstrate how to use a github repo as source of truth for part or all of your Windmill workspace.

Users of this repo can commit changes to the main branches and have it deployed to their Windmill workspace thanks to a github action that will simply uses the [windmill cli's](https://github.com/windmill-labs/windmill/tree/main/cli) `wmill sync push` under the hood.

This repo is used for syncing with the example folder on the demo workspace

## Setup

Write access to the workspace is required. This is done using an access token.
To generate a new token log into your windmill instance
(https://app.windmill.dev/ for cloud hosted instances) and navigate to the
account settings, which contains a "Tokens" section, use the relevant button
there to generate a new token. Note that you will only be able to copy this
token once!

![](./img/account-settings.png) ![](./img/tokens.png)

Add an environment "windmill" to the repository via the settings. You may name
this anything, but will need to adjust the workflow accordingly. Then add a
secret "WMILL_TOKEN" to this environment.

![](./img/gh-environment.png#gh-dark-mode-only)
![](./img/gh-environment-light.png#gh-light-mode-only)

Edit the workflows:
- [.github/workflows/push-on-merge.yaml](./.github/workflows/push-on-merge.yaml) to push on merge to main, usually you'll
only need to fill out the `env` variables, then activate GitHub actions by
navigating to the "Actions" tab in GitHub. You may want to run the action once
manually to see that everything works.

- [.github/workflows/pull-workspace.yaml](./.github/workflows/pull-workspace.yaml) to sync back any changes made in Windmill UI to this repo under the form of either a Pull Request or a commit to main directly.

![](./img/configure.png#gh-dark-mode-only)
![](./img/configure-light.png#gh-light-mode-only)

### Security

We recommend creating and using a separate account in Windmill from which to use the token of. This will allow better tracking of the use of the token.

It may additionally be useful to restrict the GitHub environment.
[The GitHub help article](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
goes into detail of all the options.

## .wmillignore

Use the .wmillignore file to filter the contents to sync (like only the content of some folders), it supports the .gitignore syntax.