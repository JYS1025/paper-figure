# Repository badges

Stars, forks and watchers come from the authenticated [GitHub repository API](https://docs.github.com/en/rest/repos/repos#get-a-repository). The checked-in SVGs work in private repositories without sending an access token to an image service. Watchers use `subscribers_count`; GitHub's `watchers_count` is an alias for stars.

The [Repository badges workflow](../.github/workflows/repo-badges.yml) refreshes the counters daily, on stars/forks, on updater changes and on manual dispatch. It commits only when generated files change. Failed API requests leave the previous snapshot intact. The [snapshot](images/readme/github-stats.json) records when the displayed values were observed; the badges are not real-time counters.

To refresh from a checkout with GitHub CLI authenticated:

```sh
python3 scripts/update-repo-badges.py
```

The **Views 14d** badge uses [GitHub repository traffic](https://docs.github.com/en/rest/metrics/traffic#get-page-views), the page-view count for the preceding 14 days at the date shown in the badge. It is not a lifetime total or a unique-visitor count. GitHub's distinct-visitor count is recorded separately in the snapshot. No third-party counter service receives repository information.

Traffic access requires an account or token with repository administration read access; the default Actions token does not provide that permission. Without a dedicated token, the workflow updates stars/forks/watchers and preserves the **dated traffic snapshot**. Refresh traffic locally with the authenticated command above.

For automatic traffic refresh, an owner may optionally add a fine-grained token as the repository Actions secret `REPO_STATS_TOKEN`, restricted to this repository, with **Administration: read** and **Contents: read**. The workflow uses it only to read the GitHub API; its normal Actions token commits the SVGs. No personal token is provisioned or copied automatically. Authentication errors preserve the old traffic snapshot; other failures stop the refresh.
