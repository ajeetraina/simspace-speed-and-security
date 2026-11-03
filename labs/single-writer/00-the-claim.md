# The Slide Made a Claim

The Coordinate slide said something easy to nod along to and hard to believe
until you see it:

> Share the box. Don't share the writes. The same isolation that makes each
> sandbox safe - its own kernel - is exactly what makes shared memory unsafe.

In Coordinate you stood up a developer and a reviewer over **one shared
workspace**. That shared mount is the whole point - it's how the developer's
commit reaches the reviewer. This lab is about the moment it turns on you: two
agents writing the **same file at the same time**.

You are going to reproduce the failure, see exactly why it happens, and then fix
it. Three scripts are already in the workspace:

```bash
ls tests
```

> [!IMPORTANT]
> **This is a scripted replay - and I want to be honest about that.** There is no
> real `sbx`, no real microVM, and no real disk here, so this terminal cannot be
> *evidence* of anything. The **numbers** are real: they were measured on `sbx`
> 0.50.0 (Windows 11 host) and recorded in
> [{{repo}}](https://github.com/ffroliva/sbx-team-kit) - `FINDINGS.md`,
> sections 1 and 1b. To actually **prove** this, clone that repo and run these
> scripts against real `sbx`. A simulator can show you the *shape* of the
> failure; it can't stand in for the measurement. Don't let a demo pretend
> otherwise.

Check your tools are present, then move on to run the race:

```bash
sbx version
```
