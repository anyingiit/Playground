#!/bin/bash
# fake curl: 404 for handles starting with "no-such", PNG bytes otherwise
fail=0; out=; url=
while [ $# -gt 0 ]; do case $1 in -o) out=$2; shift;; -*f*) fail=1;; http*) url=$1;; esac; shift; done
if [[ $url == */no-such* ]]; then
  [ $fail = 1 ] && { echo "curl: (22) The requested URL returned error: 404" >&2; exit 22; }
  echo "<html>Not Found</html>" > "$out"; exit 0
fi
printf '\x89PNG\r\n\x1a\n' > "$out"
