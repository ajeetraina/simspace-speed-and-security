# Watch the Writes Vanish

Here is the setup, and it's deliberately the most ordinary thing two agents could
do: each one appends notes to a shared `MEMORY.md`. Read the file, add a line,
write it back - the read-modify-write every coding agent does to its own memory.

Two sandboxes, one `host-mount@1`, both writing at once. Each appends **200**
lines, so a correct result is **400** lines. Run it:

```bash
bash tests/race-test.sh
```

Now count what actually survived:

```bash
wc -l MEMORY.md
```

Eleven lines. Out of four hundred. **389 writes gone - silently, no error, no
warning.** And it isn't a fluke: rerun three times and you get 28, 17, 16 out of
400 - a steady 93-97% loss.

Look at what's left in the file - it's not even a clean half, it's shredded:

```bash
cat MEMORY.md
```

The script also ran a SQLite variant (a real database, not a flat file): **228 of
400 inserts failed**, and then the database **couldn't be opened at all**. And the
heaviest case in the source - two sandboxes on one PostgreSQL data directory -
**acknowledged 494,800 rows and then lost 100% of them** on restart, four times
out of four.

> This is the part that should bother you: the agents got **success** back. The
> writes were acknowledged. The data simply isn't there. Silent loss is worse
> than a crash - a crash you'd notice.

So why doesn't the operating system stop this? Agents, SQLite, and PostgreSQL all
use file locks precisely to prevent it. Next section: watch the locks fail.
