# The Single-Writer Fix

If no agent can see another's locks, stop asking them to share a writer. Let
**one** writer own the data, and let everyone else read. Run the same 400 lines of
work that way:

```bash
bash tests/race-control.sh
```

```bash
wc -l MEMORY.md
```

Two hundred of two hundred. Integrity OK. **Zero lost, every round.** Same mount,
same files, same work - the only thing that changed is that there is one writer
instead of two. A single writer never races itself.

```bash
cat MEMORY.md
```

Clean, in order, complete. That's the rule, and it scales up exactly as you'd
hope:

- **A shared cache?** Fill it once with one writer, then mount it read-only for
  the rest. (Measured: 3 writers filling at once → 2 of 9 builds pass; filled by
  one, then shared → 6 of 6.)
- **Shared agent memory?** Serve it through **one broker** that hands out *fencing
  tokens*, so a stale writer can't clobber a fresh one - the same shape as how
  `sbx` already injects credentials from outside the box. That design, with
  conformance tests, is in
  [{{repo}}](https://github.com/ffroliva/sbx-team-kit)'s
  `docs/single-writer-design.md`.

> [!IMPORTANT]
> This is the same lesson as every other C, one layer deeper. Contain, Control,
> Choice, Capacity, Coordinate - in all of them the boundary comes from the
> **platform**, never from the agent promising to behave. Shared state is no
> different: the coordination has to be enforced, not requested. One writer,
> everyone else read-only, a broker for the rest.

## What you proved

| You ran | You saw | Because |
|---|---|---|
| `race-test.sh` | 93-97% of writes lost, silently | two writers, locks invisible across VMs |
| `lock-visibility-test.sh` | `flock` / `fcntl` grant B the lock A holds | locks are per-VM kernel state |
| `race-control.sh` | 200/200, nothing lost | one writer never races itself |

And the honest footnote one more time: you proved the *shape* here. The evidence
lives in [{{repo}}](https://github.com/ffroliva/sbx-team-kit) - run the scripts
on real `sbx` and watch the same numbers come back.
