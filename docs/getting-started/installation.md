# Installation

## Choosing an image

CloudInfra Appliance Manager is published as a family of AWS Marketplace AMIs. Each one is
the same appliance — the same console, the same controls, the same remediation and backup
machinery — packaged with a different application already installed and under management.

| Listing | Application managed | Status |
|---|---|---|
| CloudInfra NGINX Appliance Manager | NGINX (reverse proxy, web server) | Available |
| CloudInfra GitLab Appliance Manager | GitLab | Planned - the GitLab module already ships in every image and manages a GitLab you install yourself |
| CloudInfra Redis Appliance Manager | Redis | Planned |

Pick the listing for the application you want to run. If you only want the host hardening
and no managed application, any of them will do: the application module is one part of the
appliance, and the host controls apply on every image.

Everything in this section applies to all of them. Where a page describes something
specific to one application, it says so, and the [Modules](../modules/index.md) section
covers each application on its own terms.

## Launching the appliance

Launch an instance from your chosen listing's AMI.

| | |
|---|---|
| Platform | Ubuntu 24.04 LTS |
| Recommended size | `t3.medium` or larger |
| Disk | 20 GB minimum |
| Console port | TCP **8443** (HTTPS) |
| SSH | TCP 22, if you want shell access |

## Restricting access to the console

!!! danger "Never open port 8443 to the internet"

    The console manages the host it runs on. Anyone who reaches it and signs in can change
    the firewall, rewrite configuration and read logs.

    Restrict TCP 8443 in the instance's **Security Group** to the addresses your
    administrators connect from. The appliance cannot do this for you: a Security Group
    filters traffic before it reaches the instance, so from inside, an open Security Group
    and a closed one look identical.

The appliance itself refuses to write a host firewall rule that opens 8443 to `0.0.0.0/0`,
and warns on the dashboard if it detects one. That is a second line of defence, not a
replacement for the Security Group.

## Reaching the console

```
https://<instance-address>:8443
```

Your browser will warn about the certificate. That is expected: the appliance generates a
self-signed certificate for itself on first boot, because a certificate baked into a shared
image would be identical on every customer's instance — and therefore worthless.

To replace it with a certificate your browsers already trust:

```bash
sudo cloudinfra tls install --cert fullchain.pem --key privkey.pem
```

It checks the pair before replacing anything and puts the old one back if the console does
not return — see
[Replacing the TLS certificate](../reference/ports-and-paths.md#replacing-the-tls-certificate),
which also covers renewal hooks.

## What is installed

| Component | Runs as | Purpose |
|---|---|---|
| `cloudinfra-manager` | `cloudinfra` | The console and the API. Holds no privileges. |
| `cloudinfra-agent` | `root` | Performs privileged actions, from a fixed list. |
| `cloudinfra` | — | Command line client. |
| The managed application | Its own accounts | For the NGINX image, `nginx` running as `root` / `nginx`. |

The split matters: the part exposed to the network cannot change the host directly. It asks
the agent, and the agent will only perform actions that are on a list compiled into it.
There is no "run this command" action at any privilege level.
