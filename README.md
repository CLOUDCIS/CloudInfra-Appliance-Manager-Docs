# CloudInfra Appliance Manager — documentation

Customer documentation for CloudInfra Appliance Manager, built with
[MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

Published to GitHub Pages on every push to `main`.

## Working on it locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

Then open <http://127.0.0.1:8000>.

## Building

```bash
.venv/bin/mkdocs build --strict
```

`--strict` is what CI uses: a broken link or a page missing from the nav fails the build. A
documentation site that silently drops a page is worse than one that refuses to publish.

## The control catalogue is generated

`docs/reference/controls.md` is generated from the appliance's own control packs, so it
describes the controls the product has rather than the ones somebody remembered shipping.

After changing the controls in the product repository:

```bash
python3 tools/generate-control-reference.py /path/to/CloudInfra-Appliance-Manager
```

Do not edit that page by hand — the next regeneration will overwrite it.

## Writing here

Two conventions worth keeping:

**Say what the product does, not what it aspires to.** Every factual claim here was checked
against the source or a running appliance. If you are not sure, check rather than phrase it
vaguely.

**Explain why, not just how.** Most of the surprising behaviour in this product is
deliberate — a restore that does not reload a service, a control that cannot be remediated,
a backup that will not write a file back. Documentation that lists the behaviour without the
reason leaves the reader thinking it is a bug.

## Screenshots

`docs/assets/screenshots/` is captured from a real appliance by a Playwright spec in the
product repository, so the images come from a running build driven by the same harness that
tests it rather than from somebody's browser at an unknown moment.

To regenerate after a change to the console:

```bash
cd /path/to/CloudInfra-Appliance-Manager/dashboard
APPLIANCE=https://<appliance-ip>:8443 \
ADMIN_PASSWORD='...' \
SHOTS_DIR=/path/to/docs/docs/assets/screenshots \
npx playwright test e2e/screenshots.spec.ts
```

Seed the appliance with an assessment, a drift check, a backup and a report first, or the
panels will be empty.
