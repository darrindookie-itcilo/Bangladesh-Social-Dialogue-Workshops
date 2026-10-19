# Verification

The dashboard is published at https://darrindookie-itcilo.github.io/Bangladesh-Social-Dialogue-Workshops/.

GitHub Pages successfully deployed the dashboard and its workshop-label correction on 19 October 2026. The tested site revision is `4da82f8cb8cce6c4b162fe8bd5bc2db343a7495d`; the [successful deployment run](https://github.com/darrindookie-itcilo/Bangladesh-Social-Dialogue-Workshops/actions/runs/39256717035) records that revision.

## Live website checks

- All 78 published files returned HTTP 200 and matched their committed Git blob hashes after the correction.
- All 48 protected teaching files downloaded from the live website decrypted and reconstructed to the exact original SHA-256 hashes and sizes.
- Both workshop programmes were checked in Chrome: Workshop 1 has four days and 14 sessions; Workshop 2 has three days and ten sessions. Both final half-days close at 12:30.
- Both Rev.1 agendas, both participant handout ZIPs and the Secretariat toolkit downloaded through Chrome. All 20 individual handouts passed the HTTP and byte-integrity checks.
- The Secretariat toolkit preview and the notice about missing separate Modules 6–11 sheets displayed correctly.
- The original twelve-card game completed in live practice, with feedback on each card, 240/240 points, 12/12 forms correct and a valid six-character result code. The result survived a reload. The test-only score was then reset.
- The corrected Bangladesh workshop names appeared in game setup. No practice results were submitted to the external race service.
- Wrong facilitator credentials were rejected. The requested credentials unlocked the 14 and ten material sets in separate checks. A fresh tab and a refreshed page required sign-in again.
- The official English NORMLEX pages for Conventions Nos. 87, 98 and 144 opened in Chrome.
- The public dashboard rendered with the ITCILO logo and no horizontal overflow at the tested 879-pixel browser width. No game console errors or warnings were reported.

## Automated integration checks

The current files downloaded from the live website also passed all 16 integration check groups using a simulated DOM and platform Web Crypto:

- Both workshop cards and all local page links.
- All 24 session cards, breaks, topics and handout mappings in the Rev.1 programme data.
- Session completion records and the 14-event Dhaka-time calendar export for Workshop 1.
- Activity filters, individual downloads, handout previews and the missing-sheet notice.
- Separate workshop notebooks, text escaping, local saving and readable export.
- Reference library and game links.
- Rejection of incorrect facilitator credentials.
- Successful unlock with the requested facilitator credentials.
- Trainer script previews and download of a decrypted PowerPoint file.
- Fourteen sets of facilitator materials for Workshop 1 and ten for Workshop 2.
- Timer start, pause, add 30 seconds, projector mode and exit.
- Result-code validation, points/time ranking, separate workshop boards and CSV export.
- Sign-out clearing of unlocked content and trainer previews.
- Successful decryption of all 48 original protected files, with no plaintext trainer files or password in the published source.
- Byte-identical original Kenya game scenarios, classifications, feedback and scoring functions.
- No script or DOM errors during these checks.

A separate interaction test completed all twelve game cards in practice mode without network submissions or runtime errors.

Source checks verified that superseded agendas from the ZIPs are absent, the two downloadable agendas are the supplied Rev.1 documents, and all 20 participant handouts are unchanged from the supplied ZIPs. The teaching files use shared encrypted parts; reconstruction is checked against the originals.

## Remaining verification limits

Local Chrome automation stopped activating controls after facilitator sign-in. Live sign-in, the displayed workshop material sets and refresh locking were observed, but trainer preview/download buttons, the timer and sign-out could not be confirmed through live pointer interaction. These functions passed the production-file integration tests and protected-download integrity checks above. A manual browser confirmation is still needed: sign in, open **Read script**, download **Slides**, then use **Sign out & lock** and confirm that the sign-in form returns. This limitation has not been established as a dashboard defect.

Other screen sizes have not been visually verified. The layout includes desktop, tablet and mobile breakpoints.

No real live-race sessions or team submissions were created. The existing Kenya race service retains its separate authentication and was not changed. Practice and the local result-code board were tested; external live-race operation remains unverified.
