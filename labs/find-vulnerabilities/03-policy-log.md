# Read the Policy Log

Control isn't just rules - it's **visibility**. Every connection the agent tried,
allowed or blocked, is recorded with the rule that decided it.

## Read the log

```bash
sbx policy log
```

The log splits into **Blocked** and **Allowed** requests - each row showing the
sandbox, host, proxy, the reason that decided it, when it was last seen, and a
count. Condensed:

```text no-run-button
Blocked requests:
  HOST                           REASON
  inventory.internal:8080        No matching allow rule (default deny)   ← before your allow
  telemetry.vendor.example:443   denied by local rule                    ← your deny

Allowed requests:
  HOST                      REASON
  api.anthropic.com:443     (default allow)
  registry.npmjs.org:443    (default allow)
  inventory.internal:8080   (your allow rule)                            ← after your allow
```

You can see the agent trip over the default, your allow rule take effect, and the
deny rule stop exfiltration - all without trusting the agent to report it.

> [!NOTE]
> **Control** done. You decided what the agent may reach and proved it, rule by
> rule. Next pillar: **Choice** - giving the boxed agent the tools it needs.

You've completed Control.
