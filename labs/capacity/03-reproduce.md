# Reproduce It Anywhere

This is the payoff. A new teammate clones the repo and runs **one command** - and
gets the exact sandbox you declared. But first: how do you *verify* what it will
set up - the kits, and especially the secrets - before anything is created?

## Verify first - sbx env plan

`sbx env plan` shows exactly what `sbx env run` would change **outside the box**,
and asks for approval before touching anything:

```bash
sbx env plan
```

```text no-run-button
── ENVIRONMENT PLAN
   product-catalog

   kits:
+    - source: git+…/docker-cloud-sandboxes-demo.git#dir=…/dhi-mixin  (DHI pin + 3rd-party deny)

   secrets:
+    dhi-mcp-pat  (ref op://Engineering/DockerHub/pat · snapshot)
       resolved on your host, needs your approval — never read from the file

+  sandbox:
+    name: product-catalog
+    agent: claude

   Plan: + 3 to add, ~ 0 to change, - 0 to destroy.
   ✓ not approved yet; applying asks once
```

This is where the configuration is verified. The `secrets:` line shows the kit's
credential will be **resolved from your host** (your 1Password), not read from the
repo - and nothing happens until you approve. If you *don't* have that source,
plan is where you find out, not after a broken sandbox is already running.

## Reproduce from the file

```bash
sbx env run
```

`sbx env run` applies that plan - resolves each secret from your host, provisions
the kits, creates the sandbox, and attaches. Compare it to the ad-hoc run from the
first section:

```text no-run-button
  before (ad-hoc)                 now (sbx env run)
  local defaults, drifts     →    declared agent + workspace + kits, every time
  secrets vary per machine   →    same source, resolved per host (never committed)
  policy stays on your box    →   shipped in the repo
```

## Confirm it

```bash
sbx ls
```

The `product-catalog` sandbox is running - same agent, workspace, and kit for
**every developer and every run**. Each person's secret was resolved from their
own source; no key ever travelled in the repo.

> [!NOTE]
> That's the full set. **Contain** gave the boundary, **Control** decided what it
> reaches, **Choice** put your tools inside it, and **Capacity** hands the whole
> thing to the team - reproducibly.

You've completed the 4 Cs. Run fast, without running wild.
