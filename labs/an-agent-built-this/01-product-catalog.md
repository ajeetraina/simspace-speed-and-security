# Meet the Product Catalog

```text no-run-button
   Client ── REST / JSON ──▶ ┌──────────────────────────────────────────┐
                             │        Product Catalog API               │
                             │   Node.js + Express  ·  source only,      │
                             │           no Dockerfile                  │
                             └──────────────────────────────────────────┘
                                                │
        ┌──────────────┬───────────────┬───────┴───────┬───────────────┐
        ▼              ▼               ▼               ▼               ▼
   PostgreSQL       AWS S3          Kafka           Stripe        Inventory
   catalog DB    images/assets    event stream     payments      service
                                                    (LIVE)        (internal)
   ───────────────────── secrets, plaintext in .env ─────────────────────
   DB password     AWS keys           —          Stripe key     internal API key
```

*A real service: a Node.js + Express API backed by Postgres, S3, and Kafka, with
live Stripe payments and an internal inventory service. It ships source only - no
Dockerfile - which is exactly what teams now hand to an agent. Notice how every
dependency below the API maps to a credential sitting in `.env`.*

## Step 1 - Clone it

```bash
git clone https://github.com/ajeetraina/product-catalog-demo-showcase
```

## Step 2 - Note: no Dockerfile

```bash
tree product-catalog-demo-showcase
```

Source only. That's the agent's task in the next section.

## Step 3 - Note the `.env` sitting in the repo

```bash
cat product-catalog-demo-showcase/.env
```

Database password, **live AWS keys**, a **Stripe live key**, an internal API key
- plaintext, next to the code. The "private data" leg of the trifecta. Hold that
thought.

Next: **An Agent Containerises It**.
