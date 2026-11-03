# Check an Endpoint

Your agent needs to reach an internal service - `inventory.internal`. Will the
policy let it? You don't have to guess, and you don't have to run the agent to
find out.

## Start the sandbox

```bash
sbx run claude --name demo
```

## Ask the policy, read-only

```bash
sbx policy check network inventory.internal:8080
```

`Denied` - `Reason: no matching allow rule (default deny)`. The check runs the
**same authorizer the proxy uses** at request time, so what you see here is exactly
what the agent would hit; it also prints the governance source and context (here,
your local policy at global scope).

Nothing broke: the connection would simply be refused and logged. Now it's a
decision - allow it, or leave it blocked.

> [!NOTE]
> `sbx policy check` is the fast feedback loop: test a host against the policy
> without launching a task or waiting for the agent to trip over it.

Next: add the rule.
