## 2026-04-29 - O(N log N) Sorting in Render Loop
**Learning:** Found a major performance bottleneck where the `renderTimeline` function, called on every keystroke in the search bar, was redundantly `O(N log N)` sorting the data arrays and doing DOM queries for each filtering pass.
**Action:** Move sorting and initialization logic into the `initializeTimeline` post-fetch step, storing results in a global `eraDataMap`, and cache container lookups to keep `renderTimeline` strictly limited to `$O(N)` filtering.
