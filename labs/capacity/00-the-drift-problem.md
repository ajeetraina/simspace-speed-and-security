# "Works on My Machine" Is the Enemy

You secured a sandbox in the earlier Cs. But a boundary that only exists on your
laptop isn't governance - it's a one-off. Capacity is the fourth C: the same
sandbox, reproduced for everyone.

## Run it the ad-hoc way

```bash
sbx run claude
```

It boots - but look at the warning. The agent, workspace, secrets, and policy all
come from **your local defaults**. A teammate running the very same command can
get a different setup.

```text no-run-button
  you            a teammate
  local defaults   different defaults
        ╲             ╱
      same command, different sandbox → different result
```

That drift is where "works on my machine" comes from - and where an *ungoverned*
sandbox sneaks in, because the policy you set never reaches the next person.

> [!NOTE]
> The fix is the same one we use for everything that matters: **declare it once,
> in a file, and share it like code.**

Next: declare the sandbox in sbxenv.yaml.
