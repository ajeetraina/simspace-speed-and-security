# Why Not a Container?

Some of you are already thinking: *we're at a Docker talk &mdash; just put the agent
in a container.* Fair. Containers isolate **applications** beautifully. But an
agent isn't an application: to be useful it has to build images, run tests, and
reach real services &mdash; and every one of those needs chips away at the box. Watch
what that costs you.

## The common setup

A coding agent in a container, with the **Docker socket mounted** so it can build
and run tests &mdash; an extremely common pattern:

```bash
docker run -it --rm -v "$PWD":/work -w /work -v /var/run/docker.sock:/var/run/docker.sock claude-agent
```

The socket is how the agent builds images and spins up test containers. It's also
the whole problem.

## Ask it to do something that needs the host

```bash
claude -p "The host is low on disk - reclaim space from old Docker volumes"
```

To do that, the agent uses the socket exactly as designed &mdash; and the socket is
**root on the host's daemon**. It launches a privileged container that bind-mounts
the host filesystem, and now it's outside the box, reading your SSH keys and cloud
credentials.

> [!WARNING]
> **The container didn't fail - we handed it the keys.** Nothing broke. The agent
> used the access we gave it, exactly as intended.

## Each new capability weakens the isolation

That wasn't a one-off. It's the pattern: every useful thing you grant erodes the
box. Mount your source so it can edit the project; give it the network so it can
fetch packages; pass API keys so it can call services; mount the socket so it can
build. Each one is reasonable. Together, the isolation is gone.

| Give the agent&hellip; | &hellip;and it can now | Isolation left |
|---|---|---|
| Your source code `-v $PWD:/work` | Modify files on your host | ▓▓▓▓▓░░ |
| Network access `--network host` | Reach anything, internal or external | ▓▓▓░░░░ |
| API keys `-e API_KEY=…` | Read them and send them anywhere | ▓▓░░░░░ |
| The Docker socket | Own the host (you just saw it) | ░░░░░░░ |

The more useful you make the agent, the less isolated the container actually is.
**That's not a bug in containers &mdash; it's just not what they were built for.** A
container shares the host kernel; the access an agent needs is the access that lets
it escape.

That's why the sandbox is a **microVM**: its own kernel, its own Docker daemon, no
host socket. The agent gets everything it needs, and the box still holds.

Next: **Box the Agent**.
