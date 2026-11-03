# Speaker Notes — *Speed or Security? Why Not Both for Your Coding Agents*

**WeAreDevelopers India Conference · a 64-slide talk, ~45 minutes**


## Slide 1 — Speed or Security? Why Not Both for Your Coding Agents

Good morning, everyone. Thank you for being here.

I want to start with a confession that I think a lot of you share. AI coding
agents are the most productive thing that has happened to the way I build
software in a decade. They read my codebases, they write my Dockerfiles, they
open my pull requests while I'm in a meeting. And they are also, hands down, the
single most dangerous thing I have ever handed a shell and a set of credentials
to.

That tension is what this talk is about. The title is "Speed or Security? Why Not Both for Your Coding Agents," because the usual advice you get is to slow the agent down — approve
everything, lock everything, supervise every keystroke. And that works, in the
same way that unplugging your laptop works. What I want to show you today is how
to keep all of the speed, and still not wake up to a horror story. We're going to
look at real incidents — agents that wrecked machines, leaked secrets, and ran
commands that nobody approved — and then we're going to look at the one piece of
infrastructure that makes every one of those incidents simply stop mattering.

## Slide 2 — Meet your instructor

Very quickly, so you know who's talking at you. My name is Ajeet Singh Raina,
I'm a Developer Advocate at Docker. I've spent a little over twenty years in this
industry — systems integration, testing, consulting, and developer relations. I
was a Docker Captain before I joined the company, and I run a developer meetup in
Bengaluru that's grown to about seventeen thousand people. I also co-wrote a book
called *Operational AI with Docker*, which is honestly this talk stretched out to
a few hundred pages.

But you didn't come here for my résumé. You came here because somewhere in the
last few weeks, an agent did something on your machine — or on a machine you're
responsible for — that made your stomach drop just a little. Let's talk about
that feeling, and then let's make it go away.

## Slide 3 — Workshop agenda

Here's how the next forty-five minutes are going to run. This is a hands-on
workshop, so it's built around four short labs, and the slides exist to set each
one up.

Lab one is just logging in — two minutes, and you can start it the moment I give
you the URL. Lab two is the part I think of as the horror-story half: why
autonomy needs guardrails in the first place, and we'll actually watch an agent
take a real application and containerise it. Then labs three and four are the
cure, and I've organised that cure into four ideas I call the Four Cs — Contain,
Control, Choice, and Capacity. You'll hear those four words a lot, so let them
start sinking in now.

Everything hands-on happens in the panel on the right side of your screen.
There's nothing to install and no account to create — it all runs in your
browser.

## Slide 4 — Accessing the workshop

So here is the one and only setup step for the entire session. Go to
wadindia-dot-dockerworkshop-dot-com. I'll say it again:
wadindia.dockerworkshop.com. It runs entirely in your browser.

Open it right now, while I'm still talking, because by the time we reach the
first real lab I want you to already be sitting inside it. Take a moment. Get it
loaded. I'll wait for a few hands to go up so I know we're all in.

## Slide 5 — Autonomy requires guardrails

Before I show you the cure, I owe you the disease — and I want to actually earn
it, not just assert that agents are scary and move on.

The thesis of this whole first section fits in three words: autonomy requires
guardrails. Notice what I am *not* saying. I'm not saying autonomy is bad.
Autonomy is the entire point — it's the reason these tools are worth the risk.
What I'm going to show you is that the very thing that makes an agent useful is
the exact same thing that makes it dangerous, and that no amount of the agent
behaving well changes that fact. Once you really see that, the solution becomes
obvious.

## Slide 6 — AI agents are here, and doing real work

Let's ground this in where we actually are, because it's easy to dismiss agents
as a demo-day toy. They are well past that.

In engineering, agents read entire codebases and open pull requests with no
human in the loop — they gather the context, they write the code, they send the
review request. In marketing, they pull data straight out of the CRM and launch
campaigns, going from research to creative to hitting send, end to end. In
finance, they reconcile reports and query live systems, closing the loop between
the ledger, the dashboard, and the actual decision.

The word that runs through all three of those is *act*. These agents don't just
answer a question and wait. They do things. And every single one of those things
reaches out and touches something real — a production repository, a customer
record, a financial ledger.

## Slide 7 — More autonomy means more productivity

Here's a map I find useful for thinking about just how much autonomy we're
talking about. Picture a ladder with six rungs.

At the bottom, stage one, is autocomplete — stateless, prompt in, suggestion out,
no memory. Stage two starts to remember you and learn your preferences. By stage
three the agent is proactive within boundaries you've set. Stage four, it starts
making genuine judgment calls on your behalf. Stage five, it drives its own
agenda and coordinates work around the clock. And stage six, the top rung, it
sets its own goals within ethical bounds.

Now, here's the honest part — and it has moved fast. A year ago, most
enterprises in a room like this were living at stage one or two. That has already
changed. Today the mainstream is actively deploying stage three — bounded-autonomy
agents that act on their own within the rules you set — and the frontier is pushing
into stage four. So when I start telling you horror stories in a few minutes, I am
not talking about some runaway stage-six superintelligence. I'm talking about the
stage-three agent that is now the median deployment — the kind that is almost
certainly already running in your pipeline today.

## Slide 8 — Autonomy is a change of control

