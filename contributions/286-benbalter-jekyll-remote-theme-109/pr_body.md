Fixes #109.

As you diagnosed in the issue, the Usage examples pointed at `benbalter/retlab@v1.0.0`. `retlab` is archived and has no `v1.0.0` tag, so codeload returns 404 for anyone who copies the example.

This switches the examples to [`pages-themes/cayman`](https://github.com/pages-themes/cayman), one of the supported GitHub Pages themes:

- `remote_theme: pages-themes/cayman` (HEAD)
- `pages-themes/cayman@v0.2.0` (an existing tag) and `pages-themes/cayman@master` (an existing branch) in the Usage block and in "Declaring your theme"
- `pages-themes/cayman@latest`, which resolves to the `v0.2.0` release, marked Latest

Two examples only illustrate syntax, and cayman has neither an Enterprise URL nor a branch with slashes to show. The Enterprise URL and the branch with slashes (`@feature/new-layout`) now use the `OWNER/REPOSITORY` placeholder that the Enterprise section already uses. The surrounding wording is unchanged. I also added a line under Unreleased > Fixes in `HISTORY.md`; happy to drop it if you'd rather add it yourself.

I checked that every ref exists with `git ls-remote --heads --tags https://github.com/pages-themes/cayman`, which lists `master` and the tags up to `v0.2.0`. I also checked the releases page for `@latest`. I couldn't `curl -sI` the codeload URLs from my environment because outbound codeload requests are blocked there, so a quick check on your side would be welcome.

### Motivation and disclosure

This is a small `good first issue` with a clear description of the wanted fix. I prepared it with help from an AI coding assistant (Claude Code), reviewed the change myself, and checked the refs as described above.
