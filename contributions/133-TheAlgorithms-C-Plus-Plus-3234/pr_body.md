#### Description of Change

Fixes #3234.

A few files document themselves with Javadoc "banner" comments (`/*****...`), e.g.
`search/binary_search.cpp`, `search/interpolation_search.cpp`, `sorting/selection_sort_iterative.cpp`,
`dynamic_programming/partition_problem.cpp`, `geometry/graham_scan_algorithm.cpp` and
`geometry/graham_scan_functions.hpp`. `doc/Doxyfile` had `JAVADOC_BANNER = NO`, so Doxygen treated those
blocks as plain comments: the `@file` block was ignored and the files appeared in bold (no page) in the
generated file list.

This PR only flips `JAVADOC_BANNER` to `YES` in `doc/Doxyfile` (the line referenced in the issue), so the
existing banner comments are parsed as documentation. No source files are changed.

How I checked it (Doxygen 1.9.8, from the repo root with `doc/Doxyfile`, LaTeX/dot turned off to save time):

- before: all six files above are bold in `files.html` (no file page)
- after: all six have a file page with their `@brief`, `@details`, `@author`, namespaces and function docs

Side effects worth knowing about:

- Doxygen now reads these blocks, so it also reports a few pre-existing doc mistakes in them (e.g.
  `@returns void` on test functions, `@returns @param int ...` in `binary_search.cpp`). `WARN_AS_ERROR` is
  `NO`, so the docs build is not affected; I kept this PR to the config change, but I can clean those up
  here or in a follow-up if you prefer.
- A banner comment inside the body of `binarySearch()` is now appended to that function's detailed
  description (Doxygen's normal behaviour for doc blocks inside function bodies). The text is an
  explanation of the algorithm, so it reads fine.
- `data_structures/cll/cll.h` uses banners as section headers ("Useful method for list"); those now
  become the docs of the next member.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as described
above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

#### Checklist

- [x] Added description of change
- [x] Relevant documentation/comments is changed or added (Doxygen config only)
- [x] PR title follows semantic [commit guidelines](https://github.com/TheAlgorithms/C-Plus-Plus/blob/master/CONTRIBUTING.md#Commit-Guidelines)
- [x] Search previous suggestions before making a new one, as yours may be a duplicate. (no other PR for #3234; #3229 touches only `CONTRIBUTING.md` for a different Doxygen problem)
- [x] I acknowledge that all my contributions will be made under the project's license.
- [x] Tested locally: `doxygen` with `doc/Doxyfile` before/after, the six banner-documented files go from "no page" to rendered; `CHANGELOG.md` n/a (repo has none)

Notes: Enable `JAVADOC_BANNER` so files documented with `/*****` banner comments get rendered by Doxygen.

Closes #3234