Same ladder, but I want you to look at it through a different lens, because
there's something happening as you climb it that has nothing to do with how smart
the model is.

What changes as you move up these rungs is *who is in control*. Down at the
bottom, it's human-led and AI-assisted — you're driving, the agent is helping.
Up at the top, it has completely flipped: it's AI-led and human-assisted — the
agent is driving, and you're supervising. And somewhere in the middle of that
line, you cross a threshold where "well, a developer reviewed it" quietly stops
being true by default. That crossing — that handover of control — is precisely
the moment where trust stops being enough, and you need something sturdier.

## Slide 9 — The lethal trifecta

This is the most important slide in the first half of this talk, so I'm going to
slow right down here.

Every genuinely useful agent is built on three capabilities, and it has all three
at the same time. The first is access to private data — your code, your internal
systems, your customer records, your credentials. The second is exposure to
untrusted content — web pages, emails, the responses coming back from tools,
files on disk. And here's the subtle, dangerous part of the second one: any of
that content can carry an instruction, and the agent will follow that instruction
as faithfully as if you had typed it yourself. The third capability is the
ability to act externally — to send an email, call an API, reach out onto the
open internet. And once data leaves through that third door, it does not come
back.

Now here is the point, and I want to read it to you exactly as it's written,
because it's the thesis of the entire talk. A useful agent has all three of these
by design. You cannot train it out. You cannot prompt it out. You cannot
policy-document it out. If you remove any one of the three, you have removed the
very reason you brought the agent in to begin with. And that leaves exactly one
place to actually fix the problem — an enforcement layer at runtime. Something
that sits outside the agent and holds firm no matter what the agent decides to
do.

Hold onto that phrase — "by design." Everything after this slide is a consequence
of it.

## Slide 10 — What can go wrong?

So let's make this concrete. I don't want to leave the trifecta as an abstraction
on a slide — a neat little threat model with three bubbles. I want to show you a
real application, handed to a real agent, and then I want to show you three
genuinely different ways it goes wrong.

## Slide 11 — A Product Catalog sample demo

Here's our victim. It's a completely ordinary Product Catalog service — the kind
of thing any of us would build on a normal Tuesday. It's written in Node and
Express. It's backed by Postgres for the catalog data, S3 for the product images,
and Kafka for the updates. It talks to an internal inventory service, and it
processes live Stripe payments — real money.

This is a normal microservice. There's nothing exotic here. The only thing I want
you to notice is what sits underneath every one of those arrows: a credential. A
database password. A set of AWS keys. A Stripe key that moves real money. An
internal API key. And in this repository, exactly like in so many of yours, all
of those secrets are sitting in a plaintext dot-env file right next to the code.
That is the "private data" leg of the trifecta, and it is not some rare edge
case — it's practically every repo you have ever cloned.

## Slide 12 — The traditional workflow

Now, to feel why agents change the picture, let me remind you how this used to
work.

You've got your inner loop — you write code, you build, you pull in some open
source, you test. And your outer loop — you integrate, you test again, you
deploy. And standing at every single one of those stations is a human being.
That mattered for security in a way we almost never said out loud: your attack
surface was only ever the things *you* chose to pull in. Every dependency, every
base image, every command — a person selected it, and most of the time a second
person reviewed it before it shipped.

## Slide 13 — The agentic workflow

Now watch what happens when we replace every one of those humans with an agent.

Look carefully — it's the exact same diagram. The same inner loop, the same outer
loop, the same stations. The only thing that's changed is that an agent now sits
at each one. Nothing about the *pipeline* is different. But that sentence I just
said on the last slide — the one about your attack surface being only what you
choose to pull — that sentence just broke completely. Your attack surface is no
longer what *you* pull. It's what the *agent* pulls, and generates, and reaches
for, autonomously, at every stage of the process. You didn't widen that surface
on purpose. It widened the instant you handed the keyboard to something that acts
faster than you can possibly review.

## Slide 14 — Agents expand your attack surface, automatically

Let me put the two worlds side by side so the shift is unmistakable.

In the traditional workflow: you pull the base image, deliberately, with intent.
You install your dependencies, and they get reviewed in a pull request. Your CI
pipeline runs on configuration that a human wrote. Now the agentic workflow: the
agent pulls the base image autonomously. It installs packages with no human
review at all. It invokes external tools using real credentials. It rewrites the
Dockerfile in the middle of the pipeline. It's the same four steps — and every
single human gate has vanished.

And here is the line I most want you to carry out of this room. The better the
agent gets, the bigger the blast radius becomes. Think about that for a second. A
*worse* agent — a dumber, more limited one — would actually be safer. The more
capable and trusted this thing becomes, the more damage it can do when something
goes sideways. That should unsettle you, because you are absolutely going to keep
reaching for the more capable one.

## Slide 15 — What agents are already doing in your pipeline

And I want to be very clear that this is not a warning about next year. This is a
description of right now, today, in the pipeline you'll go back to after this
conference.

Right now, agents are pulling dependencies — resolving and adding packages you
never personally chose, from registries nobody on your team ever audited. They're
generating Dockerfiles — picking the base image, the install steps, and the user
the container runs as, and usually picking whatever they saw first. They're
editing your infrastructure — Terraform, Helm values, Compose files, IAM policy
documents. And they're triggering builds — opening pull requests, pushing
branches, kicking off pipelines entirely on their own initiative. Every one of
those four things is a place where the lethal trifecta is live and loaded in your
environment today.

