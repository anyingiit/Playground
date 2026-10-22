Fixes #4.

`script/download` had two bugs:

- The cleanup step quoted its glob (`rm -Rf "./avatars/*.png"`), so `rm` looked for a file literally named `*.png` and avatars from a previous `handles.txt` stayed in the montage. It's now `rm -f ./avatars/*.png`, which leaves `avatars/.gitkeep` alone.
- `curl` didn't fail on HTTP errors, so a mistyped or deleted handle saved GitHub's 404 page as `<handle>.png` and `montage` then failed on it. `curl` now runs with `-f`. If a download fails, the script removes anything it left behind and, at the end, prints the handles that failed to stderr.

The script still exits 0 when some downloads fail, so the "Run Avatar Montage" workflow goes on to build the montage from the avatars that did download. If every handle fails, the workflow still stops at the `montage` step, since there are no images. The handle loop is unchanged, so blank lines and surrounding spaces in `handles.txt` (including the spaces after commas in the workflow input) are still ignored.

### Testing

The sandbox I worked in can't reach `github.com/<handle>.png`, so I ran the old and new scripts with a stub `curl` on the `PATH`. The stub returns PNG bytes for valid handles. For a handle starting with `no-such`, it exits 22 when given `-f` and writes an HTML page otherwise. In a directory with a stale `avatars/olduser.png` and a `handles.txt` containing `octocat`, a blank line, `  github  ` and `no-such-user`:

- Before, `avatars/` still had `olduser.png` and an HTML `no-such-user.png`.
- After, it has only `.gitkeep`, `github.png` and `octocat.png`, and the output ends with `Couldn't download avatars for: no-such-user`.

I also confirmed that the real `curl -fL -o` writes no file for a 404 from a local server.

### Motivation and disclosure

This is a `good first issue` with clear acceptance criteria. I prepared it with help from an AI coding assistant (Claude Code), reviewed the change myself, and ran the checks above.
