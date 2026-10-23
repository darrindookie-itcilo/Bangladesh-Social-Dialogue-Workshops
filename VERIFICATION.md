# Verification — 23 October 2026 review fixes

## This revision

- Applied the attached answer-display shuffling, readable connection/session-code errors, labelled daily recommendations and eight-round mandate challenge.
- All 40 challenge questions are identical between the participant bank and the competition service. Server grading still receives original bank indices.
- The competition service now accepts `mandate` sessions and grades all eight rounds. Version 13 deployed successfully from source `74876c89d9f1b05bde6010c8999c9363a116df3a`, deployment `appgdep_6adb6f1492c88191a93ba6dd9b1aefe4`.
- Replaced the twelve dialogue scenarios with fictional Bangladesh workshop situations. All original form/setting answers, both acceptable alternatives and scoring rules are preserved.
- Full-text handout search includes session themes and budget/cost/resource terms. Clearing filters also works when the current route is unchanged.
- Corrected agenda revision headings, restored a preparation row with unconfirmed arrangements, and marked missing session leads as to be confirmed. The supplied session timetable and content are unchanged. Both participant packs include the corrected agendas. All six rendered agenda pages were visually inspected.

## Automated checks

- All 11 dashboard DOM/integrity tests passed, including every session mapping, all 40 challenge rounds, game counts, search and clear filters, independent team tokens, offline/code errors, notebook separation and protected materials.
- All 46 protected downloads reconstructed to their recorded SHA-256 hashes. Wrong-password rejection and lock-on-sign-out passed. Their encrypted files were not changed in this revision.
- All 19 participant handouts retain their recorded hashes. Updated agendas and packs match the refreshed integrity manifest; original agenda hashes remain recorded as `sourceSha256`.
- All 33 service tests passed after the production build, including Bangladesh and Kenya authentication, scoring, isolation, reset, stale updates, session expiry, CORS and existing India behavior. The new mandate game passed create, join and eight-round server scoring through the actual route against the test database.
- Service TypeScript check and production build passed. Dashboard JavaScript syntax and whitespace checks passed.

## Live verification

- GitHub Pages successfully published commit `c91274e2bfd63927753b128fb96ca39a422c8554` (Actions run `39971011828`). All 117 published files, totalling 13,664,637 bytes, matched the release byte for byte. All 17 obsolete download paths returned 404. See `verification/live-pages.json`.
- Facilitator sign-in on the published site unlocked teaching materials and connected to the production competition service. The selector lists all seven games.
- The published mandate game completed all eight rounds in the browser with 80/80 points. Its session-code field is present for live play. The game desk displays six workshop challenges/40 decision rounds plus the twelve-scenario dialogue game; no practice-only restriction remains.
- The command-line live-service test stopped at the service's browser protection (HTTP 403/code 1010), as required. This is not counted as a passing live test.
- The facilitator controls use explicit, removable event listeners, and the interface regression check activates the actual submit button after repeated mounts. All 11 tests pass with this change.
- Live team join, reset and CSV download still require a completed production-browser check; automated service tests above use an isolated test database. Browser-control issues encountered during this run are not reported as passing interactions.

## Materials provenance

The October 22 training refresh used the separately supplied Rev.3/Rev.3.1 agendas and the two current training ZIPs. ZIP agendas were excluded. There are 19 participant handouts, 22 protected slide decks, 22 protected trainer scripts and two protected reserve sheets. This revision changes only agenda labels/placeholders and game/interface code; it does not re-upload the previously excluded NSDF translation PDF or publish facilitator credentials.
