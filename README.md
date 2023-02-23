# Windmill Sync Example

Template repo that demonstrate how to use a github repo as source of truth for part or all of your Windmill workspace.

Users of this repo can commit changes to the main branches and have it deployed to their Windmill workspace thanks to a github action that will simply uses the [windmill cli](https://github.com/windmill-labs/windmill/tree/main/cli) "wmill sync push" under the hood.

To use a repo solely for backup purpose, see the
[backup example](https://github.com/windmill-labs/windmill-backup-example).

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

Edit the workflow in
[.github/workflows/push.yaml](./.github/workflows/push.yaml), usually you'll
only need to fill out the `env` variables, then activate GitHub actions by
navigating to the "Actions" tab in GitHub. You may want to run the action once
manually to see that everything works, in the future the action will be
automatically ran on a schedule.

![](./img/configure.png#gh-dark-mode-only)
![](./img/configure-light.png#gh-light-mode-only)

### Security

We recommend creating and using a separate account in Windmill from which to use the token of. This will allow better tracking of the use of the token.

It may additionally be useful to restrict the GitHub environment.
[The GitHub help article](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
goes into detail of all the options.

## .wmillignore

To avoid tracking certain files or to whitelist only certail files (like only the content of some folders)