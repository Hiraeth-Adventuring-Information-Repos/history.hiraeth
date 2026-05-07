## 2026-05-07 - [Off-Canvas Sidebar Keyboard Navigation]
**Learning:** Adding an off-canvas sidebar menu without a programmatic keyboard escape hatch creates a functional focus trap or requires frustrating reverse-tabbing for keyboard users.
**Action:** Always implement an `Escape` key listener for off-canvas elements. Crucially, when dismissing via Escape, programmatically return focus to the trigger button (`#sidebar-toggle`) to maintain a logical and continuous focus flow in the DOM.
