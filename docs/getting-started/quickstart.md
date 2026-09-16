# Quickstart

This walks through the first thing worth doing: finding out what is wrong, and fixing one
of it.

## 1. Run an assessment

Open **Security** and select **Run assessment**. It takes a few seconds.

You will get a score out of 100 and a list of controls, each in one of five states:

| State | Meaning |
|---|---|
| **Passed** | The appliance checked it and it is as it should be. |
| **Failed** | It checked it and it is not. |
| **Warning** | Not wrong, but worth looking at. |
| **Not applicable** | The control does not apply here — a TLS control on a server offering no TLS. |
| **Error** | It could not check. Never treated as passed. |

A fresh appliance will have failures. That is normal: Ubuntu's defaults are general-purpose,
and several controls describe a hardened posture rather than a broken one.

## 2. Read a finding

Select any failing control. Every finding tells you:

- **What was observed**, and where it was read from — a file path, a `/proc` entry, the
  output of a configuration tool
- **What was expected**, and why it matters
- **What to do about it**

If a finding does not tell you what was observed, that is a bug — please
[report it](../about/support.md).

## 3. Preview a fix

Failing controls that the appliance can fix show **Remediate**. Selecting it shows you a
plan **before anything changes**:

- The exact file that will change, and a diff of the change
- What the change does, in plain language
- Whether it risks your connectivity
- Whether a service will be reloaded

Read the diff. Approving a change you have not looked at is the one habit this design cannot
protect you from.

## 4. Apply it

Select **Apply**. The appliance then, in order: takes a backup, validates the proposed
configuration, writes it, validates what is now on disk, reloads the service, checks it came
back, and re-runs the control.

If any step fails, it puts the file back and tells you why. A change that cannot be
completed does not leave the appliance half-changed.

## 5. Confirm

Re-run the assessment. The control you fixed should now pass, and the score should move.

## Where next

- [Security assessment](../guide/security-assessment.md) — what the controls cover
- [Configuration drift](../guide/drift.md) — noticing when something changes behind your back
- [Firewall](../guide/firewall.md) — changing firewall rules without locking yourself out
