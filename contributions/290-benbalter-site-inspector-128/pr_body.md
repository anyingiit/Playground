Fixes #128.

The README's options block and "What's checked" section had fallen behind the checks in `lib/site-inspector/endpoint/`.

### Changes

- **Options:** replaced the block with the real `site-inspector inspect --help` output, generated with `pa11y` and `wappalyzer` resolvable on the `PATH` (stub scripts that print a version are enough) so that all ten `--<check>` flags appear. A sentence below it notes that `--accessibility` and `--wappalyzer` only show up when those CLIs are installed.
- **What's checked:** each check now lists the keys its `to_h` returns.
  - Accessibility: `valid` and `results`. The four standards are methods you can call on the check, which the section now says.
  - Content: added `generator`, `proper_404s`, `humans_txt`, `vulnerability_disclosure_policy`, `security_txt` and `data_json`.
  - Cookies: new section with `cookie?` and `secure?`, which used to be listed under Headers.
  - Headers: the keys are the header names (`strict-transport-security`, `x-frame-options` and so on) plus any other `x-` headers, so the list now uses those instead of method-style names like `click_jacking_protection`.
  - HSTS: added `preload_list_status`.
  - Well-known and Whois: new sections.

I checked the key names against the code, for example `WellKnown.keys` and `Content.paths` in a console. The specs and RuboCop are unaffected, since only `README.md` changes.

### Motivation and disclosure

This is a `good first issue` with a clear checklist. I prepared it with help from an AI coding assistant (Claude Code) and checked each documented key against the code myself.
