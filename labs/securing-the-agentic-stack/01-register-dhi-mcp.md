# Register the DHI MCP Server

Registering a server tells sbx it *exists*. It doesn't attach it to anything yet,
and it persists across sessions.

## Add it by URL

```bash
sbx mcp add remotedhi --url https://dhi.io/mcp
```

That stores the server spec under the name `remotedhi`. Its tools become available
to agents in a sandbox - governed by your MCP policy.

## Confirm it's registered

```bash
sbx mcp ls
```

```bash
sbx mcp inspect remotedhi
```

`inspect` shows the transport and the tools it exposes - `dhi_list_repositories`,
`dhi_get_image_cves`, `dhi_get_image_attestations`, and more.

> [!NOTE]
> You can register a remote endpoint URL, a community-registry entry, a
> server-manifest URL, or even a DHI image ref - sbx auto-detects the type.

Next: authorize it and attach it to the sandbox.
