Speed or Security? Why Not Both for Your Coding Agents: AI Coding Agent Horror Stories and the microVM That Saves You

If you run coding agents all day, you already know the feeling. Claude Code, Codex, Gemini CLI save you real hours, and then every so often one of them does something that makes your stomach drop. It deletes the wrong folder. It runs a curl nobody read closely enough. It reaches for a credential you forgot was sitting in your environment.
Last year made it worse. System prompts leaked, MCP file swaps turned into remote code execution, and tool-poisoning hit Anthropic, OpenAI, Zapier, and Cursor one after another. None of it was exotic. It all came down to the same thing: we hand these agents a lot of trust, and something on the other end keeps finding ways to abuse it. So most developers end up stuck in the same tradeoff. Give the agent freedom and get speed but no safety, or lock it down with permission popups and lose the speed you came for.

This talk is about getting out of that tradeoff. It starts with the horror stories, the real ones, and then shows what actually helps. Not permission dialogs, because most of us click through those in about a second when we are moving fast. Not "please be careful" in a system prompt, because that is just text. What holds up is a real boundary. You will see Docker Sandboxes, where each agent runs inside its own microVM with its own kernel, and your SSH keys, AWS creds, and Docker socket are just not in there to steal.
We will go through it live. Credential injection through a proxy, network rules that block exfiltration before it starts, branch mode, agents running in parallel. Then the part worth staying for: Sandbox Kits, where you package tools like VS Code, Firecrawl, or Box into something your whole team can run the same safe way, instead of everyone improvising on their own machine.

You will walk out knowing how to let your agents run fast, without letting them run wild.

## Implementation

The WeAreDevelopers India Conference slides starts with tradtional vs agentic workflow. Typically, when you ask agent to containerise this app, it might download pakcages randonly from container registry and download packages that are vulnerable. The first lab would be showcasing this: 
- Clone the repo https://github.com/ajeetraina/product-catalog-demo-showcase
- Ask Agent to containerise this app
- Let it download packages that are vulnerable
- Use Scout to check abd verify the vulnerabilities

- 
