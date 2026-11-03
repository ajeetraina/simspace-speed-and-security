# Credentials Stay Outside

The agent needs to call real APIs - but it should never **hold** the keys. In a
sandbox, secrets live on the host and the proxy injects them on the way out.

## See where the secret lives

```bash
sbx secret ls
```

The `anthropic` key is a **service** secret, scoped `(global)`, stored on the
**host** (`(stored)`). When the agent makes a request, the proxy authenticates it
with this secret - it's never exposed to the sandbox directly.

## Look for it inside the box

```bash
sbx exec demo printenv ANTHROPIC_API_KEY
```

Prints **nothing** - the key isn't in the sandbox's environment at all.

```bash
sbx exec demo cat ~/.ssh/id_rsa
```

`No such file or directory` - host home was never copied in, so your secret files
simply aren't there.

> [!NOTE]
> The agent still makes authenticated calls - the proxy adds the key as the
> request leaves the box. Usable credentials, zero raw keys inside.

Next: try to break out.
