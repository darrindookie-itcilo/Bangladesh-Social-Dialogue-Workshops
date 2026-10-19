# Verification

The dashboard passed 16 automated integration check groups using a simulated DOM and the platform Web Crypto implementation:

- Both workshop cards and all local page links.
- All 24 session cards, breaks, topics and handout mappings in the Rev.1 programme data.
- Session completion records and 14-event Dhaka-time calendar export for Workshop 1.
- Activity filters, individual downloads, handout previews and the notice about missing separate Secretariat activity sheets.
- Separate workshop notebooks, text escaping, local saving and readable export.
- Reference library and game links.
- Rejection of incorrect facilitator credentials.
- Successful unlock with the requested facilitator credentials.
- Script previews and download of a decrypted PowerPoint file.
- Fourteen sets of facilitator materials for Workshop 1 and ten for Workshop 2.
- Timer start, pause, add 30 seconds, projector mode and exit.
- Result-code validation, points/time ranking, separate workshop boards and CSV export.
- Sign-out clearing of unlocked content and trainer previews.
- Successful decryption of all 48 original protected files, with no plaintext trainer files or password published in the source.
- Byte-identical original game scenarios, classifications, feedback and scoring functions.
- No script or DOM errors during these checks.

A second interaction check completed all twelve game cards in practice mode, selecting, locking in and revealing each answer. It produced 240/240, a six-character result code and twelve saved answers, with no remote submissions or runtime errors.

Source checks verified that the original agendas from the ZIPs are absent, both downloadable agendas are the supplied Rev.1 documents, and all 20 participant handouts are unchanged from the supplied ZIPs. The 48 trainer files are packaged as shared encrypted parts for reliable transfer. Reconstructed downloads are checked against the SHA-256 hashes of the original files.

## Verification limits

The managed browser preview could not start because its sandbox could not mount `/proc` in this environment. Browser visual verification, responsive screenshots and real-browser downloading were therefore unavailable. The responsive layout is implemented with explicit desktop, tablet and mobile breakpoints, but has not been visually verified here.

No real live-race sessions or team submissions were created during testing. The existing Kenya live service retains its separate authentication and was not changed. Practice and the local result-code board were tested.

The GitHub Pages deployment workflow is included. Publication is complete only after the new repository exists, GitHub Pages is enabled with GitHub Actions, and a deployment reports success. A local package or workflow file alone does not verify publication.
