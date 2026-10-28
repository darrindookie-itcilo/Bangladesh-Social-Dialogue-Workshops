# Bangladesh Social Dialogue Workshops

[Open the dashboard](https://darrindookie-itcilo.github.io/Bangladesh-Social-Dialogue-Workshops/)

Updated from the materials supplied on **22 October 2026**. GitHub Actions publishes `dist/` to GitHub Pages. The website itself has no build step or runtime dependencies.

## Current programmes and materials

- **A3519987 · Tripartite institutions · 26–29 October:** 12 sessions. Tuesday 27 October morning is reserved for the Bangladesh Labour Rules meeting; course sessions resume at 13:30. Thursday is a half day.
- **A3519988 · Secretariat capacities · 30 October–1 November:** 10 sessions; Sunday is a half day.
- Only the separately attached **Rev.3** and **Rev.3.1** agendas are used. Agenda files inside the materials ZIPs are excluded. The download labels now agree with the internal revision headings. On 23 October, missing session leads and preparation arrangements were explicitly marked to be confirmed; the supplied timetable and session content are retained. Both handout packs contain these corrected agendas.
- The activity desk contains **20 current participant handouts**, editable Word downloads, readable previews and two refreshed participant ZIPs. **One Decision, Three Gates: Participant Activity Pack** is available in Workshop 01, Session 7. The revised workbook supplied on 28 October 2026 replaces the previous version in the Word download, readable preview and workshop participant pack. The previous handout set and Rev.1 packs/agendas are removed from the published tree.
- The updated secretariat toolkit contains **eight templates**, including an annual budget template. It is available throughout that workshop. Separate activity sheets referenced for Modules 6–11 were not included in the supplied ZIP; the dashboard states this.
- Facilitator access contains **22 current slide decks, 22 matching trainer scripts and two reserve sheets**. Reserve sheets are optional facilitator material, not scheduled participant downloads.

## Seven learning games

**Call It What It Is** now uses twelve fictional Bangladesh workshop scenarios; its scoring and two acceptable alternative classifications are preserved. Six original Bangladesh workshop challenges add 40 rounds using single choices, pairs and sequencing:

| Game | Best used for |
| --- | --- |
| Rapport Relay | Listening, reframing and maintaining rapport |
| Inclusion Detective | Gender, informality, wage evidence and policy reach |
| Secretariat Sprint | Meeting planning, fair information, minutes, budgeting and technical support |
| Decision to Delivery | Assigned commitments, indicators, follow-up and reform pathways |
| Action Plan Rescue | Drafting, peer review, 30-day improvements and institutional roadmaps |
| Whose Table Is It? | Mandates, routing a matter to the right body, referral files and overlap |

Handout search covers titles, document text and linked session themes, including budget/cost/resource terminology. Clearing a search restores the handouts even on the same route.

The programme and game desk recommend games for every workshop day, and each recommendation block names the day it belongs to. All scenarios and numerical examples are fictional training material. Practice needs no session code. New challenges award 10 points per fully correct round; two-choice rounds award 5 points for each correct choice. Right/wrong totals count whole rounds, so a partial round counts as wrong. The original game counts correct form classifications separately from its setting and keyword bonus points.

**Answer positions are shuffled for display.** Every option list is reordered deterministically before it is drawn, and each game's two-choice round is given a different target position pair. Stored selections and anything sent to the competition service stay in the question bank's original index space, so server scoring is unchanged. Before this, the correct pair was A and C in all five two-choice rounds and B in 13 of 23 single rounds; a team answering by position alone could reach about two thirds of the available points without reading a question.

**All seven games support live competition and practice.** The competition service now includes the same eight mandate rounds for **Whose Table Is It?**, and the facilitator board offers it in the game selector.

## Participant refinements · 23 October

Answer selections in **Call It What It Is** update the existing controls, keeping the card, scroll position, keyboard focus and draft change in place. Locking an answer and moving to the next card still open the next screen at the top.

**Leave race** disconnects immediately with an inline message. The device remembers the disconnect across reloads of the original join link. Its saved result stays on the facilitator board, and explicitly rejoining with the same alias and code resumes that team. Background responses cannot reactivate a stopped connection.

Session codes stay on one line and the code card stacks its controls in narrower windows. Projector view was visually checked at 1280 × 900.

The elapsed clock starts when a team joins. Brief the room first, then ask all tables to join together; the board and game setup now state this. Use one shared device and browser profile per table.

## Run a live competition

1. Unlock **Facilitator view** using the existing workshop credentials; select the workshop and **Live team board**.
2. Choose a game and label, then create a session. Share its eight-character code or join link.
3. Each team opens the selected game on one shared device, chooses the same workshop and enters a distinct alias and the code.
4. Watch each team’s question/section, answered count, right/wrong totals, points, elapsed time and last activity. The board polls every 2.5 seconds and flags a stale connection.
5. Reset one team or all teams in that session. A confirmation describes what clears. Connected team devices return to question one; stale updates from the prior attempt are rejected.

The facilitator can hide scores, project the board, export CSV results, close a session to new teams or reopen it. Closing entry does not stop teams already joined. The timer and local result-code board remain available as an offline classroom fallback for the original game.

Session codes are eight characters drawn from letters A–Z and digits 2–9; there is no zero and no one, so a code read aloud cannot be mistyped as `I` for `1` or `O` for `0`. If a team's device cannot reach the board, the challenge now says so in plain words and offers practice mode, rather than showing the browser's own `Failed to fetch`.

Live competition uses a dedicated Bangladesh API namespace on the existing workshop service:
`https://platform-grievance-india.darrin-dookie.chatgpt.site/api/bangladesh/race`

Sessions and team progress are stored in D1 with separate Bangladesh tables. The server verifies submitted choices, computes scores, locks submitted answers and scopes all controls to their session. It does not trust a participant-supplied score. Teams use independent random bearer tokens; only their hashes are stored. Facilitator login is checked on the server, rate limited and valid for 90 minutes. Facilitator tokens stay in tab memory and are revoked on sign-out. Existing Kenya and India features retain their access protections and data.

## Access and references

Teaching documents and previews use AES-256-GCM encryption with a key derived using PBKDF2-SHA-256 (600,000 iterations) from both username and password. Shared encrypted parts reconstruct the exact original Office files. Neither the login identifier nor password is hardcoded in the public interface. Plaintext teaching files are not published. Refreshing the page, signing out or reaching 90 minutes locks the view again.

Participant notebooks are separate per workshop and saved only in the participant’s browser. Export before changing devices or clearing browser data.

ILO Conventions, including C98, link to official ILO webpages. An automatic review rejected re-uploading the old NSDF translation PDF; it is excluded from this revision. Its reference card now offers the current mapping worksheet and the official Bangladesh Government Press Gazette archive. The archive is a search portal, not a verified notification.

## Checks and maintenance

`npm ci` installs the development-only DOM test dependency. `npm test` prompts securely for the facilitator username and password; it never writes it to a file. `tools/verify_materials.py` verifies source bytes, participant-pack contents, all 46 protected files and wrong-password rejection. `tools/refresh_materials.py` refreshes the training set from the original attachments; it deliberately excludes ZIP agendas and keeps reserve sheets locked.

See [VERIFICATION.md](VERIFICATION.md) and `verification/` for the current test and deployment evidence. A simulated DOM test is identified as such; it is not a substitute for the live browser checks.
