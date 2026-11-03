# Pin It to DHI: One Kit, No Drift

The last three sections wired the DHI MCP server into the box by hand, and the
agent used it. But "wired in" is **soft**: the agent picked DHI because the tool
was there *and* it chose to. Hand it a blunter prompt - "give me a hardened Node
image" - and it can still drift to a third-party hardened registry (Chainguard,
RapidFort, Wolfi), because that's what its training nudges it toward.

The `dhi-mixin` kit closes that gap. It packages the same DHI wiring **and** denies
the third-party registries at the network edge - so the agent can't reach them even
if it ignores every word of steering.

## Inspect the kit

```bash
sbx kit inspect "git+https://github.com/ajeetraina/docker-cloud-sandboxes-demo.git#dir=agent-cli/codex-dhi/dhi-mixin"
```

```text no-run-button
  Name:           dhi-mixin
  Kind:           mixin
  Schema:         v3
  Display:        Docker Hardened Images (DHI)
  Description:    Wires an agent to the hosted Docker Hardened Images MCP server (dhi.io), steers it to prefer DHI for hardened base images, and denies 3rd party registries at the network edge.

  Policies:
    Network:      1 allow, 7 deny
    Credentials:  2 sources
    Environment:  1 variables, 0 proxy-managed
    Commands:     0 install, 1 startup, 1 init files
```

One allow - `dhi.io` - and **seven denies**: `cgr.dev`, `*.cgr.dev`,
`chainguard.dev`, `*.chainguard.dev`, `wolfi.dev`, `*.wolfi.dev`, `apk.dag.dev`. The
kit also drops a steering file (a `CLAUDE.md` / `AGENTS.md`: "prefer DHI, never
Chainguard or Wolfi") and registers the DHI MCP server - the by-hand wiring from the
last three sections, packaged into one artifact.

## Add it to the running box

`--kit` only applies at **create** time, but `demo` already exists. `sbx kit add`
appends a mixin to a live sandbox: it recreates the container with the kit added,
preserving your workspace and the agent's session state.

```bash
sbx kit add demo "git+https://github.com/ajeetraina/docker-cloud-sandboxes-demo.git#dir=agent-cli/codex-dhi/dhi-mixin"
```

```text no-run-button
  ✓ sandbox demo — started
  KITS
    ✓ dhi-mixin — built
  Recreating 'demo' with kit: dhi-mixin…
    workspace and session state preserved
  ✓ demo ready — dhi-mixin active: DHI MCP registered · dhi.io allowed · 3rd-party registries denied
```

## Prove the deny

Steering only *asks* the agent to prefer DHI. The deny **guarantees** it. Check a
third-party registry against the policy:

```bash
sbx policy check network cgr.dev
```

```text no-run-button
Denied: cgr.dev
Governance: Local policy only
Context: global
Reason: denied by dhi-mixin (3rd-party registry block); deny beats allow
```

Chainguard is closed at the network edge. The agent can ask for it, and a drifting
prompt can reach for it - the pull fails before it ever leaves the box. DHI is the
only hardened base it *can* land on.

> [!NOTE]
> That's the full shape of **Choice**: the DHI MCP steers the agent to a better
> base, and the kit's deny makes it stick - a soft preference plus a hard boundary,
> in one artifact. Next pillar: **Capacity** - ship this exact kit to the whole team
> in an `sbxenv.yaml`, so every developer's sandbox pins DHI the same way.

You've completed Choice.
