# Attach and Authorize

Registered isn't the same as usable. Many servers need authorization - and the
credential should be held **centrally**, never written into the sandbox.

## Check authorization status

```bash
sbx mcp auth status
```

`remotedhi` shows `not authorized`. Fix that:

```bash
sbx mcp auth remotedhi
```

The hosted control plane runs OAuth and holds the credential. The sandbox never
sees it - same credential-isolation idea as Contain, now for tools.

## Create the box with DHI locked in

Now start the sandbox with the DHI server fixed into it at creation. `--static-mcp`
is the locked, governed posture - the box's MCP set can't drift after boot:

```bash
sbx run claude --name demo --static-mcp remotedhi .
```

That boots the microVM through the proxy (host read-only), with `remotedhi` wired
into the agent's one MCP gateway. The agent can query DHI - and only the servers
you fixed at create time.

> [!NOTE]
> `--static-mcp` fixes the MCP set at creation. The agent always talks to one
> gateway, and authorization is held centrally - the box never holds the credential.

Next: watch the agent actually use it.
