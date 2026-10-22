# Verification — 22 October 2026 refresh

## Verified before the Pages revision

- Both programme datasets follow the separately attached Rev.3 and Rev.3.1 agendas: 12 institutions sessions and 10 secretariat sessions. Tuesday morning 27 October is an external meeting, with course Session 5 at 13:30.
- Both published agenda files match the attached originals byte for byte.
- All 19 participant Word handouts match the new ZIP sources. Both participant packs contain only those handouts and the correct separately attached agenda. No trainer documents, reserve sheets or reference PDFs are included in those packs.
- All 46 protected files reconstruct to their original source bytes: 22 slide decks, 22 trainer scripts and two reserve sheets. A wrong password is rejected. The HTML script previews remain encrypted.
- Seven simulated-DOM interface tests passed: both programmes, all session activity mappings, previews, wrong/correct facilitator access, all 46 download buttons, sign-out, live-board request handling, independent team-token allocation, all 32 new game rounds and result exports, and notebook separation.
- The competition service passed 32 automated tests, its TypeScript check and a production build. These include team isolation, server scoring, immutable answers, per-team/all-team reset, stale-update rejection, CORS, workshop/game matching, rate limiting, session expiry, logout and preservation of the existing Kenya game rules.
- The competition service deployment succeeded at version 12, source `7ad6f25c1717c501dae86975d819930fac3fdbda`, deployment `appgdep_6ada5a16eb28819187ca06a7bb2ffae0`.

## Review handling

Automatic review rejected re-uploading `dist/downloads/NSDF_Unofficial_English_Translation.pdf`, stating that it appeared nonpublic and conflicted with the earlier request to use a webpage instead of a PDF. The rejected upload was not retried. This revision removes that old PDF and replaces its reference card with the current mapping worksheet and the official Gazette archive webpage. The C98 link remains the official ILO webpage.

A second review rejected the live-board script because it prefilled the facilitator email in public JavaScript. The public script now leaves the username field empty, and test tools prompt for the identifier rather than embedding it. The private server continues to verify both credentials.

## Live checks

The command-line test client was rejected by the service’s browser protection (HTTP 403, code 1010). No attempt was made to bypass that protection. Live browser and GitHub Pages checks are recorded below when completed; the command-line attempt is not counted as a passing live test.

Publication and native-browser checks are in progress. Do not treat this preflight record as a completion claim.
