# The Agent Uses DHI

Here's the payoff. Hand the boxed agent the same "containerise this" task - but
now the DHI server is in the box, so it asks the catalog *before* choosing a base.

## Ask the boxed agent

```bash
claude -p "Containerise this service with a hardened base image"
```

Watch it query the DHI MCP server first:

- `dhi_list_repositories` → finds the hardened `dhi.io/node`
- `dhi_get_image_cves` → **0 critical · 0 high · 0 medium · 0 low**
- `dhi_get_image_attestations` → SBOM + SLSA provenance + VEX, signed by Docker

Then it writes a multi-stage Dockerfile on that base.

## See what it chose

```bash
cat Dockerfile
```

A distroless, non-root base - picked by the agent because the tool was there.

## Prove it - scan with Scout

The agent *claims* 0 CVEs. Don't take its word for it - measure the built image the
same way you measured the ungoverned one back in **Contain**:

```bash
docker scout quickview product-catalog:dhi
```

```text no-run-button
  Target             │  product-catalog:dhi      │    0C     0H     0M     0L
  Base image         │  dhi.io/node:24-debian13  │    0C     0H     0M     0L
```

Same tool, same prompt as the ungoverned run. In Contain, `docker scout quickview`
read **2C / 12H / 20M / 13L** over 431 packages; on the DHI hardened base it's
**0 / 0 / 0 / 0** over 211. The tool in the box changed the outcome.

> [!NOTE]
> The right tool in the box steered the agent to a better outcome. But notice the
> agent *chose* DHI - nothing stopped it from reaching for a third-party registry
> instead. Next, we make that choice impossible to get wrong.

Next: pin it to DHI, so the agent can't drift to a third-party registry.
