# Bangladesh social dialogue workshops · 2026

[Open the published dashboard](https://darrindookie-itcilo.github.io/Bangladesh-Social-Dialogue-Workshops/) · [Publication workflow](https://github.com/darrindookie-itcilo/Bangladesh-Social-Dialogue-Workshops/actions)

A combined ITCILO dashboard with separate programmes for:

1. **A3519987** — Strengthening Tripartite Social Dialogue Institutions: From Policy Design to Effective Implementation and Institutional Transformation. Dhaka, **26–29 October 2026**, three and a half days.
2. **A3519988** — Strengthening the Capacities of the Secretariats of Tripartite Social Dialogue Institutions in Bangladesh. Dhaka, **30 October–1 November 2026**, two and a half days.

The exact venue and session leads remain unconfirmed in the supplied revised agendas. Both workshops finish at 12:30 on their final day. All session times are Dhaka time (UTC+6).

## Dashboard

The static website is in `dist/`. It has no build step or JavaScript dependencies. The dashboard includes the two Rev.1 programmes, 24 sessions, 20 individually downloadable participant handouts, two handout packs, calendar exports, the shared reference library, separate personal notebooks and planning spaces, and a locked facilitator workspace.

**Only the separately supplied Rev.1 agendas are used.** The superseded agendas in the source ZIPs are excluded from the website and participant packs. The supplied emails, technical proposal and brand guideline PDFs are not published.

The primary ITCILO logo is retained intact on white at the upper right. The interface uses the guide's blue `#284B96`, cyan `#00A3E0`, and Noto Sans. Font license: `dist/assets/fonts/OFL.txt`.

## Run locally

From the repository root:

```sh
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000/`. Use a server, rather than opening the HTML as a local file, for facilitator unlocking and encrypted downloads. Decryption requires a secure context: HTTPS when hosted, or localhost during development.

## GitHub Pages

The included `.github/workflows/pages.yml` deploys `dist/` when `main` changes. In the repository's **Settings → Pages**, select **GitHub Actions** as the source, then run the publication workflow if needed. There is no package install or build step.

All links are relative and work under a GitHub Pages repository subpath. Keep the complete `dist/` tree together.

## Facilitation

Open **Facilitator view** and use the workshop credentials supplied separately. The password is not stored in the repository. The username and password together derive an AES-256-GCM decryption key using PBKDF2-SHA-256 with 600,000 iterations and a random salt. The 24 slide decks, 24 trainer scripts and trainer reading previews are encrypted at rest. None of these original trainer files is published as a plaintext download. The slide decks include speaker notes.

The decryption key exists only in tab memory. Refresh, sign out or the 90-minute session check locks the view. This is password-based unlocking of encrypted teaching materials; it is not an online account service or a mechanism for managing participant identities. Participant handouts and the copied game's scenarios and feedback are public teaching resources. Teaching files share small encrypted storage parts; downloads reconstruct each original file exactly. Keep `dist/protected/parts/`, `recipes.enc` and `manifest.enc` together.

The facilitator workspace includes a discussion timer, a projector timer, and separate local game-result boards for the workshops. Set the discussion duration, start or pause, add 30 seconds, or reset. The timer never prevents the game from continuing.

## Call It What It Is

This duplicates the current Kenya game. Its twelve fictional public-health, higher-education and national scenarios, scoring functions and explanations are preserved. The Bangladesh edition has its own local practice save key. One device per team is recommended. Team and individual practice are available.

Choose the form, the setting and one useful change. Forms earn 10 points, settings 5, and a recognized change 5, up to 240. Two arguable cases allow alternative classifications. Recognition of a change uses keywords; it is a discussion prompt, not an assessment of the answer's full quality.

At the end, enter each team's six-character result code in **Facilitator view → Timer & game board**. Teams rank by points, then time. Times in result codes are rounded to five seconds. The board saves on that facilitator's device; it does not synchronize across devices or authenticate team-generated scores.

The original live-race connection remains available through the Kenya service. That service requires its own existing sign-in, independently of the Bangladesh materials password. Create a separate live session for each workshop. The existing service retains its Kenya sector categories; game participants' workshop selections use those existing category identifiers for compatibility. The local result-code board shows the Bangladesh workshop directly. No live race was created as part of development testing, and that external service's availability is not guaranteed by this static dashboard.

## Data and downloads

Personal notes, plans, checkmarks and locally entered result codes use browser local storage. Notebooks are separate for the workshops, can be exported as Markdown, and can be backed up or restored together as JSON. They are not sent to the facilitator or an external service. Local storage can be unavailable or cleared by browser settings: export important work.

The original live-race option sends team aliases, choices, timings and scores to the same secure service used by Kenya. Practice does not send results. No participant roster or real private institutional data is included.

Use the Word handouts for original formatting and printing. Dashboard previews show the supplied content in a readable HTML layout. The two participant packs contain the handouts and Rev.1 agenda, not the trainer materials.

For Secretariat Modules 6–11, the supplied files include a seven-template reusable pack. Separate exercise sheets mentioned in the scripts were not included in the uploaded ZIPs. The activity desk states this explicitly.

The NSDF reference is the **unofficial English translation supplied for the workshops**. Consult the authoritative Gazette text for legal interpretation. The reference library links to official ILO texts for Conventions Nos. 87, 98 and 144 rather than republishing local treaty PDFs. No country ratification status is asserted.

## Updating

Edit `dist/data.js` to change programme or handout metadata, `dist/app.js` for behavior and content, and `dist/styles.css` for the interface. Supplied Word documents remain unchanged. Encrypted resources cannot be edited or have their password changed by modifying a login condition: decrypt and re-encrypt the materials with the intended credentials, maintaining the documented file format.

See `VERIFICATION.md` for the checks and verification limits of this version.
