Fixes #1327

When Danger runs on Bitrise against a self-hosted Bitbucket Server whose clone URL looks like `https://host/bitbucket/scm/PROJ/repo.git`, `Danger::Bitrise#repo_slug` is `bitbucket/scm/PROJ/repo`. `RequestSources::BitbucketServer#initialize` did `ci_source.repo_slug.split("/")` and took the first two parts, so it called the REST API for project `bitbucket` / repo `scm`. That request fails, and the run ends in `NoMethodError: undefined method '[]' for nil:NilClass`.

Bitbucket Server repositories are always `PROJECT/REPO` (or `~user/repo`), so the request source now uses the **last** two segments of the slug: `split("/").last(2)`. Plain `PROJ/repo` slugs behave the same as before.

I fixed this in the Bitbucket Server request source on purpose, not in `Bitrise#repo_slug_from`. Bitrise is also used with GitHub/GitLab, and its specs expect multi-segment slugs such as GitLab subgroups (`artsy/mobile/ios/artsy.github.io`) to be kept. The same change also covers Appcircle, which derives the slug from the URL path in the same way.

Changes:
- `lib/danger/request_sources/bitbucket_server.rb`: use the last two slug segments (with a short comment explaining why)
- `spec/lib/danger/request_sources/bitbucket_server_spec.rb`: regression spec that builds a `Danger::Bitrise` source from `https://stash.example.com/bitbucket/scm/PROJ/repo.git` and checks that `fetch_details` requests `/rest/api/1.0/projects/PROJ/repos/repo/pull-requests/2080`
- `CHANGELOG.md`: entry under `master`

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Testing:
- Without the lib change, the new spec fails: WebMock reports an unregistered request to `.../projects/bitbucket/repos/scm/pull-requests/2080`. With the change, it passes.
- `bundle exec rspec spec/lib/danger/request_sources spec/lib/danger/ci_sources`: 690 examples, 0 failures (Ruby 3.3.6, `LANG=C.UTF-8`)
- `bundle exec rubocop lib spec`: no offenses

## Checklist

- [x] Tests added and passing locally (see above)
- [x] `CHANGELOG.md` updated under `## master`
