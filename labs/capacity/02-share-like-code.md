# Share It Like Code

`sbxenv.yaml` is just a file in your repo, so it travels exactly like your source
does - through version control, review, and history.

## Stage and commit it

```bash
git add sbxenv.yaml
```

```bash
git commit -m "Add sbxenv.yaml - shared team sandbox"
```

The sandbox is now **versioned**. It can be reviewed in a pull request, rolled
back if someone loosens a secret binding, and audited in the history.

## Push it to the team

```bash
git push
```

Every teammate who pulls now has the identical sandbox definition. The governance
you set ships with the repo instead of living in one person's shell history.

> [!NOTE]
> Because the definition is in code, changing the sandbox becomes a **reviewable
> event**, not a silent local tweak.

Next: reproduce it as a brand-new teammate.
