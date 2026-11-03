# What the Agent Can Reach

Containment is always on; **Control** is what you tune. The agent is already
boxed - every outbound request leaves through a proxy that allows or blocks it
against your policy. First, see the posture you start with.

## Governance profiles (if your org publishes them)

```bash
sbx policy profile ls
```

`No policy profiles found` - profiles are an optional **remote-governance** feature.
An org can publish ready-made postures (for example locked-down, balanced, open) and
you'd select one at create time with `--profile`. On a plain install there are none,
so you shape access directly with rules on top of **deny-by-default**.

## The active policy

```bash
sbx policy ls
```

The `local-policy` applies to **all** sandboxes: a set of network allows on top of
deny-by-default, plus filesystem rules. The agent can reach the LLM and common dev
endpoints (like `api.anthropic.com`); anything else is denied and logged.

> [!NOTE]
> You don't have to choose "all or nothing". You start from a sensible default
> and adjust - per host, per sandbox.

Next: check an endpoint before you run.
