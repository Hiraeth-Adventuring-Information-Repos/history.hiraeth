## 2024-05-15 - [Hoisting Redundant Operations]
**Learning:** Found a nested loop inside `renderTimeline` where `searchTerm.toLowerCase()` was being redundantly executed. `eraData.filter()` was inside an `eras.forEach` block, meaning string conversion was re-computed for every event rendering check.
**Action:** Hoist repetitive string operations out of inner loops for operations that remain constant across elements.
## 2024-05-15 - [Caching DOM Queries and Pre-Sorting Data]
**Learning:** Found that `document.querySelector` and `Array.prototype.sort()` were being redundantly executed on every call to `renderTimeline()`, which fires frequently during search input. This causes O(N log N) sorting and unnecessary DOM traversals on the main thread for every keystroke.
**Action:** Cache DOM elements into a global object (`cachedContainers`) and pre-sort data during the initial fetch phase, storing it in `eraDataMap`. Reference these pre-computed structures in the render loop to prevent recalculation.
## 2026-05-04 - Pre-computing searchable text
**Learning:** During high-frequency renders (like search filtering), repeatedly executing string operations such as `.toLowerCase()` on multiple properties (title, description, summary) across many objects introduces a significant and measurable performance bottleneck. The DOM render itself was not the main culprit, but rather the repeated string manipulation during array filtering.
**Action:** Pre-compute a single `_searchableText` string (e.g., combining and lowercasing the relevant fields) on initialization for static or rarely-changing data. Query against this pre-computed string during loops to bypass redundant string processing overhead.
## 2026-05-06 - Event Delegation Over Individual Listeners
**Learning:** Found a major bottleneck in `renderTimeline()`. The function was running `document.querySelectorAll` and manually attaching `click` and `keydown` event listeners to every `.event-trigger` and `.sub-event-trigger` element on every single keystroke during search. This redundant O(N) querying and listener attachment degraded rendering performance.
**Action:** Use document-level Event Delegation. Attach a single listener to the `document` during application initialization and use `e.target.closest()` to dynamically handle clicks on interactive elements, avoiding the need to re-query the DOM or attach new listeners on subsequent renders.
## 2024-05-15 - [Pre-computing HTML rendering]
**Learning:** Found that `createEventCard` and `createStarEvent` functions were being repeatedly called on every render cycle during search filtering, causing redundant string interpolations and string concatenations to regenerate HTML for each event even though the data does not change.
**Action:** Pre-compute the HTML structure for each event once during the initial data loading phase and cache it on the event object (e.g. `event._cachedHtml`). Then, use this pre-computed HTML directly during the `renderTimeline` function via `.map().join('')`, significantly reducing the work done inside high-frequency render loops.

## 2024-05-18 - Early Returns and Bypassing Loops
**Learning:** Found a performance bottleneck in `renderTimeline` where the `.filter()` loop executed for every event even when the search and tags arrays were empty (e.g., initial render, clearing search). Additionally, the loop redundantly evaluated all filtering conditions using logical operators (`&&`, `||`) for every event instead of short-circuiting.
**Action:** Skip `array.filter()` entirely if the input conditions are empty, and return the original array directly. Inside filtering loops, use early returns (`if (condition fails) return false;`) to exit the execution path immediately and save CPU cycles.

## 2024-05-19 - Skipping Redundant DOM Updates
**Learning:** Found that `renderTimeline()` was updating the DOM (using `innerHTML` or `insertAdjacentHTML`) on every single render cycle, even when the resulting HTML string was identical to the previous render. DOM updates and the resulting browser layout/paint calculations are a significant performance hit.
**Action:** Implemented caching of the generated HTML string directly on the container element (`container._lastHtml`). By checking `if (container._lastHtml !== newHtml)` before applying updates, redundant DOM manipulation is completely skipped when the visual state doesn't change, dramatically improving rendering performance during operations like identical filter outcomes.
## 2024-05-19 - Bypassing Array Operations Completely on Empty Filters
**Learning:** Found that `renderTimeline` was performing an O(N) operation `filteredData.map(event => event._cachedHtml).join('')` for every era, even when `filteredData` represented the entire unmodified dataset (i.e. when search and tags are empty). While string generation is fast, repeatedly joining thousands of pre-computed strings still takes ~1-2ms per render cycle.
**Action:** When no filters are active, completely bypass the `.map().join('')` operation by referencing a pre-computed and cached combined HTML string (`eraData._cachedFullHtml`) generated once during the initialization phase.