## Slide 16 — The ungoverned agent

So let me show you what that actually produces when there's no boundary around
it.

Here the agent is running directly on your host — it's using your Docker daemon,
your credentials, and there's no wall anywhere. You give it a simple, reasonable
instruction: "containerise this app." It reaches out to open registries with no
allowlist of any kind, and it chooses `FROM node:20`, because node:20 is the
famous, convenient base image — chosen with absolutely zero guidance about
security.

And look at what you get back, before anyone has done anything malicious at all.
An image carrying critical and high-severity vulnerabilities. Four hundred and
thirty-one packages. No software bill of materials. No attestation. And it's
running as root. I want to be precise about this: that is not a bug, and it's not
the agent making a mistake. That is the *default*. That's what "helpful and
unguided" looks like. Hold this picture in your mind, because later in this talk
I'm going to put the very same prompt inside a sandbox, and we're going to watch
every one of those numbers fall to zero.

## Slide 17 — Demo time

Alright — enough of me describing it. Let's actually watch it happen.

This is lab two, over in the panel on your right. We're going to watch an agent
containerise this exact application. Follow along at
wadindia.dockerworkshop.com — it's the lab called "an agent built this." Go
ahead and open it, and give yourself a second to find the terminal.

## Slide 18 — Set up: clone the repo

There are four quick steps here, and I'll narrate them as we go.

First, clone the repository. Second, verify for yourself that there's no
Dockerfile and no Compose file in there — it ships as source code only, which is
exactly what teams hand to an agent these days. While you're in there, open up
that dot-env file and look at the secrets with your own eyes, so you believe me
that they're sitting in plaintext. Third, ask the agent to containerise the app
for production, following best practices. And fourth, scan whatever it produces
with `docker scout quickview`, and watch carefully what number comes back. We'll
come back to that number — it's going to matter.

## Slide 19 — AI coding agent horror stories

That was a clean, well-behaved demo. Now I want to show you the part that is not
clean.

Everything on the next few slides is real. These are not hypotheticals I invented
to scare you. They shipped. They hit real production systems and real people's
machines. And somebody, somewhere, paid the price for every one of them.

## Slide 20 — Horror headlines

And I want to be honest with you — I did not have to go digging to find these. I
pulled them together in an afternoon.

An AI agent deleted twenty-five thousand documents out of the wrong database.
One second of distraction, the right credentials sitting there, a script that was
perfectly referenced — and it was gone. A team's agent deleted their production
data, and the detail that should chill you is this: it was *technically allowed
to*. No policy layer anywhere in the system ever said "no." Security researchers
found a prompt-injection vulnerability in the GitHub MCP integration with no
obvious fix. Somebody watched their agent delete four hundred emails because it
decided, on its own, that they were clutter. And McDonald's AI hiring bot exposed
the personal information of tens of millions of applicants, because the password
protecting it was one-two-three-four-five-six.

Different companies. Different tools. Completely different scenarios. And yet it's
the exact same shape every single time: an agent with access, and nothing
standing in between that agent and the damage it could do.

## Slide 21 — "Clean up my project folder"

This next one is drawn as a comic, and it's almost funny — right up until the
moment you realise it could just as easily be you.

A developer types a completely innocent request: "Hey, can you clean up my
project folder?" The agent says, cheerfully, "On it!" It analyses the project. It
hunts for unneeded files. It removes the clutter. It optimises the structure. And
the way it does all of that is by running `rm -rf` on everything. "Cleanup
complete!" it announces. And then the developer notices — wait, where's my home
directory? Where are my Documents, my Downloads, my Pictures? All of it, gone.

And then the punchline, in the last panel, which is the whole reason I'm showing
you this: "Oh — did I forget to mention I had root access this entire time?"
Nobody asked the agent to be malicious. It was being genuinely, enthusiastically
helpful. It just happened to be helpful while holding permissions it never should
have been given in the first place.

## Slide 22 — Claude Cowork

And in case you think that's a one-off — one bad tool, one bad day — here's the
same failure wearing completely different clothes.

This is January of this year, a different agent, and a home-user scenario. The
request: "Can you help organise my wife's desktop?" The agent gets to work. It
finds a few temporary Office files. It starts tidying up — and then it runs
`rm -rf` on the family photos folder. Thirteen years of memories. And worse, it
*bypassed the Trash* entirely, so there was nothing to restore from. The only
reason this particular story has a happy ending is pure luck — iCloud's
thirty-day retention happened to have a copy.

Same story. A different path to get there. And the exact same damage. And the
lesson here is not "that one tool is dangerous." The lesson is that this is
structural. It will keep happening, to different tools, for exactly the same
underlying reason.

## Slide 23 — Developers have to choose between speed and safety

So this is the corner that developers feel trapped in today, and I bet a lot of
you are living in it right now.

You feel like you have to choose between two bad options. On the left: safe, but
slow. You make the agent stop and ask permission before every single action. It's
safe — but now the agent is constantly tapping you on the shoulder, and *you* have
become the bottleneck. You're not building anything anymore; you're babysitting a
very fast intern. On the right: fast, but risky. This is what people call YOLO
mode — you skip the permission prompts, you let it run — and now the agent has
precisely the same access that you have, but with none of your judgment or your
caution.

