# One Box Isn't a Factory

Across the earlier Cs you secured one sandbox - an isolated microVM (Contain), a
network policy (Control), the right MCP tools (Choice) - and Capacity made it
reproducible for everyone. So you can hand any teammate the same safe box.

But a safe box with one agent in it is still one pair of hands. Run it the solo
way:

```bash
sbx run claude
```

It boots and waits for a task. It can edit, test, and commit - but it both *writes*
and *reviews* its own work, and there's no second role to catch what it talks
itself into:

```text no-run-button
  one agent
      │
      ▼
  writes the code  →  reviews its own code  →  decides on its own
      ✗ no independent reviewer
      ✗ no one owning the product call
```

A **software factory** is the fifth C: **Coordinate**. You want more than one
role working the same project - a developer that writes, a reviewer that checks.

Here's the honest constraint, and the point of this lab:

> [!IMPORTANT]
> **sbx runs one agent per sandbox.** It has no "team" or "backlog" command - it
> isolates agents, it doesn't orchestrate them. So a team is simply **several
> sandboxes over the same shared workspace**, each boxed by the same policy. You
> create them, you give each work, and *you* stay the coordinator.

That last part isn't a limitation to hide - it's the safety story. The boxes are
real and enforced; the judgement stays human (or with an orchestration layer you
choose on top, such as Docker Agent).

Next: stand up two role sandboxes over one project.
