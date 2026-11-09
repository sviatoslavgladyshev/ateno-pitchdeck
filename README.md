# Ateno — pitch deck (source)

The Ateno pitch deck, built from Python sources into a self-contained HTML presentation
(same viewer as the CQTS exciton talk: presenter view, notes, grid, phone remote).

| Folder / file | What it is |
|---|---|
| `slides_en.py` | All slides: text, layout, speaker notes |
| `build.py` | Builds `deck_en/` from the slide sources |
| `make_pdf.py` | Exports a built deck to a pixel-perfect PDF |
| `deck_en/` | Built deck: open `index.html` (or publish the folder on GitHub Pages) |
| `translate_ru.py` | Builds `deck_ru/` from `deck_en/` (run after `build.py en`, then `python3 thumbs.py deck_ru`) |
| `template/` | The viewer, taken from the CQTS talk (Nov 2026): navigation, presenter mode, animations, phone remote with laser pointer. Normally no need to touch |

## Setup (once)
```
pip install playwright pillow
playwright install chromium
```

## Edit → rebuild → export
1. Change text in `slides_en.py` (search for the sentence you want to change).
2. Rebuild: `python3 build.py en`.
3. Check: `cd deck_en && python3 -m http.server`, then open http://localhost:8000
4. PDF: `python3 make_pdf.py deck_en Ateno_Pitch_Deck_EN.pdf`

## Common edits
- **Round size**: $1.25M, on the `ask` slide.
- **Add a slide**: copy an existing `slides.append(sec("id", f'''...''', "notes", ...))` block, give it a new id, and raise `N_TOTAL` by one.
- **Remove a slide**: delete its block and lower `N_TOTAL`.
- **Animations**: `data-build-in="rise 1"` makes an element appear in order (fade / rise / pop + order number). `data-count="173161"` counts a number up. Classes `grow` / `shrink` animate bar widths.
- **Images / video**: put files in `deck_en/assets/` and reference them as `assets/name.jpg`. Videos: `<video src=... poster=... muted loop playsinline autoplay>`.

Pictures from the website (`place-*`, `map-*`, `device-main`) are in `deck_en/assets/`; they are renders and simulations, so they carry an *Illustration* / *Concept render* label.

## Viewer keys
→ / Space next · ← back · G all slides · N notes · P presenter · F full screen · R phone remote · B black screen

Honesty labels ("Concept render", "Illustrative build-up") are part of the slides on purpose — keep them.

## Private link with invitations (Firebase)
The deck is published at **https://pitch.ateno.co** (Firebase project `ateno-pitch`, free Spark plan). The site sends no email.

- **Admin:** run `python3 admin_link.py` once; it prints your personal admin link (also saved in `.admin-link`, not in git).
  Open it, confirm glsvyatoslav@gmail.com, and that browser stays admin. `--revoke` cancels old admin links.
- **Invite someone:** admin page → enter their email, pick 1–3 devices → *Create link* → paste the link into your own email to them.
  They open it, confirm their email, and see the deck. On those devices they can come back any time without the link.
- **Forwarding:** the link only works with the invited email and on at most the chosen number of devices.
  *Reset devices* moves access to new devices; *Remove* ends it; *Block* also black-lists the email. Whole domains can be black-listed.
- **Viewers** get no speaker notes, no presenter mode or phone remote. Printing/PDF, saving and copying are off; 3 screenshot attempts block access until you reset it.
- **Visits:** every opening with device, total time and seconds per slide. Each visit hides a code in the slides
  (invisible; raise a leaked screenshot's contrast to read it, then search it in admin). A phone camera can't be blocked.
- **Publish after a rebuild:** `python3 publish.py` (needs `firebase` and `gcloud` logged in). Details at the top of `publish.py`.
