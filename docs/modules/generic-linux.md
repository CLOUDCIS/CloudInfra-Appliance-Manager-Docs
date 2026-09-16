# Generic Linux module

The baseline. It manages the operating system rather than an application, and is present on
every appliance.

It reports itself installed unconditionally: the operating system is always there.

## What it covers

43 controls across SSH, accounts, networking, filesystem, services, logging, privileges and
updates. See the [control catalogue](../reference/controls.md).

## Remediation

Most of its controls can be fixed by the appliance, using two approaches:

**Kernel parameters** are written to a drop-in under `/etc/sysctl.d/`, never to your
`/etc/sysctl.conf`. Your own file is watched for drift and read for assessment, and the
appliance does not rewrite it.

**SSH configuration** is edited in `/etc/ssh/sshd_config`, with `sshd -t` validating the
result before the daemon is reloaded.

!!! warning "SSH changes carry connectivity risk"

    A change to SSH configuration is assessed for connectivity risk like a firewall change,
    and the preview says so. Read it before approving.

## Files it watches

| Target | File |
|---|---|
| SSH daemon configuration | `/etc/ssh/sshd_config` |
| Login defaults | `/etc/login.defs` |
| Kernel parameters | `/etc/sysctl.conf` |
| Filesystem table | `/etc/fstab` |

`/etc/fstab` and `/etc/sysctl.conf` are watched and backed up but **never written**. A stale
fstab restored onto a running machine can leave one that will not boot. The appliance keeps
a copy for the record and declines to put it back.
