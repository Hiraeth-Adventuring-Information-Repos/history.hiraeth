## 2024-05-15 - [Hoisting Redundant Operations]
**Learning:** Found a nested loop inside `renderTimeline` where `searchTerm.toLowerCase()` was being redundantly executed. `eraData.filter()` was inside an `eras.forEach` block, meaning string conversion was re-computed for every event rendering check.
**Action:** Hoist repetitive string operations out of inner loops for operations that remain constant across elements.
