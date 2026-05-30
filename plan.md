1. Add Previous and Next buttons inside the modal navigation container to allow chronological navigation between events.
2. Update the javascript `openModal` function to handle updating these buttons' states and click events based on the current event index in `sortedEventIds`.
3. Add keyboard shortcuts (ArrowLeft, ArrowRight) in the `keydown` event listener for the document to allow keyboard navigation of the modal when it's open.
4. Verify by running UI tests `test_delegation.py`, `verify_navigation.py`.
5. Pre-commit checks.
6. Submit PR.