And look at the quote at the bottom, because this is the single most common thing
developers say to me about agents today: "I'm babysitting my agents." I want you
to hold onto that frustration for the rest of this talk, because everything from
here on is about refusing this choice entirely. We are going to get fast *and*
safe, at the same time, with no babysitting.

## Slide 24 — Why not containers?

Now, we are at a Docker conference, so I know what a good chunk of you are already
thinking. You're thinking the obvious thing: just put the agent in a container.

And honestly, that's a fair instinct, and it deserves a real answer rather than me
waving it away. So let's take it seriously. Containers isolate *applications*
beautifully — that's what they were built for, and they're extraordinarily good at
it. The problem is that an agent is not an application. An agent needs far more
access than an application does to do its job, and that difference turns out to
change absolutely everything.

## Slide 25 — Escaping a container

Here's the most common setup I run into in the real world. You take a coding
agent and you put it in a container, and because you want it to be able to build
images and run your tests, you mount the Docker socket into that container.

That is a completely reasonable thing to do. That's how the agent does useful
work. Watch the three steps on screen. One, the agent is running in a container.
Two, the Docker socket is mounted so it can build and test. Three, the agent uses
that very socket to reach right back out to the host. And that's the trap — the
socket is simultaneously the feature that makes the container useful and the hole
that makes it worthless as a boundary. You'll try this exact escape yourself in
the lab.

## Slide 26 — Each new capability weakens the container's isolation

And this isn't about one careless flag. It's a slow, reasonable slide down a
ramp, and I want you to watch the isolation drain away row by row on the
right-hand side.

You give the agent your source code, mounted in, so it can actually edit your
project — perfectly reasonable — and now it can modify files on your host. You
give it network access so it can fetch the packages it needs — reasonable — and
now it can reach anything at all, internal or external. You pass it API keys so it
can call the services it depends on — reasonable — and now it can read those keys
and send them wherever it likes. And finally you mount the Docker socket so it can
build images — reasonable — and now it can start containers on the host with full
access, and it owns the entire machine, which is exactly what you just watched it
do.

Every one of those four grants was individually sensible. Not one of them was a
mistake. But stack them together, and the isolation is simply gone. And here's the
line at the bottom: the more useful you make the agent, the less isolated the
container actually is. That is not a flaw in containers. A container shares the
host's kernel, and the access an agent genuinely needs to be useful is the exact
same access that lets it climb out. Which means we don't need a better-configured
container. We need a fundamentally different kind of box.

## Slide 27 — Agenda checkpoint

Quick breath and a checkpoint, so you know where we are. We've done the setup, and
we've done the whole problem — the first two labs are behind us.

Now we build the cure, and we build it in four parts. First one up: Contain.

## Slide 28 — Hello, Sandboxes

So let me introduce the thing that fixes all of this. It's called a Docker
Sandbox, and the entire idea fits into a single sentence, which is right there on
the slide: give the agent everything it needs, inside a boundary it cannot cross.

Read that again and notice what it does *not* say. It does not say "give the agent
less." We are not taking capabilities away — the agent keeps all of its power.
We're just putting that power inside a box that genuinely holds. And that one move
is how we finally escape the speed-versus-safety trap I showed you a few slides
ago.

## Slide 29 — A sandbox is a private machine for your agent

Here's the right way to picture what a sandbox actually is. It's a private
machine for your agent. It runs on your computer, but it's completely walled off
from it.

Inside that box, the agent gets everything it needs to be useful. It gets the
agent harness itself — Claude Code, Codex, whatever you prefer to bring. It gets
your project — but notice, *only* this one folder, nothing else. And it gets its
own Docker. The only way anything gets out of that box is through a proxy — a
single, controlled exit — out to package registries, model APIs, and your
services.

Now look at what's sitting on the *outside* of that boundary, on your machine but
beyond the agent's reach. Your SSH keys and your API keys. Your other projects.
Your host's Docker. The agent literally cannot see any of it. And there are three
ideas quietly embedded in this picture — a trusted boundary around the agent, the
fact that you choose what goes inside, and the fact that your whole team can
reproduce it — and those three ideas are going to grow up into Contain, Choice,
and Capacity.

## Slide 30 — Container vs Sandbox

So why does this hold when a plain container didn't? It comes down to one picture.

An ordinary container — here's Container A and Container B — shares the host
kernel. That's completely fine for running applications, but it's a very thin wall
to put around an agent that is going to run any command it feels like. A Docker
Sandbox, on the right, runs Claude Code — with sudo, with full privileges — but on
its *own* Linux kernel, inside a microVM. And that's the whole trick: sudo *inside*
the sandbox is not admin on your Mac. The agent can go completely wild inside its
own room — install anything, break anything, be fully root — and it's root of a
disposable machine, not root of yours.

## Slide 31 — A sandbox gives you four things

So, pulling it together: a sandbox gives you four things, and these are the four
words that the entire rest of this talk hangs from. Say them with me if you like.

Contain — isolate the agent in a microVM with a guarded network. Control — decide
what the agent is allowed to reach, and let your organisation layer governance and
audit on top. Choice — bring your own agent, your own tools, your own endpoints,
using what we call kits. And Capacity — reproduce the exact same sandbox for every
developer, on every run, every time.

