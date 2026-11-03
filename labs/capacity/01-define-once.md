# Declare the Sandbox Once

Everything you tuned across the earlier Cs can be captured in **one file**:
`sbxenv.yaml`. It declares the sandbox so `sbx env run` can recreate it anywhere.

## Read the declaration

```bash
cat sbxenv.yaml
```

```text no-run-button
schemaVersion: "1"
name: product-catalog
agent: claude            # which agent runs
workspace: .             # what it can see
kits:                    # the DHI pinning kit from Choice
  - git+https://github.com/ajeetraina/docker-cloud-sandboxes-demo.git#dir=agent-cli/codex-dhi/dhi-mixin
secrets:                 # the DHI mirror tools' Docker Hub PAT
  dhi-mcp-pat:
    ref: "op://Engineering/DockerHub/pat"   # a SOURCE, not a value
    snapshot: true
```

The sandbox is no longer a pile of flags you remember to type. It's **data** -
the agent, its workspace mount, and the `dhi-mixin` kit from Choice, all pinned.
That one kit carries the whole DHI posture: the DHI MCP server, the steering, and
the deny of 3rd-party registries - so *every* teammate's sandbox pins DHI, not just
yours.

Notice the `secrets:` block carefully: it never contains a **value**. It declares
a **source** - here a 1Password `ref:` to the Docker Hub PAT the DHI mirror tools
need - that each developer's `sbx env` resolves **on their own host**. The repo
carries *how to get* the secret, never the secret itself.

> [!NOTE]
> This is the same move as a Dockerfile or a Compose file: the environment stops
> being tribal knowledge and becomes a reviewable artifact.

Next: share it like code.
