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

The appliance generates a self-signed certificate for itself on first boot, which is why
your browser warns about it. To use your own:

```bash
sudo cloudinfra tls install --cert fullchain.pem --key privkey.pem
```

The command checks the pair before replacing anything, keeps the certificate that was in
use, restarts the console and waits for it to answer. If the console does not come back,
the previous certificate is restored and the console is brought back on it.

That matters more than it sounds. The console reads the certificate once, at startup, and
exits if it cannot use it — so a key that does not match, or one still encrypted with its
passphrase, leaves the appliance restarting every five seconds with nothing listening on
8443. The only way back would be SSH.

What it refuses, before anything is changed:

| | |
|---|---|
| A key that does not belong to the certificate | The console would not start |
| A key encrypted with a passphrase | Nothing is present at boot to type it |
| An expired certificate | Every browser rejects it |

What it warns about, but installs:

- **A missing chain.** If your issuer sent a separate intermediate file, use the combined
  one — often `fullchain.pem`. A leaf on its own works in some browsers and fails in others.
- **A certificate that does not name this host.** The browser warning you are trying to
  remove will still appear.
- **A certificate expiring within 30 days.**

To see what is being served now, including the fingerprint your browser shows you:

```bash
sudo cloudinfra tls show
```

### Renewals

A renewed certificate is installed the same way. The console must be restarted to serve it,
which `cloudinfra tls install` does — so a renewal hook can simply call it:

```bash
# /etc/letsencrypt/renewal-hooks/deploy/cloudinfra (chmod +x)
#!/bin/sh
cloudinfra tls install \
  --cert "$RENEWED_LINEAGE/fullchain.pem" \
  --key  "$RENEWED_LINEAGE/privkey.pem"
```

The appliance raises an alert when the certificate it is serving is within 30 days of
expiry, and a critical one inside 7 days, so a renewal that silently stopped running is
noticed before it matters.

### Doing it by hand

If you would rather copy the files yourself, the paths are below. Check the pair first —
`openssl x509 -noout -modulus -in cert.pem | openssl md5` and the same for the key — because
nothing else will check it for you.

```bash
sudo cp fullchain.pem /etc/cloudinfra/appliance-manager/tls/server.crt
sudo cp privkey.pem   /etc/cloudinfra/appliance-manager/tls/server.key
sudo chown root:cloudinfra /etc/cloudinfra/appliance-manager/tls/server.*
sudo chmod 0644 /etc/cloudinfra/appliance-manager/tls/server.crt
sudo chmod 0640 /etc/cloudinfra/appliance-manager/tls/server.key
sudo systemctl restart cloudinfra-manager
```

The key must be readable by the `cloudinfra` group and by nobody else. The appliance will
not start with a key it cannot read, and should not be able to start with one everyone can.

## Changing the listen address

`/etc/cloudinfra/appliance-manager/config.yaml` sets the console's listen address. It binds
`0.0.0.0:8443` by default so the console is reachable from wherever you restrict it to.

If you bind it to a specific address, restart the manager afterwards. The appliance refuses
to start with configuration it cannot parse rather than falling back to defaults — a console
that silently ignored your configuration would be doing something other than what it says.
