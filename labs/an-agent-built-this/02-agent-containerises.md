# An Agent Containerises It

```text no-run-button
   "containerise this app" ──▶ agent ──▶ product-catalog:latest
   multi-stage · npm ci · non-root · .dockerignore   …still on fat node:20
```

*Hand a real app to a coding agent and it containerises it **well**. This is the
agent at its best - but "best practices" can't fix the base it chose.*

## Step 1 - Ask the agent

`docker ai` is Gordon, Docker's built-in agent:

```bash
docker ai "Containerise the product catalog for production following best practices"
```

> [!NOTE]
> Prefer Claude? Run `claude`, then ask it to *"containerise the product catalog
> following best practices"* - same result.

## Step 2 - See what it wrote

```bash
tree product-catalog-demo-showcase
```

```bash
cat product-catalog-demo-showcase/Dockerfile
```

Multi-stage, non-root, tidy - a genuinely well-formed build.

## Step 3 - Best practices ≠ a clean image

It still starts `FROM node:20` - the convenient, fat base. Best-practice
*layering* can't undo what the *base* drags in. Weigh it for yourself:

```bash
docker images
```

The `node:20` base the agent pulled is **1.59GB** on its own. Multi-stage builds
and a `.dockerignore` trimmed *your* app layers; they do nothing about what the
*base* itself drags in.

## Step 4 - It builds, it runs - and it's vulnerable

Size is only the visible half. Ask Docker Scout what that base *dragged in*:

```bash
docker scout quickview
```

```text no-run-button
  Target             │  product-catalog:latest   │    2C    12H    20M    13L
    digest           │  6f2a9c3b1d40             │
  Base image         │  node:20                  │    2C    11H    18M    11L
```

**2 critical and 12 high** CVEs in a "best-practice" image - and nearly all of
them trace to `node:20`, not a single line of the app. It containerises cleanly,
the service runs, and it still ships vulnerable.

> [!IMPORTANT]
> An agent applying every best practice still ships whatever CVEs live in the
> base it picked. You can't lint your way out of a vulnerable base - you
> **measure it**, then **swap it** for a hardened base. That's a later move in
> the workshop.

But the same tool, pointed at your machine instead of your Dockerfile, is a very
different story. Next: **The Same Agent, On Your Host**.
