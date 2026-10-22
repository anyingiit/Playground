## Description

As described in #1626, `configure_from_parent` copies the parent's db provider settings to a slice for everything except gateways, and slice gateway URLs come only from `ENV`. So an app that sets its `database_url` explicitly in the db provider:

```ruby
Hanami.app.configure_provider :db do
  config.gateway :default do |gw|
    gw.database_url = "sqlite://db/app.sqlite"
  end
end
```

can't start the db in any slice that has one:

```
Hanami::ComponentLoadError: A database_url for gateway default is required to start :db.
```

With this change, when no URL for a slice's gateway is found in `ENV`, the slice falls back to the URL of the parent's gateway with the same name. This only applies when `config.db.configure_from_parent` is enabled, which is the default.

On the precedence question in the issue, I went with **ENV first, then the parent**. A slice-specific or generic `DATABASE_URL` env var still wins, so existing setups that configure slices via ENV don't change. The parent URL is only used where the slice would otherwise fail to start. Since the URLs then match, the existing `apply_parent_gateway_config` also copies the parent gateway's other config, so the slice shares the parent's connection. The parent's other gateways are still not copied to slices. One consequence: the unprefixed `DATABASE_URL` also counts as ENV for slices, so an app that sets an explicit URL in its provider but keeps the `DATABASE_URL` that `hanami new` writes to `.env` will still have its slices use the `.env` database, as before this change. If you'd rather have the parent's explicit URL win over the generic `DATABASE_URL` (and only slice-prefixed vars like `MAIN__DATABASE_URL` win over the parent), or the parent win outright, I'm happy to change it.

`hanami db` commands already group slice gateways by database URL, so a slice using the parent's URL is treated as the same database as the parent.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues / help-wanted issues. The change was prepared with Claude Code and checked as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #1626

## Checklist

- [x] Specs added in `spec/integration/db/db_slices_spec.rb`:
  - A slice without a URL in ENV uses the parent's explicitly configured URL and shares its gateway. A slice with `MAIN__DATABASE_URL` keeps its own. This fails before the change with the error above.
  - A slice with `configure_from_parent = false` still requires its own URL. This one passes before the change too; it guards against the fallback leaking into opted-out slices.
- [x] `spec/integration/db`: 60 examples, 0 failures. The full suite gives the same results before and after. The 20 failures that happen locally either way are in assets, CSP nonce, request logging and detailed error specs, and they fail the same way on `main` in my environment, which has no JS asset toolchain.
- [x] RuboCop clean on the changed files
- [x] `CHANGELOG.md` entry under Unreleased / Fixed
