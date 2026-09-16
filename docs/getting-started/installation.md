# Installation

## Launching the appliance

Launch an instance from the **Cloud Infrastructure Services NGINX Appliance Manager** AMI.

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

To replace it with your own certificate, see [Ports and paths](../reference/ports-and-paths.md).

## What is installed

| Component | Runs as | Purpose |
|---|---|---|
| `cloudinfra-manager` | `cloudinfra` | The console and the API. Holds no privileges. |
| `cloudinfra-agent` | `root` | Performs privileged actions, from a fixed list. |
| `cloudinfra` | — | Command line client. |
| `nginx` | `root` / `nginx` | The reverse proxy the appliance manages. |

The split matters: the part exposed to the network cannot change the host directly. It asks
the agent, and the agent will only perform actions that are on a list compiled into it.
There is no "run this command" action at any privilege level.