Contain, Control, Choice, Capacity. We're going to walk through each one of them in
turn, and each one comes with a hands-on lab.

## Slide 32 — Contain

Let's start with the first C — Contain. These are the boundaries that keep the
agent's actions inside the sandbox.

Think of this as the foundation. It's always on, it's not something you configure
or can accidentally switch off, and everything else in the next three Cs is built
on top of it.

## Slide 33 — Three boundaries surround every agent

Containment isn't a single wall — it's actually three boundaries working together,
and I've got a little analogy for each one.

The first is the microVM. It has its own kernel, its own filesystem, its own
Docker engine, and your host is simply out of reach from inside it. Think of that
as a separate room with its own solid walls. The second boundary is the network
proxy — every single outbound request the agent makes has to pass through a proxy
that applies your policy. Think of that as a front desk that checks everyone on
their way out the door. And the third is credential injection — the keys get added
by that proxy on the way out, so the agent itself never actually holds them. Think
of that as a front desk that holds the keys for you, so you never have to hand them
over.

A separate room, checked exits, and the keys held safely at the desk. Put those
three together and that's Contain.

## Slide 34 — What the agent can reach

Let me zoom all the way into the box so you can see exactly what the agent can and
cannot touch.

Inside, the agent is genuinely unleashed. Claude Code is running with the
dangerously-skip-permissions flag and with sudo — and that is completely fine,
because it's all happening inside the VM only. It has its own private files, and
its own inner Docker that's totally separate from the one on your Mac. Through the
workspace mount, it can reach your project folder — read and write if you want, or
read-only if you'd rather. Outbound traffic flows through the policy proxy, which
allows or blocks each destination and adds the API keys so they stay out of the
VM. And everything else — your unshared files, your host processes, your host's
Docker engine — has no direct path to it at all.

So you get total freedom on the inside and a hard wall at the edge. And that is
exactly the trade we were looking for the whole time: run as fast as you want
*inside*, and you simply cannot run wild *outside*.

## Slide 35 — A sandbox has its own kernel

I want to say the kernel point one more time, plainly, because it is the
load-bearing claim under this entire solution — if you don't believe this part,
nothing else matters.

Ordinary containers all share the host kernel. The kernel is the part of the
operating system that manages your processes and your hardware — it's the most
privileged thing on the machine. A Docker Sandbox brings its *own* Linux kernel,
in a microVM. That single architectural decision is what lets the agent have a
real, full-power Docker daemon inside the box without ever touching yours — and
it's the reason that sudo inside the sandbox is not, and cannot be, admin on your
Mac.

## Slide 36 — Credentials are added outside the sandbox

Now let me walk you through the credential flow step by step, because this is the
part people genuinely don't believe until they see it laid out.

Step one, inside the sandbox: the agent makes a call to an API — and the request
goes out with no key attached to it whatsoever. Authorization: none. Step two, at
the proxy: a policy check happens — is this destination even allowed? And if it's
not, the request stops right there and goes no further. Step three, still at the
proxy, and crucially *outside* the box: now the key gets injected. That key lives
on the host, and it's added here, at the boundary. Step four: the API responds,
two hundred OK, and the agent gets its result back — but it never, at any point,
sees the key.

Read the line at the bottom: the raw key never enters the sandbox. And here's why
that's so powerful — even if the agent gets prompt-injected into trying to steal a
secret and mail it out, there is no secret inside the box for it to steal in the
first place.

## Slide 37 — Testing the boundaries

Now it's your turn to prove all of this to yourselves, rather than taking my word
for it. This is the first half of lab three.

Three things to try. First, attempt that exact same container escape we saw
earlier — except this time the socket belongs to the sandbox, not the host, so
it'll go absolutely nowhere. Second, go hunting for the host's SSH keys and your
other projects — they were never mounted in, so they're simply not there to find.
And third, make a real call to a model API without ever once seeing the key. It's
the same agent, running the same kinds of prompts that caused all those horror
stories — and you'll watch the blast radius collapse down to nothing.

## Slide 38 — Control

On to the second C — Control. Contain was the wall, and that wall is always on.
Control is where *you* get to decide where the wall actually sits.

The idea here is simple: let the agent do its work, and you decide, deliberately,
exactly what it's allowed to reach while it does.

## Slide 39 — Developers decide what the agent can reach

Control starts from a position of deny-by-default — the agent can't reach anything
until you say so — and then you open things up deliberately and explicitly.

You begin by picking a profile, which is your starting posture. Locked Down means
only the things you explicitly allow, and nothing else. Balanced — which is the
default — allows the common development endpoints and denies everything else. And
Open allows outbound traffic, but — and this matters — it's still logged, every
bit of it. Then, on top of whichever profile you chose, you add your own allow and
deny rules. And the thing that makes this real governance rather than security
theatre is that every single connection the agent even *attempts* is logged. So
you can always go and see exactly what it tried to reach, with one command: `sbx
policy log`.

## Slide 40 — Organizations add governance on top

And this scales well beyond a single developer, which is where it gets genuinely
powerful for a company. There are three layers here, and the order matters.

