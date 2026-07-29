# Working notes — gotchas that cost real time

Environment and workflow traps hit while building this. Written down because each
one was expensive to diagnose and will recur.

---

## 1. Claude's file mount can create, but not delete or replace

When Claude works in this repo from Cowork, its sandbox mounts the folder with
**create and rename allowed, delete and in-place replace denied**. Symptoms:

```
rm: cannot remove '…': Operation not permitted
warning: unable to unlink '.git/objects/…/tmp_obj_…': Operation not permitted
fatal: Unable to create '.git/index.lock': File exists
```

### What this breaks

**Any git command that rewrites `.git/index`.** Writing the index means creating
`index.lock`, then swapping it over the old index — and the swap needs delete.
So these all fail, sometimes *silently doing nothing*:

`git add` (normal index) · `git checkout` · `git reset` · `git merge` · `git stash`

Worse, each failed attempt **leaves a lock file behind that jams the next
command**. One failure cascades.

### What still works

| Need | Use |
|---|---|
| Stage + commit | `GIT_INDEX_FILE=/tmp/alt-index git read-tree HEAD && git add … && git commit` |
| Move a branch to another commit | `git update-ref refs/heads/main <branch>` — touches no index, no working tree |
| Clear a stuck lock | `mv .git/index.lock .git/index.lock.old` — rename works, delete doesn't |
| Read anything | All read-only git commands are fine |

`update-ref` is the one to reach for. A fast-forward merge is *only* a pointer
move; if the working tree already matches the target commit, `update-ref`
achieves the whole thing with none of the machinery that fails here.

### Symptoms that mean "stale index", not "lost work"

`git status` listing files as `D` (deleted) that are plainly on disk. The index
is out of date and can't be refreshed. **Nothing is lost.** Fix with
`git reset` from a terminal once locks are cleared.

### Sane division of labour

- **Claude:** edit, build, run tests, commit (via alt index), move branch pointers
- **You, in Terminal:** deletions, `find .git -name '*.lock*' -delete`, `git reset`

Anything Claude wants deleted has to be written down as a list instead — that's
why `DEPRECATED.md` existed rather than Claude just removing the folder.

---

## 2. Two copies of the engine will diverge within a day

The starter kit held its own copy of `wbyc-rangefinder-template.html`. It drifted
from the repo's within one working session — the copy missed a tokenisation pass
and two features, and building from it would have silently reverted both.

There is now one engine. Keep it that way. If something needs the engine, have it
read the engine.

---

## 3. Browser-capture gotchas

- **`save_to_disk` is ignored inside `browser_batch`.** Screenshots must be taken
  as standalone calls or the files never land, and you won't be told.
- **`resize_window` reports success and does nothing** when the Chrome window is
  maximised. Check `innerWidth` rather than trusting the return value.
- **Serve from the repo root**, not a subfolder, so both builds are reachable:
  `python3 -m http.server 8000`
- **Add `?nocoach=1`** so the first-run coach card doesn't cover every frame.
- **localStorage persists between captures.** Pins and memories survive a reload
  and will silently change what a screenshot shows — clear the relevant keys
  between beats, not just at the start.
- **`file://` won't open** via the browser tools (the URL gets an `https://`
  prefix), and the extension can't read local files anyway. Use the local server.

---

## 4. Verification that actually caught things

Habits worth keeping, each of which caught a real bug here:

- **Build guards.** `build.py` fails if a brand config is missing a key, or if
  another club's identity survives into the output. The second one caught a leak
  I'd missed by hand, and a `.webp` MIME fallback that would have shipped a
  working-but-wrong crest.
- **Byte-for-byte comparison.** After the engine inversion, WBYC's app rebuilt
  *identical* to the previously shipped file. That single check proved the whole
  refactor was behaviour-preserving.
- **Test the failure path.** The keepsake-photo tests mock a `QuotaExceededError`
  and assert it surfaces to the user. Storage filling up is the expected outcome
  of the chosen approach, so silence there would be the real bug.
