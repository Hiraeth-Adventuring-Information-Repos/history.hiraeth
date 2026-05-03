## 2024-05-15 - [Hoisting Redundant Operations]
**Learning:** Found a nested loop inside `renderTimeline` where `searchTerm.toLowerCase()` was being redundantly executed. `eraData.filter()` was inside an `eras.forEach` block, meaning string conversion was re-computed for every event rendering check.
**Action:** Hoist repetitive string operations out of inner loops for operations that remain constant across elements.
## 2024-05-15 - [Caching DOM Queries and Pre-Sorting Data]
**Learning:** Found that `document.querySelector` and `Array.prototype.sort()` were being redundantly executed on every call to `renderTimeline()`, which fires frequently during search input. This causes O(N log N) sorting and unnecessary DOM traversals on the main thread for every keystroke.
**Action:** Cache DOM elements into a global object (`cachedContainers`) and pre-sort data during the initial fetch phase, storing it in `eraDataMap`. Reference these pre-computed structures in the render loop to prevent recalculation.