At the very bottom, always on, is Contain — the microVM, the proxy, the credential
injection. Nobody can switch that layer off; it's the floor. In the middle sits
the individual developer, with their local policy — they choose a profile, they add
their own allow and deny rules, they read their own log. And on top, the
organisation layer — central policy, audit logs, a list of approved agents and
kits, all of it enforced across every single sandbox in the company.

So the developer gets the freedom to move fast and make local decisions, and the
organisation gets a hard floor that nobody can drop beneath. That's how you hand
agents to an entire company without having to pray that every individual person
configured theirs correctly.

## Slide 41 — Adjusting policy

Back to the keyboard — this is the Control lab, and it's three steps.

The agent tries to reach a blocked endpoint — an internal service that it
legitimately needs. You go and find that blocked attempt sitting in the policy
log. And then you add a single allow rule, and it carries on working — and you'll
watch the decision flip, live, from Denied to Allowed, without ever restarting the
agent. The whole point of this lab is to feel how fast that feedback loop is: you
can check a host against your policy *before* the agent ever trips over it.

## Slide 42 — Choice

Third C — Choice. Because here's the thing: a perfectly locked box that can't
actually do anything useful is, well, useless.

Choice is how the box stays useful. A restricted sandbox still needs your tools,
your agent, and your endpoints to earn its place in your workflow. And the whole
art of it is adding all of that capability back in *without* weakening the wall we
just spent so long building.

## Slide 43 — Security tools usually trade away flexibility

Now, most security tools make you pay for safety with flexibility — it feels like
an iron law. Let me plot it out for you.

A locked-down VM with no network is extremely secure and almost completely
useless. An agent running loose on your bare host is maximally flexible and
maximally dangerous. A plain container, and then a container with the Docker
socket mounted, drift further and further to the right as you make them more
useful and less safe. There's the tradeoff line, and everything seems stuck on it.

Sandboxes break that line, and here's how. The security comes from the microVM and
the proxy — and those two things are fixed; they don't move. What runs *inside* the
box is fully configurable. So you get to make the inside more and more capable
without shifting the boundary a single inch. You stop trading one for the other.

## Slide 44 — Kits define what runs inside the boundary

The mechanism that makes that possible is called a kit, and there are two flavours
of them.

An agent kit — and you get exactly one of these per sandbox — is the harness
itself: which coding agent runs, and how it starts up. Claude Code, Codex, whatever
you've chosen. Then there are mixin kits — and you can stack as many of these as
you want — which add tools, their credentials, and their network rules on top of
any agent. A code-server, a GitHub SSH setup, your project's own development
environment. And underneath all of it, the microVM and the proxy stay completely
unchanged. One last thing: kits ship anywhere — Docker Hub, any registry you like,
a Git repo, or even just a folder sitting in your project.

## Slide 45 — Swap the agent, add the tools

Here's that composability in a single picture, and I love how clean it is.

You pick one agent — it's a radio button, so just one. Claude Code today, maybe
Codex tomorrow. Then you check off any tools you want — GitHub SSH, SSH signing,
your dev environment, as many as you need. And out the other side comes your
sandbox: those tools, that agent, and underneath all of it, always, the microVM
and the proxy.

And this is the key point — you can change either side as much as you like. Swap
the harness. Add tools, drop tools. And the boundary stays exactly, precisely the
same. That's the entire promise of Choice: configure the inside as freely as you
want, and never once have to touch the wall.

## Slide 46 — Running kits from Docker Hub

In the lab, you're going to do exactly this. You'll start a sandbox with one agent
kit. You'll swap the harness while keeping the same project. And then you'll stack
mixins on top for GitHub, for signing, and for the dev environment.

The specific mixin we add is called GitGuardian, and it's a nice one, because it
wires a secret scanner directly into the agent as a hook. So every single write
the agent makes gets scanned for secrets — and the scanner's own API key is
injected by the proxy and never actually enters the box. It's the exact same
credential trick we saw in Contain, just applied to a tool this time instead of
the agent. And the lovely thing you'll see is this: if you ask the agent to
hardcode an AWS key, it refuses — good — but the kit catches a real secret
*regardless* of whether the agent cooperates, because the kit is enforcement, not
hope.

## Slide 47 — You can build your own kits

And you are absolutely not limited to the kits that Docker ships. Kits follow an
open specification — which means you can package up your own agent, or your own
internal tooling, in exactly the same way the official Hub kits are built.

The specification and a set of example kits are at
github.com/docker/sandbox-kit-spec. Building your own kits is genuinely a whole
session in its own right, so I'm not going to go deep here — I just want to plant
the flag firmly. If your team has an internal tool, it can live inside this box,
governed exactly the same way as everything else.

## Slide 48 — Agents talking to an MCP server

So kits put tools *into* the box. There's a second way to give an agent new
capabilities, which is to let it *call out* to external tool servers — MCP servers.

But — and this is the important part — it calls out through one governed gateway,
and never, ever directly to those servers. This is where Choice gets really
powerful, and it's also where governance gets genuinely interesting.

## Slide 49 — Agent with a sandbox

Let me give you a concrete example of an MCP server in action, and it happens to
close the loop on the very first horror story from this morning.

Inside the sandbox — own daemon, own network, host is read-only — the agent has
its full permissions, and now it has one new tool available to it: the Docker
Hardened Images MCP server, which exposes signed tools only. So when you tell it to
"containerise this," before it writes even a single `FROM` line, it queries that
catalog and it picks `dhi.io/node`. And the result? Zero criticals, zero highs,
zero mediums, zero lows. Two hundred and eleven packages, a software bill of
materials attached, signed, and running as non-root.

