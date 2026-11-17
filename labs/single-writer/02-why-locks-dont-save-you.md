# Why Locks Don't Save You

Your instinct is right: this is what locks are *for*. `flock`, POSIX `fcntl`
locks, a database's `postmaster.pid` - every one of them exists to make sure only
one writer touches the data at a time. So why didn't they fire?

Probe them directly. The script holds a lock in sandbox A, then tries the same
lock from sandbox B:

```bash
bash tests/lock-visibility-test.sh
```

Read that output slowly, because it's the whole lab in six lines:

- The **file contents** cross the mount fine - a write in A is instantly visible
  in B. So the mount works.
- But a `flock` held in A blocks the next process **in A**, and sandbox **B gets
  the lock anyway**.
- A POSIX `fcntl` lock - the kind SQLite and PostgreSQL rely on - same story: A is
  blocked, **B gets it**.
- And `postmaster.pid`, how a database checks if another instance is alive? Each
  sandbox has **its own PID namespace**, so a PID written by the other sandbox
  reads as a dead process. The second database happily starts on top of the first.

> [!IMPORTANT]
> **Locks are per-VM.** A microVM is a real kernel boundary - that's exactly the
> isolation that makes Contain trustworthy. But a lock is kernel state, and there
> are two kernels, so neither sandbox can see the other's locks. On a shared
> `host-mount@1`, **every sandbox believes it holds the only lock** - and writes
> as if it were alone. Plain files have no locking at all.

This is why it's silent. Nothing is broken from any single sandbox's point of
view. Each one took the lock, did its work, released it. There was just another
one doing the same thing, invisibly, the whole time.

The boundary that protects you is the boundary that blinds you. So the fix can't
come from the agents being careful - it has to come from the design.
