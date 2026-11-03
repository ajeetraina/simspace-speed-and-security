# A Locked Box Needs Tools

**Contain** gave the agent a boundary. **Control** decided what it can reach. But
a sandbox that's safe and can't do anything is useless - the boxed agent still
needs **your tools**. We'll give it one that fixes the CVEs the ungoverned agent
shipped back in Contain: **Docker Hardened Images (DHI)**, 0-CVE base images. And
we'll add it two ways, because sbx has two distinct mechanisms:

- **MCP servers** - external tool *servers* the agent calls through one governed
  gateway. We register the **DHI MCP server** so the agent queries the catalog and
  picks a 0-CVE base *before* it writes a single `FROM` line.
- **Mixin kits** - package tooling *into* the sandbox as one signed artifact: a
  CLI or server, its credentials, and its network rules. We wrap DHI as the
  **`dhi-mixin`** kit, which pins the agent to DHI *and* denies 3rd-party
  registries at the network edge - reproducible, and enforced.

Same tool, two mechanisms: the **MCP server** steers the agent to a better base;
the **kit** makes it stick and ships to the whole team. Credentials stay outside
the box in both.

> [!NOTE]
> This is **Choice**, the third C: you bring your own agent, tools, and endpoints -
> safely, inside the box.

Next: register the DHI MCP server.
