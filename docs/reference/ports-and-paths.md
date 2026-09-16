# Ports and paths

## Ports

| Port | Protocol | Purpose |
|---|---|---|
| **8443** | HTTPS | The console and API. Restrict to your administrators. |
| 22 | SSH | Shell access, if you want it |
| 80, 443 | HTTP/HTTPS | Whatever NGINX serves |

The appliance does not open any of these in the host firewall. Reachability is decided by
your Security Group and, if you enable it, the host firewall.

## Paths

### Configuration

| Path | Contents |
|---|---|
| `/etc/cloudinfra/appliance-manager/config.yaml` | Appliance configuration |
| `/etc/cloudinfra/appliance-manager/tls/` | TLS certificate and key, generated on first boot |
| `/etc/cloudinfra/appliance-manager/secret.key` | Secrets key, generated on first boot |

### State

| Path | Contents |
|---|---|
| `/var/lib/cloudinfra/state/appliance.db` | Assessments, backups index, audit log, accounts |
| `/var/lib/cloudinfra/backups/` | Configuration backups |
| `/var/lib/cloudinfra/metrics/` | Recorded telemetry |

### Logs

| Path | Contents |
|---|---|
| `/var/log/cloudinfra/manager.log` | Structured appliance log |
| `/var/log/cloudinfra/agent-journal.jsonl` | Append-only record of privileged actions |

### Binaries

| Path | |
|---|---|
| `/opt/cloudinfra/appliance-manager/bin/` | The three binaries |
| `/usr/local/bin/cloudinfra` | Symlink to the command line client |

## Replacing the TLS certificate

The appliance generates a self-signed certificate for itself on first boot. To use your own:

```bash
sudo cp your.crt /etc/cloudinfra/appliance-manager/tls/server.crt
sudo cp your.key /etc/cloudinfra/appliance-manager/tls/server.key
sudo chown root:cloudinfra /etc/cloudinfra/appliance-manager/tls/server.*
sudo chmod 0644 /etc/cloudinfra/appliance-manager/tls/server.crt
sudo chmod 0640 /etc/cloudinfra/appliance-manager/tls/server.key
sudo systemctl restart cloudinfra-manager
```

The key must be readable by the `cloudinfra` group and not by anyone else. The appliance
will not start with a key it cannot read, and should not be able to start with one everyone
can.

## Changing the listen address

`/etc/cloudinfra/appliance-manager/config.yaml` sets the console's listen address. It binds
`0.0.0.0:8443` by default so the console is reachable from wherever you restrict it to.

If you bind it to a specific address, restart the manager afterwards. The appliance refuses
to start with configuration it cannot parse rather than falling back to defaults — a console
that silently ignored your configuration would be doing something other than what it says.
