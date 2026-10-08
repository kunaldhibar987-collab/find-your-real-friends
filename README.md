# Find Your Real Friend — Pro Max Update

## What is included
- Cute multi-color scrapbook UI with responsive desktop/tablet/mobile layouts.
- Navbar stays at the top. The old navbar panda has been completely removed.
- Footer scene uses real wildlife photographs for lions, tigers, panda and parrots, with a static brown dry-bush illustration and close parrot placement.
- Question/answer cards attempt a real photo for every option. Brand/game photos use mapped source URLs; missing/broken sources fall back to a photo-search image and then a local SVG so the card never stays empty.
- Male/Female question banks, 10–15 questions, creator-selected correct answers.
- Friend gets exactly 3 choices per question.
- FastAPI + SQLite backend. Correct answers stay server-side.
- Persistent creator dashboard using a creator token stored in the browser. On the same device/browser, the dashboard loads saved quizzes from the database after refresh/reopening the site.
- Dashboard shows participant name, relationship, score, result, View and Remove actions.
- View Result page shows every question, selected answer, correct answer and correctness.
- Quiz links are generated from the current website origin, e.g. https://findyourfriend.site/take-quiz.html?quiz=ABC12345.

## Localhost: one-command architecture
1. Install Python 3.11+.
2. Open `START-BACKEND.bat`.
3. Install dependencies if needed: `pip install -r backend/requirements.txt`.
4. Open `http://127.0.0.1:8000/`.
5. The SQLite database is created automatically as `backend/findyourfriend.db`.
6. The frontend automatically uses `http://127.0.0.1:8000/api` on localhost and `/api` on a deployed domain. No API URL needs to be pasted into every page.

## Production / GoDaddy domain
The GoDaddy domain is only the address. The FastAPI application and database must be hosted on an online server. When the production server is serving this same frontend, the app automatically uses `/api`, so the final setup is:
`https://findyourfriend.site/` → FastAPI → `/api` → database.

## Important limitation about "who did not submit"
The system can permanently show everyone who submitted. It cannot identify a person who never opened/submitted a shared link because the website does not know that person's identity. To show named "Not attempted" invitees, an invite-list feature must be added (creator enters expected friend names before sharing).


## PRO MAX V7 changes
- Domain: findyourfriend.site
- Clean quiz links: https://findyourfriend.site/q/XXXXXXXX
- Local testing: http://127.0.0.1:8000/ and http://127.0.0.1:8000/q/XXXXXXXX
- Quiz name input removed; title is generated from creator name.
- Cute Male/Female gender cards replace the browser-default select.
- Every answer option uses a photo URL; exact product/game photos are used where available and photo-search fallbacks are used for every remaining option.
- Footer removed completely.
- Same-device creator dashboard appears on the home page and full dashboard; View and Remove actions are available.
- Creator token remains in localStorage and server data remains in backend/findyourfriend.db for local use.


## V7.1 Complete Photos Patch
Every question option now has an explicit relevant photo-search mapping where it is not an exact product/game image. Image loading has a two-stage real-photo fallback (LoremFlickr then Picsum) so option cards do not remain blank when a source blocks hotlinking.


## V7.2 — Correct Option-Matched Photos
- Removed random Picsum fallback.
- Removed random LoremFlickr fallback from the active photo path.
- Non-exact options now use a Bing image-search thumbnail query built from the exact option/category.
- Exact branded products/games still use dedicated image URLs first, then fall back to an exact Bing image search for that same item.
- This prevents unrelated photos such as travel/trees appearing for cricket, food, sneakers, etc.

### Quiz share-link styling fix
The `/q/{quiz_code}` route serves `take-quiz.html` from the site root, so `take-quiz.html` now declares `<base href="/">`. This keeps CSS, JavaScript, images, and navigation on the same root paths when a shared quiz link is opened. The API helper also falls back to `/api` if its config object is unavailable.


## Offline Play Corner
The `frontend/games.html` page is intentionally front-end only. It makes no API requests and includes local mini-games: Ludo Dash, Carrom Clash, Snakes & Ladders, Tic-Tac-Toe, Mini Chess, Memory Match, Color Blocks, Fruit March, Basketball Hoops, Spin Wheel, Slot Cars, Classic Snake, and Fruit Knife. Bot-style games use simple local browser logic. The result page offers the Play Corner after a score greater than 5.


## Final Play Corner behavior
- The Play Corner is a private surprise and is not shown in the normal navigation.
- It unlocks only after a quiz submission scores strictly above 5.
- Result page stores the last successful score locally and reveals the Play Corner button only when score > 5.
- Games are front-end only: no game fetch/API/backend calls.
- Solo games are player-controlled. Multiplayer-style games alternate player and automatic local bot turns.
- Creator quiz answers remain authoritative; each shared quiz question exposes exactly one creator-selected correct answer plus two random wrong options.
