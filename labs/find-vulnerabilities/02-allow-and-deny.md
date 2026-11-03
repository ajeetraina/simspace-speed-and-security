# Allow and Deny

Two rule types sit on top of the default posture: **allow** opens a host, **deny**
closes one - and deny always wins.

## Allow the internal service

```bash
sbx policy allow network inventory.internal
```

`Rule added to policy local (scope: global)` - with a rule id and the resource
(`inventory.internal [tcp]`). Re-check and watch the decision flip:

```bash
sbx policy check network inventory.internal:8080
```

`Allowed` now - the agent can reach exactly what you decided, and nothing else new.

## Block a known-bad host

```bash
sbx policy deny network telemetry.vendor.example
```

Another rule added (`[tcp,udp]`). Deny takes precedence over any allow, so even a
broad allow rule can't re-open it - a simple way to stop a known exfiltration target.

> [!NOTE]
> Rules are global by default; add `--sandbox demo` to scope a rule to one sandbox
> instead of all of them. Remove one with `sbx policy rm network --resource <host>`.

Next: see every decision in the log.
