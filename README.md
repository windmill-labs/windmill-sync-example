# Windmill Sync Example

Example repo that demonstrate how to leverage Github to orchestrate your
development cycles with Windmill.

## How it works

This repo illustrates the following process:

- Users iterates and make their changes in a "staging" Windmill workspace,
  called `github-sync-example-staging` for this tutorial
- Everytime a Windmill App, Flow or Script is deployed to that workspace (via
  Windmill's UI), Windmill automatically commits it to this repo and creates one
  branch per app/flow/script.
- On every commit, PRs are automatically created via a Github action. Approved
  Github users can review and merge those PRs.
- Everytime a PR is merged, another Github action automatically deploys the
  change to a "production" Windmill workspace, called `github-sync-example-prod`
  for this tutorial

## Setup

#### Github repository setup

First the Github repo needs to be setup and Windmill needs to be able to commit
to it.

1. Create a Github repository
1. Generate a
   [Github token with write permission](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
   to this repository. This is necessary for Windmill to push commits to the
   repo everytime a change is made to the staging workspase. (keep the token
   value somewhere, we will need it in the following setup steps)
1. In the repository settings > Actions > General, tick the
   [Allow GitHub Actions to create and approve pull requests](https://docs.github.com/en/enterprise-server@3.10/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#preventing-github-actions-from-creating-or-approving-pull-requests).
   This is necessary for the Github action automatically creating PRs when
   Windmill commits a change
1. From Windmill, create a token under User settings > Token and
   [save it as a secret](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)
   named `WMILL_TOKEN` in the repo settings > "Secret and Variable" > "Actions".
   This is necessary for Windmill to push to the production workspace
   ![](./img/token_creation.png)

#### Windmill setup

1. In Windmill, create a `git_repository` resource pointing to the Github
   repository and containing the token generated previously. You URL should be
   `https://[USERNAME]:[TOKEN]@github.com/[ORG|USER]/[REPO_NAME].git`. Note that
   you have the possibility to input a custom branch name and a subfolder in
   this resource. Given that we are going to request Windmill to create one
   branch per script/flow/app, setting a custom branch will have no effect.
   However, if you wish to persist the windmill workspace in a subfolder of your
   repository, you can set it here. ![](./img/resource_creation.png)
1. In Windmill workspace settings > Git sync tab, pick the `git_repository`
   resource and toggle ON "Create one branch per per deployed script/flow/app"
   ![](./img/git_sync_tab.png)

#### Github actions setup

Two actions are needed.

1. The first one to automatically create a PR when Windmill commits a change
   after a user deployed a script/flow/app in the staging workspace. It is
   [open-pr-on-commit.yaml](./.github/workflows/open-pr-on-commit.yaml). All
   branches created by Windmill will have a `wm_deploy/` prefix, which is handy
   to triger this action only when a branch mathcing this pattern is created.
1. The second one to automatically push the content of the repo to the Windmill
   production workspace when a PR is merged. It is
   [push-on-merge.yaml](./.github/workflows/push-on-merge.yaml). This action
   uses the [Github CLI](https://cli.github.com/) which is available by default
   on Github action workers.
