Part of #21432

### Description of changes

Renames the remaining TitleCase constants in `world/Entrance.h` and `management/NewsItem.h` to the `kCamelCase` notation, and updates every use:

- `world/Entrance.h`: `ParkEntranceHeight` → `kParkEntranceHeight`, `RideEntranceHeight` → `kRideEntranceHeight`, `RideExitHeight` → `kRideExitHeight`, `MaxRideEntranceOrExitHeight` → `kMaxRideEntranceOrExitHeight`
- `management/NewsItem.h` (`News` namespace): `ItemTypeCount` → `kItemTypeCount`, `ItemHistoryStart` → `kItemHistoryStart`, `MaxItemsArchive` → `kMaxItemsArchive`, `MaxItems` → `kMaxItems`

Uses updated in `ParkEntrancePlaceAction.cpp`, `RideEntranceExitPlaceAction.cpp`, `InteractiveConsole.cpp`, `NewsItem.cpp`, `S6Importer.cpp`, `ScPark.cpp`, `ScParkMessage.cpp` and `openrct2-ui/windows/News.cpp`.

### Rationale behind changes

#21432 asks to move constants to `kCamelCase`. This is a pure rename with no behaviour change. None of these names are exposed to the plugin API. The values and types are unchanged.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

### Suggested testing steps

- Build (`ninja`) and run the test suite (`ctest`). No behaviour change is expected.
- `grep -rnwE 'ParkEntranceHeight|RideEntranceHeight|RideExitHeight|MaxRideEntranceOrExitHeight|ItemTypeCount|ItemHistoryStart|MaxItemsArchive|MaxItems' src test` returns nothing.

Verified locally: headless Debug build (`-DDISABLE_GUI=ON -DWITH_TESTS=ON`, scripting enabled) compiles and `ctest` passes, except for the 13 tests that need the game data/objects/replays, which are not available in my environment (they fail at Context init / with missing objects, unrelated to this change), and `src/openrct2-ui/windows/News.cpp` (not part of the headless build) passes a `-fsyntax-only` compile with the same flags. `clang-format-diff` reports no changes on the modified lines.

### Did you use AI to help find, test, or implement this issue or feature?

Yes. Claude Code did the rename and ran the build and tests. I reviewed the diff before submitting.
