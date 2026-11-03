# Give Each Role Work

You drive an agent in a box with `sbx exec <sandbox> <command>`. To run the agent
headless - no interactive session - give it `claude -p "<task>"`. Hand the
developer the task:

```bash
sbx exec developer claude -p "Implement CAT-12 from backlog/CAT-12-category-filter.md"
```

The developer edits `product-list.js`, runs the tests, and commits - all inside
its own microVM, against the mounted project. Because the workspace is shared, the
reviewer's box can now see that commit. Check from the **reviewer**:

```bash
sbx exec reviewer git log --oneline -2
```

```text no-run-button
a1b2c3d (developer) CAT-12: add category filter to the product list
9f3c1a2 Add sbxenv.yaml - shared team sandbox
```

No handoff tool, no message bus - the reviewer sees the work because both boxes
mount the same project. Have the reviewer run the tests in its own box:

```bash
sbx exec reviewer npm test
```

Then let the reviewer actually review the change against the task and the policy:

```bash
sbx exec reviewer claude -p "Review the latest commit against CAT-12 and our coding policy"
```

Read what it checks - not just "does it run", but the acceptance criteria *and*
the boundary from the earlier Cs:

```text no-run-button
  ✓ category filter renders          (acceptance)
  ✓ filter narrows to one category   (acceptance)
  ✓ existing tests pass              (acceptance)
  ✓ no secrets, no new registry      (policy - the boundary holds)

  ⚠ product question, not a bug:
    what should the list show for products with NO category set?
```

The reviewer found something the task never decided - and it **does not guess**.

> [!NOTE]
> A separate reviewer box - ideally a different model - is what catches this. One
> agent reviewing its own work tends to rationalise its choices. Two isolated
> roles over the same project create an honest second opinion.

Next: the one decision that's yours to make.