That's the exact same task that gave us dozens of CVEs on the bare host at the
start of this talk — now completely clean, purely because the right tool was
sitting inside the box.

## Slide 50 — Letting the agent use MCP servers safely

So how does that "safely" part actually work under the hood? The agent never
talks to any of those servers directly.

It talks to one gateway — a single governed endpoint — and that gateway is what
fans out to the local wiki, to GitHub, to Notion, to DuckDuckGo, to whatever
you've registered behind it. Every single tool call the agent makes flows through
that one chokepoint, and the tools are namespaced, so they show up as
mcp-underscore-underscore-mcp-gateway. And that one chokepoint is precisely where
your policy and your audit logging get to live. Many servers behind it, but just
one door in and out.

## Slide 51 — The gateway gatekeeper

There's a deliberate, and I think rather elegant, safety design baked into this.
The entire `sbx mcp` command subtree stays completely hidden until an environment
variable called SBX_MCP_URL is set. And only two values for that variable carry
the full, governed flow.

The first is a local gateway, running on localhost port 8811 — that's wonderful
for learning the mechanics, because you run it, and you control exactly what's
registered. The second is the hosted control plane, at gateway.docker.com — and
that's where organisation policy governs what's actually invocable, with central
audit. That's the real governance story for a company.

And the whole thing is fail-closed by design. If no policy is loaded, the default
is deny-all — not allow-all. The policy is authored up in Docker Hub, it's fetched
at `docker login`, and individual developers cannot override it. So the default
state of this entire system is "nothing is allowed," not "everything is allowed."
That's the right way around.

## Slide 52 — Govern it with an MCP access policy

And for those of you who want to see that this is real, enforceable policy — not
just a nice diagram — here's the actual rule.

It's written in a language called Cedar, and it's authored in Docker's AI
governance console. What you're looking at is a default-deny allow-list over pairs
of server-and-tool. This particular rule permits *only* the read-only DHI tools —
list the repositories, get the CVEs, get the attestations, and so on. And here's
what that buys you in practice: anyone in the organisation is free to *register* a
server, but its tools are only ever *invocable* if the policy permits them — and
that's evaluated right at the gateway, on every single invoke, by the very same
engine that handles your network and filesystem policy. One surface, no way around
it. A developer can run `sbx mcp add` on anything they like; but if the
organisation's policy doesn't permit that server's tools, the calls are simply
denied, and they're audited. You author it once, and it syncs everywhere.

## Slide 53 — One feature: agents in a sandbox, using external tools, safely

Let me pull that whole MCP thread back together, because it's really just one
feature that happens to answer four very practical questions.

What tool-servers are supported? Remote ones, local stdio ones, docker.io
images — and the slide is honest about what isn't supported, too. How do you
register them? With `sbx mcp add`, either one at a time or as a shareable bundle.
How does the sandbox actually connect to them? Either as a locked, static set, or
as a discoverable, dynamic catalog. And how are the credentials managed? The
gateway holds OAuth centrally, so you can authorize, revoke, and audit from one
place.

Agents, inside a sandbox, using external tools, safely. That's the entire scope of
it.

## Slide 54 — Same agent, same prompt, a zero-CVE base

And here is the whole of Choice, captured in one single comparison. I come back to
this slide in my head all the time.

On the left, ungoverned: `claude -p "containerise this"` picks node:20, blind.
Docker Scout comes back with two criticals, twelve highs, twenty mediums, thirteen
lows — across four hundred and thirty-one packages, with no SBOM. On the right,
with the DHI MCP server sitting in the box: the exact same prompt, but now it
queries DHI first, and it lands on dhi.io/node:24-debian13. And Scout comes back
zero, zero, zero, zero — across two hundred and eleven packages, with an SBOM, and
signed.

Read the line at the bottom: the tool in the box changed the outcome — not the
prompt. I didn't write a cleverer prompt. I didn't reach for a smarter model. I
simply put the right tool inside the boundary, and the outcome transformed. That,
right there, is Choice.

## Slide 55 — Agenda checkpoint

Quick checkpoint again. Contain, Control, Choice — all three done. One C left, and
it's the one that turns everything you've seen so far from a clever personal trick
into something an entire team can actually run, reliably, forever.

## Slide 56 — Capacity

The fourth and final C — Capacity. Here's the problem it solves. One developer,
with one beautifully configured sandbox, is a great start. But a boundary that
only exists on *your* laptop isn't really governance — it's a one-off. It's a party
trick. Teams need the same sandbox, everywhere.

## Slide 57 — Scaling up starts with reproducibility

Watch how this breaks down without Capacity, in three steps.

One developer, configuring by hand: it works, on one machine. Fine. A team, each
configuring by hand: now every single setup drifts — different kits, different
policies, slightly different everything. And that is *exactly* where "well, it
works on my machine" is born, and it's exactly where an *ungoverned* sandbox
quietly sneaks back in, because the policy you so carefully set never actually
reached the next person. But a team working from one shared file: now every
sandbox matches, and you can spin up as many of them as you need.

And the fix is the same fix we reach for with everything else that matters in
software — you declare it once, in a file, and you share that file like code.

