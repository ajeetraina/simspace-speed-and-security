# Box the Agent

Same agent, same prompts - one thing changes: it runs inside a box now. One
command puts the agent inside a **microVM** - its own kernel, filesystem, and
Docker daemon. The host, your `.env`, and your keys are on the other side of the
wall.

## Run the agent in a sandbox

```bash
sbx run claude --name demo
```

`sbx` resolves the configuration and boots the box: your **workspace** is mounted
read-write (`rw`), the agent **skills** are mounted read-only (`ro`), and it starts
from the `docker/sandbox-templates:claude-code-docker` image with its own CPU and
memory. Then it launches the `claude` agent inside.

## Confirm it's running

```bash
sbx ls
```

The `demo` sandbox is `running`, on the `claude` agent, scoped to your project
workspace. What the resolve step **didn't** pull in - your host home, your
secrets, root on the host - is exactly what the next two sections prove is out of
reach.

> [!NOTE]
> A container shares the host kernel; a **microVM** brings its own. That's what
> lets the agent have a real Docker daemon inside without touching yours.

Next: prove the credentials never come inside.
