#!/usr/bin/env bash
# Regression check for TheAlgorithms/C-Plus-Plus#3234 (not part of the patch).
# Usage: check_banner_docs.sh <repo-dir> <out-dir>
# Runs doxygen with the repo's doc/Doxyfile (LaTeX/dot disabled for speed) and fails
# if any of the files documented with /***** banner comments is listed in bold
# (= no file page) in files.html.
set -u
repo=$1; out=$2
cd "$repo" || exit 2
(cat doc/Doxyfile; echo "OUTPUT_DIRECTORY=$out"; echo "GENERATE_LATEX=NO"; echo "HAVE_DOT=NO"; echo "NUM_PROC_THREADS=2") \
  | doxygen - > "$out.log" 2> "$out.err" || exit 2
rc=0
for f in binary_search.cpp interpolation_search.cpp partition_problem.cpp \
         selection_sort_iterative.cpp graham_scan_algorithm.cpp graham_scan_functions.hpp; do
  if grep -q "<b>$f</b>" "$out/html/files.html"; then echo "FAIL $f: no page (bold)"; rc=1
  else echo "ok   $f: has a file page"; fi
done
exit $rc
