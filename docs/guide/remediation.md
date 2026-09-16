# Remediation

Remediation is how the appliance fixes a failing control. Every change is previewed,
approved, backed up and validated.

## The pipeline

When you approve a change, it runs in this order:

1. **Take the change lock** — only one change happens at a time
2. **Re-evaluate the control** — confirm it is still failing
3. **Back up** the files about to change
4. **Verify the backup** is intact and restorable
5. **Generate** the new configuration
6. **Validate** the proposed configuration, before anything is written
7. **Apply** it atomically
8. **Validate** what is now on disk — not what we believe we wrote
9. **Reload** the affected service
10. **Check** the service came back
11. **Re-run** the control
12. **Record** what happened in the audit log

If any step fails, the file is restored from the backup taken at step 3.

## Previewing

The preview shows:

| | |
|---|---|
| **Diff** | The exact lines that change, in the file they change in |
| **Impact** | What the change does, in plain language |
| **Connectivity risk** | Whether it could affect your access |
| **Reload strategy** | Whether a service restarts, reloads, or neither |
| **Rollback available** | Whether this change can be undone |

## Approval is bound to what you saw

An approval carries a hash of the plan you were shown. If the host changed between the
preview and the approval, the change is refused with *"the appliance changed since this plan
was previewed"* rather than applying something you did not review.

This is why remediation cannot be triggered straight from the findings table.

## When a change fails

A failed remediation is recorded as **rolled back**, with the reason, the error, and the
backup it restored from. The file is byte-identical to how it started.

!!! note "A rolled-back change is a completed job"

    In the jobs view a rolled-back remediation shows as completed, because the pipeline did
    what it promised: it left the appliance as it found it. The remediation record is the
    authoritative outcome — it reads **rolled back** and carries the reason.

## Controls that cannot be remediated

Some failing controls have no **Remediate** button. That is deliberate, not unfinished.

The clearest example is the NGINX request body size limit. Every other control has one
correct value; this one does not. The right limit is whatever the application behind the
proxy accepts, which the appliance cannot know — and setting it too low silently breaks
every upload larger than it, with nothing failing until a user tries.

Where the appliance cannot know the right answer, it reports the finding and leaves the
decision to you.
