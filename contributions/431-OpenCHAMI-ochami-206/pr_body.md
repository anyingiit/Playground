<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KMcyNnzD6JeAFXoMMWEfs3D)_

Fixes #206

This adds `add` and `delete` entries to the `iface` section of `man/ochami-smd.1.sc`, which until now covered only `get`. The new entries follow the existing `compep` and `rfe` sections.

- **add** describes:
  - the positional form `comp_id mac_addr net_name,ip_addr`;
  - the `-d data`, `-d @path` and `-d @-` forms;
  - the `-D/--description` option, including its default and that it cannot be combined with `-d`;
  - the `-f/--format-input` option.
- **delete** describes:
  - the `--all`, interface ID, and `-d` forms;
  - `--no-confirm`;
  - the rule from #170: only each payload item's ID is used, and a blank, `.`/`..` or `/`-containing ID is a usage error before anything is deleted;
  - that delete does not derive a missing ID from `MACAddress`.

`make man` builds cleanly with scdoc 1.11, and the generated `ochami-smd.1` now lists `add`, `delete` and `get` under `iface`.

### Possible follow-up for `iface add`

While checking the positional form of `iface add` against the code, I noticed two things:

- The `Use` string and `--help` say "one or more pairs of network name and IP address", and one of the examples passes two pairs. `PreRunE`, however, requires exactly 3 arguments (`len(args) != 3`), so `ochami smd iface add x3000c1s7b55n0 de:ca:fc:0f:fe:ee external,10.1.0.55 internal,172.16.0.55` fails with `expected -d or >= 3 arguments ..., got 4`.
- A network argument without a comma, such as `... de:ca:fc:0f:fe:ee external`, panics with `index out of range [1] with length 1` at `cmd/smd/iface/add.go:92`.

The man page above documents what the command does today, which is a single `net_name,ip_addr` pair. I'm happy to open a separate fix if you'd like `add` to accept multiple pairs as its help text says.

The commit is signed off (DCO).

This change was prepared with AI assistance (Claude Code). I reviewed the diff and the generated man page, and I ran the commands above myself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
