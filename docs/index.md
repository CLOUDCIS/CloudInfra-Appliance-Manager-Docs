# CloudInfra Appliance Manager

CloudInfra Appliance Manager assesses a Linux host against a set of security controls,
explains what it found, and — when you approve it — fixes what is wrong without breaking
what is working.

It ships as an AWS Marketplace AMI with NGINX already installed and managed.

## What it does

<div class="grid cards" markdown>

- **Assesses**

    48 controls across SSH, accounts, networking, filesystem, services, updates and the
    application itself. Every verdict names what was observed and where.

- **Remediates**

    Changes are previewed before they are made, backed up before they are applied, and
    validated afterwards. A change that cannot be completed is undone.

- **Watches for drift**

    Tells you when a file it is responsible for has changed since you last agreed it, shows
    what changed, and offers to put it back.

- **Protects your access**

    A firewall change that would disconnect you is refused, or made behind a timer that
    undoes it if you do not confirm you are still connected.

</div>

## What it does not do

It is not a VM backup product. The backups it takes are configuration files — enough to
undo a change it made, not enough to rebuild a machine.

It does not make changes on its own. Nothing is applied without an administrator approving
the specific change they were shown.

It does not open its own management port. The console listens on TCP 8443, and restricting
access to it is your responsibility — see [Installation](getting-started/installation.md).

## Start here

1. [Installation](getting-started/installation.md) — launching the appliance and reaching
   the console
2. [First boot](getting-started/first-boot.md) — what happens the first time it starts, and
   creating the administrator
3. [Quickstart](getting-started/quickstart.md) — your first assessment and your first fix