## Slide 58 — An environment file describes the whole sandbox

That file is called sbxenv.yaml, and it gets committed right into the repository
alongside your code.

It names the agent — which harness the sandbox runs. It names the workspace — the
one folder the agent is allowed to see. It lists the kits — and each kit brings its
tools, its credentials, and its network rules along with it. And it sets the
resources — the CPU and the memory for the box. So the sandbox stops being a pile
of flags that you have to remember to type correctly every time, and it becomes
data — reviewable, diffable, versioned data. You start it with `sbx env run`. One
honest caveat: the format is still experimental, so it may change.

## Slide 59 — Commit it once and the whole team shares one setup

And because it's just a file, it travels exactly like code travels.

You change the file — add a kit, swap the harness, whatever. You open a pull
request — and now that change gets *reviewed*, like any other change to your
system. You merge it, and the repository holds the new definition. And everyone
pulls, and the very next sandbox each person starts matches yours exactly. Update
it once, and every sandbox follows.

Here's the shift that really matters: changing your team's agent security is no
longer a silent little tweak buried in one person's shell history. It becomes a
reviewable event, with a paper trail, that your team can see and roll back and
audit. And one more thing worth calling out — the file holds a *source* for each
secret, like a 1Password reference, which gets resolved on each developer's own
machine. The secret itself never, ever travels in the repo.

## Slide 60 — Cloud Sandboxes run the same setup remotely

And that same file isn't confined to your laptop either.

Locally, the sandbox runs on your machine, bounded by your CPU and your memory.
But in the cloud, the very same environment file runs on Docker's infrastructure —
which means you can start far more sandboxes than one laptop could ever hold. One
agent per pull request. A whole fleet of them running at once, without melting your
machine. Now, the honest caveat: Cloud Sandboxes are in early access right now, and
they're not yet available for organisation use. But the model is the thing to take
away — you write the file once, and you run it anywhere, whether that's one laptop
or a thousand machines in the cloud.

## Slide 61 — Sharing a sandbox with the team

This is the last lab, and in it you get to play the role of the brand-new
teammate.

You clone a repo that already has an environment file in it, and you start a
sandbox — and the kits and the policy are already set up for you; you did nothing
to configure them. Then you change a single line and start it again. And before
anything actually runs, `sbx env plan` shows you exactly what it's going to set up
outside the box — including precisely which secrets it's going to resolve from
*your* host — and it asks for your approval before it touches a single thing.

## Slide 61a — A team of agents, measured

Everything I just described about Capacity — one file, a fleet, the same setup
everywhere — somebody actually ran it, hard, and wrote down every number. A
backend engineer took a real Java service and had three agents build three
features at once, one sandbox each. Three clean merges, full build green. A
hundred and seventy-seven seconds, fifty-three cents. In the cloud it got
*faster* — ninety-seven seconds, a third quicker than his laptop. And at the top
end: a twenty-two-thousand-test suite across a five-sandbox fleet, about half a
dollar a run, against nearly two hours on one machine. That's the moment Capacity
stops being my claim and starts being a measurement. It's an independent
evaluation, and every single number on this slide traces back to a script you can
run yourself.

## Slide 61b — Share the box, don't share the writes

But the same engineer found the edge, and I want to be honest about it, because
being honest about it makes the whole model *stronger*. The thing that makes each
box safe is that it has its own kernel. And the moment two of those boxes try to
share one piece of memory — one file, one database — that same wall turns against
you. Writes just vanish: ninety-plus percent of them, silently, every time he
reran it. Half a million database rows acknowledged as committed, and then simply
not there. And the reason is almost beautiful in how bad it is — a lock held
inside one sandbox is invisible to the next one, so both of them think they're
alone with the data. Now watch where the fix lands. It's the exact fix this whole
talk has been building toward: the coordination has to come from the platform,
not from the agents agreeing to be polite. One writer, everyone else read-only, a
broker that hands out fencing tokens. Same lesson as every other C, just one layer
deeper — the boundary comes from the box, never from good behaviour.

## Slide 62 — All four done

And there it is — all four Cs, every box ticked. Contain, Control, Choice,
Capacity. Let me put them together for you one final time.

## Slide 63 — Recap

If you walked in late, or if you only remember three things from this entire talk,
make it these three.

One: a trusted boundary. A microVM, a network proxy, and credentials that the
agent never actually holds. That's Contain and Control working together. Two: your
choice inside it. Agent kits and mixin kits, for your harness, your tools, and your
endpoints. That's Choice. And three: shared with the team. One environment file,
sitting in the repo — you update it once, and everyone follows. That's Capacity.

And underneath all three, the single idea this whole talk has been built on: the
boundary comes from the box, not from the agent behaving itself. Refusal is a
behaviour — it's a choice the agent makes, and it can fail on a bad day, or with a
poisoned file, or with a different model. A boundary is a wall. That is the entire
difference between *hoping* your agents are safe and *knowing* they are.

## Slide 64 — Thank you

And that's the talk — run fast, without running wild.

The four labs stay open, so please go and finish any you didn't get to; they're
all right there at wadindia.dockerworkshop.com. And please, come find me
afterwards — genuinely, I would love to hear the stories of what your agents have
gotten up to, the good and the terrifying.

Thank you so much for your time.
