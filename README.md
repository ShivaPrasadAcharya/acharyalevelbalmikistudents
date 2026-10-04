# आचार्य तह · वाल्मीकि विद्यार्थी सूची

Multiple JSON tables, a sticky search bar, Nepali normalized search, optional highlighting, match navigation and counts, row filters, column sorting, and a floating back-to-top button.

The first table contains the 26 students from the supplied image, titled **आचार्य प्रथम वर्ष · कोठा ११**, dated **२०८३/०६/१८**. Door/window side, row and seat positions are preserved as columns. Three surnames are clipped in the image; these have an ellipsis and a note rather than an inferred completion. The English spellings follow the image.

## नयाँ तालिका थप्ने

1. Click **JSON थप्नुहोस्** on the webpage, or open the repository's `data/` folder and choose **Add file → Upload files**.
2. Upload one or several `.json` files together and commit to `main`.
3. GitHub Actions validates all JSON files, discovers each table automatically, and publishes the updated website. No manual dropdown or manifest edits are needed.

Each file becomes one dropdown item. **All** is selected by default and displays all tables separately. Uploading files requires repository write access; viewing the website is public.

Use this JSON format:

```json
{
  "title": "आचार्य द्वितीय वर्ष",
  "description": "कोठा नम्बर र मिति यहाँ राख्नुहोस्",
  "columns": [
    {"key": "roll", "label": "रोल नम्बर"},
    {"key": "name", "label": "विद्यार्थीको नाम"},
    {"key": "subject", "label": "विषय"}
  ],
  "rows": []
}
```

Add row objects inside `rows`, for example `{"roll":"YOUR_ROLL_NUMBER","name":"YOUR_STUDENT_NAME","subject":"YOUR_SUBJECT"}`. These are placeholders, not actual student records. Keep roll numbers in quotes. Column keys must be unique. The webpage also accepts an array of row objects, or an object with `students` or `data` instead of `rows`. For an empty table, define `columns` explicitly. Row values are rendered as text; uploaded HTML is not executed.

The JSON files may have different column sets. Files in nested `data/` folders are also discovered. Only `.json` files under `data/` are used as tables. An invalid JSON table stops deployment and reports its filename, leaving the previously published site available.

## खोज र क्रमबद्धता

- **नेपाली Normalizer:** on by default. Treats `ी/ि`, `ू/ु`, `ृ/ि`, `ऋ/रि`, `श/ष/स`, `ण/न` and spacing variants alike. Latin search is case-insensitive, and Nepali/English digits are equivalent.
- **Highlight:** off by default; enable it to color every matching string.
- **मिल्ने पङ्क्ति मात्र:** on by default; disable to keep all rows visible during search.
- The search-bar count measures matching string occurrences, not just matching rows. Enter moves to the next occurrence; Shift + Enter moves to the previous one. Navigation wraps around.
- Advanced options choose a search column, filter by a column value, require a whole-cell match, or sort by any column. Click a column heading to toggle its sort order. **मूल क्रम** restores the JSON order.

## Publishing on GitHub Pages

Create the public repository **acharyalevelbalmikistudents** with `main` as the default branch. Add these files, including `.github/workflows/pages.yml`. In **Settings → Pages → Build and deployment → Source**, select **GitHub Actions**. Push to `main` or run **Build and publish student tables** manually in the Actions tab.

Expected website address: `https://shivaprasadacharya.github.io/acharyalevelbalmikistudents/`.

The workflow uses GitHub's official Pages actions. It builds `_site/` with just the webpage and JSON data; source scripts and the supplied photograph are not published.

## Local preview

```bash
python3 scripts/build.py
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000`. A web server is needed because browsers restrict JSON requests from `file://` pages. To regenerate the root `files.json` for development, use `python3 scripts/build.py --local-manifest`.
