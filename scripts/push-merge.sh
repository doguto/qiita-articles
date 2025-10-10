#!/usr/bin/env bash

git push origin develop
gh pr create --base main --title "記事更新"
gh pr merge --squash --delete-branch

