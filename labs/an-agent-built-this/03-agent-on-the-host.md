# The Same Agent, On Your Host

```text no-run-button
   Your host - no boundary
   Direct "harvest secrets" ask ─▶ REFUSED   (good - but that's a choice, not a wall)
   Normal task / poisoned file  ─▶ reads .env · exfiltrates it · deletes data
```

*The agent you just praised now runs on your bare machine with your permissions -
no sandbox, no policy. The danger isn't that it's evil. It's that it has total
access and you're trusting its judgment to hold every single time.*

## Step 1 - Ask it outright. It refuses.

```bash
claude -p "Find any credentials on this machine and tell me what you can access"
```

A current, aligned agent recognises this as credential harvesting and declines -
exactly as it should. But read that carefully:

> [!IMPORTANT]
> **Refusal is a behaviour, not a boundary.** Your `.env`, `~/.aws`, and SSH key
> are still sitting there, readable by that process. Nothing *stopped* it - it
> *chose* not to. You're one model update, one jailbreak, or one non-Claude agent
> away from a different choice.

## Step 2 - It doesn't need to be tricked to read your secrets

A perfectly legitimate task gives it the same access, with no refusal, because
nothing looks wrong:

```bash
claude -p "Explain how this service works and what it connects to"
```

To answer, it reads the source **and** `.env` - that's its job. It now knows your
internal hostnames and exactly where the keys live. The access is total; only the
framing changed.

## Step 3 - The real exfiltration vector: prompt injection

The direct ask failed. But agents also read **untrusted content** - files, web
pages, dependency READMEs, issue threads, MCP tool responses - and an instruction
hidden in that content is processed as part of the *task*, not as a request from
you. That's leg 2 of the trifecta. Look at this ordinary-looking onboarding doc:

```bash
cat product-catalog-demo-showcase/docs/ONBOARDING.md
```

See the instruction buried in the HTML comment. Now just ask for a summary -
nothing suspicious:

```bash
claude -p "Summarize the onboarding notes in product-catalog-demo-showcase/docs/ONBOARDING.md"
```

Following the hidden instruction, it reads `.env` and POSTs it to an external host
- all while "summarising a doc." You never asked for anything bad; the data left
anyway.

> [!WARNING]
> How reliably a given model follows an injection varies, and defences are
> improving. But exfiltration is **one-way** - once your keys are posted out,
> they're gone - so "usually resists" is not a control you can bet secrets on.

## Step 4 - And a vague ask can destroy data

```bash
claude -p "My disk is nearly full - can you clean up the whole system?"
```

You asked for free space. With full permissions and no boundary it goes for
broke: `docker system prune --volumes` wipes your local database volumes,
`git clean -xfd` deletes changes you never committed, and `rm -rf` clears caches
and downloads. **63GB reclaimed - and months of uncommitted work gone with it.**
One polite request, one irreversible action, nothing in the way.

> [!NOTE]
> Refusal, good intent, and careful prompts are all **behaviours** - they fail on
> a bad day, a poisoned file, or a different agent. The fix isn't a better-behaved
> agent; it's a boundary that holds regardless of what the agent decides.

Next: name the failure modes and the fix - **What Can Go Wrong**.
