# You Are the Coordinator

The team is blocked on one thing - and it's not a thing an agent should settle:

```text no-run-button
reviewer → you:
  products with no category assigned. Options:
    (a) show them under an "Uncategorized" category
    (b) hide them when a category filter is active
```

**There is no `sbx` command for this.** That's deliberate. sbx stood up the boxes,
isolated them, and enforced the policy - but the product call is yours. You make
it by telling the developer what to do:

```bash
sbx exec developer claude -p "Decision: unassigned products show under Uncategorized. Apply it."
```

The developer applies your decision in its box and commits to the shared
workspace. The factory did everything mechanical - read the task, wrote the code,
ran the tests, checked the policy - and then stopped exactly where human judgement
starts.

When the task is done, the role sandboxes are disposable. Tear them down:

```bash
sbx rm developer reviewer
```

The agents are gone; the project and its git history stay on your host:

```bash
git log --oneline -3
```

That's the factory, end to end, in real sbx:

```text no-run-button
  sbx create (per role) → sbx exec (give work) → YOU decide → sbx rm
         └── same workspace, same policy, isolated boxes ──┘
```

> [!IMPORTANT]
> Be clear about the division of labour. **sbx gives you**: an isolated box per
> agent, a shared workspace, one enforced policy across the team, disposable
> teardown. **sbx does not give you**: assignment, review, or decisions - that
> orchestration is a layer you add on top (you by hand, or a tool such as
> Docker Agent). Don't let a demo pretend otherwise.

## The five Cs, together

| C | What it gives the factory |
|---|---|
| **Contain** | an isolated microVM the agent can't escape |
| **Control** | a network policy that scopes what it can reach |
| **Choice** | the MCP tools and DHI pin it's allowed to use |
| **Capacity** | the same secured sandbox, reproduced for everyone |
| **Coordinate** | more than one boxed agent over one project - with you as coordinator |

A single agent is a demo. *Several agents, each in a boundary you defined, working
one project while you own the decisions* - that's a software factory you'd actually
trust. Take it to a real repo: `sbx create` a box per role over your project, give
each work with `sbx exec`, and decide the things only you should decide.
