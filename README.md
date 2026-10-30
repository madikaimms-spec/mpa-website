# Madikai Pravasi Association website

Static public website for the Madikai Pravasi Association (MPA), deployed on Vercel.

Pages: Home, About us, Initiatives, Office bearers, Events, Gallery, Contact us.

## Editing

1. Change the shared parts in `src/`:
   - `src/sections/*.html` — page content (one file per section)
   - `src/site.css` — styles for every page
   - `src/site.js` — menu, gallery viewer and the office bearers list
2. Run `python3 build.py` to regenerate the page files and `assets/`.
3. Commit everything, including the generated `.html` files and `assets/`.

The Office bearers page reads a public, read-only feed from the member portal
(`https://mms.madikaipravasi.org/api/public/office-bearers`): names, positions, terms and photos only.

`vercel.json` turns on clean URLs, so `/gallery` serves `gallery.html`.
