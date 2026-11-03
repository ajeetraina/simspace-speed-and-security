# Agents at Every Stage

```text no-run-button
   TRADITIONAL  human at every stage   →   attack surface = what YOU pull
   AGENTIC      agent at every stage   →   attack surface = what the AGENT pulls
```

*AI agents don't just answer any more - they act. In your pipeline they already
pull dependencies, generate Dockerfiles, edit infra, and open PRs on their own.
That autonomy is the point - and why it needs guardrails.*

## The "lethal trifecta"

Every useful agent has all three at once, *by design*:

1. **Access to private data** - code, internal systems, credentials.
2. **Exposure to untrusted content** - web pages, files, MCP responses that can carry instructions the agent will follow.
3. **Ability to act externally** - call APIs, send data out. Once it leaves, it's gone.

> [!IMPORTANT]
> You can't prompt or policy-doc the trifecta away. The only fix is an
> **enforcement layer at runtime**.

## What you'll do

| Step | What you'll see |
| --- | --- |
| Meet the app | A real Node.js service, **no Dockerfile** |
| An agent containerises it | Done well, in seconds |
| The same agent, on your host | It refuses an outright "harvest secrets" ask → then a poisoned file exfiltrates your `.env` anyway |
| Box the agent | Re-run it inside a sandbox - the blast radius collapses |

This is **Contain**, the first of the four Cs. First we show what an ungoverned
agent does on your host; then we put a wall around it.

Next: **Meet the Product Catalog**.
