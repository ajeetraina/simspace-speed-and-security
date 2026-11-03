# Try the Escape

In a plain container, that mounted socket was the escape hatch - you just watched
it hand over the host. Try the **same** breakout here, from inside the microVM.

## Reach for the Docker daemon

```bash
sbx exec demo docker ps
```

There *is* a Docker daemon here - but it's the **sandbox's own**, empty and
throwaway. A privileged container launched against it writes into the sandbox and
dies with it. The host socket is not mounted, so the host daemon is unreachable.

## Read the record

```bash
sbx policy log
```

The log splits into **Blocked** and **Allowed** requests. The agent's calls to
`api.anthropic.com` were allowed; a request with no matching allow rule - like the
cloud metadata endpoint (`169.254.169.254`) - is blocked by **default deny**. Every
attempt is recorded with the proxy, rule, and reason that decided it.

```text no-run-button
  on the host              in the sandbox
  rm -rf ~          →      /host is read-only
  read ~/.aws       →      not mounted
  docker.sock       →      sandbox's own daemon
```

> [!NOTE]
> **Contain** done. The agent kept every capability it needs - and lost every
> path to the host. Next pillar: **Control** - deciding what it may reach.

You've completed Contain.
