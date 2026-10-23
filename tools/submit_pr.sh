#!/usr/bin/env bash
# usage: submit.sh <folder> <owner/repo> <base> <branch> <title-file> <body-file> [--signoff] [--draft] [--trailer "K: V"]...
# Applies the folder's patch on upstream <base>, pushes to anyingiit fork, opens PR. Prints PR URL.
set -euo pipefail
F=$1 REPO=$2 BASE=$3 BR=$4 TITLE=$(cat "$5") BODY=$6; shift 6
SIGN=0 DRAFT=() TRAILERS=()
while [ $# -gt 0 ]; do case $1 in --signoff) SIGN=1;; --draft) DRAFT=(--draft);; --trailer) TRAILERS+=(--trailer "$2"); shift;; esac; shift; done
G() { env -u GITHUB_TOKEN -u GH_TOKEN gh "$@"; }
# Never publish the harness attribution block, "Requested by", claude.ai links or Claude-Session trailers.
SCRUB=$(cd "$(dirname "$0")" && pwd)/scrub_disclosure.py
python3 "$SCRUB" check "$BODY" "$5" || { echo "refusing: PR text contains private disclosure (run $SCRUB fix)" >&2; exit 1; }
for t in ${TRAILERS[@]+"${TRAILERS[@]}"}; do case $t in *claude.ai*|*Claude-Session*|*Requested\ by*) echo "refusing trailer: $t" >&2; exit 1;; esac; done
NAME=${REPO#*/}
W=${WORKDIR:-/tmp/pr-submit}/$(basename "$F"); rm -rf "$W"; mkdir -p "$(dirname "$W")"
G repo fork "$REPO" --clone=false >/dev/null 2>&1 || true
FORK=$(G api "repos/$REPO/forks?per_page=100" --jq ".[]|select(.owner.login==\"$(G api user --jq .login)\")|.full_name" | head -1); [ -n "$FORK" ] || FORK=$(G api user --jq .login)/$NAME
for i in $(seq 1 30); do G api repos/$FORK >/dev/null 2>&1 && break; sleep 2; done
FORK=$(G api repos/$FORK --jq .full_name)   # fork may be renamed
git clone -q --depth 50 --single-branch --branch "$BASE" https://github.com/$REPO "$W"
cd "$W"
git config user.name anyingiit; git config user.email 49945850+anyingiit@users.noreply.github.com
git am -q --3way "$F"/0001-*.patch
args=(--reset-author); [ $SIGN = 1 ] && args+=(--signoff)
git commit -q --amend --no-edit "${args[@]}" ${TRAILERS[@]+"${TRAILERS[@]}"}
git log -1 --format='--- %an <%ae>%n%B' >&2
git log -1 --format=%B > .git/msg-check
python3 "$SCRUB" check .git/msg-check || { echo "refusing: commit message contains private disclosure" >&2; exit 1; }
if grep -qiE '^Co-Authored-By: *Claude' .git/msg-check; then echo "refusing: commit message names the AI model (Co-Authored-By: Claude...)" >&2; exit 1; fi
git -c credential.helper= -c credential.helper='!env -u GITHUB_TOKEN -u GH_TOKEN gh auth git-credential' \
  push -q -f "https://github.com/$FORK" "HEAD:refs/heads/$BR"
EX=$(G pr list -R "$REPO" --head "$BR" --author @me --json url --jq '.[0].url')
if [ -n "$EX" ]; then echo "$EX"; else G pr create -R "$REPO" --base "$BASE" --head "${FORK%%/*}:$BR" --title "$TITLE" --body-file "$BODY" ${DRAFT[@]+"${DRAFT[@]}"}; fi
cd /; rm -rf "$W"
