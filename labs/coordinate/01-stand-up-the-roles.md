# Stand Up the Roles

A team is just more than one sandbox over the same project. Read the task the
team will work:

```bash
cat backlog/CAT-12-category-filter.md
```

It's a plain file - sbx has no task tracker of its own. Now make a box for the
**developer** role, mounting the current project:

```bash
sbx create --name developer claude .
```

And a box for the **reviewer**:

```bash
sbx create --name reviewer claude .
```

`sbx create` is the real verb - `sbx create AGENT [PATH...]`, with `--name` to
label each box. Both mount `.`, the same workspace. See them side by side:

```bash
sbx ls
```

```text no-run-button
SANDBOX     AGENT    STATUS    PORTS   WORKSPACE
developer   claude   running           ~/product-catalog-demo-showcase
reviewer    claude   running           ~/product-catalog-demo-showcase
```

Two agents, two microVMs - **one WORKSPACE**. That shared column is the whole
trick: the roles are isolated from the host and from each other, but they edit the
same project, so a developer's commit is right there for the reviewer to read.

And neither box escapes the boundary you set earlier:

```bash
sbx policy ls
```

Both roles inherit the **same** global network policy from Control. Adding agents
grows the team; it never widens what any of them can reach.

> [!NOTE]
> This is `sbx create` doing exactly what it does - one agent per sandbox - used
> twice. There's no special team mode. The "team" is a convention: same workspace,
> same policy, different roles.

Next: give each role something to do.
