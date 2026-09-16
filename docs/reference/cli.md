# Command line

The `cloudinfra` command is installed on the appliance for diagnosis and first-boot
provisioning. It is not a second way to administer the appliance — day-to-day work happens
in the console, where actions are authenticated, authorised and audited.

## Commands

### `cloudinfra status`

Appliance version, agent reachability and service state.

```bash
cloudinfra status
```

### `cloudinfra agent ping`

Checks the privileged agent is reachable over its socket. The first thing to run when the
console reports that the agent is not responding.

```bash
sudo cloudinfra agent ping
```

### `cloudinfra agent actions`

Lists every privileged action this build permits. There is no "run a command" action at any
privilege level, and this is how you confirm that for yourself.

```bash
sudo cloudinfra agent actions
```

### `cloudinfra jobs list`

Recent background jobs — assessments, remediations, backups, drift checks — with their
states.

```bash
cloudinfra jobs list
```

### `cloudinfra diagnostics`

Collects a support bundle. Passwords, tokens and keys are removed.

```bash
sudo cloudinfra diagnostics --output /tmp/bundle.tar.gz
```

### `cloudinfra provision`

Generates first-boot TLS material and the secrets key. Run automatically by
`cloudinfra-firstboot.service` on the first boot; you should not need it.

### `cloudinfra users list`

The accounts on this appliance, their roles and whether they are locked out. Reads the
appliance's database directly, so it works when the console does not.

```bash
sudo cloudinfra users list
```

### `cloudinfra users reset-password`

Sets a new password for an account, for recovering an appliance whose only administrator
password has been lost.

```bash
sudo cloudinfra users reset-password --username admin
```

The password is read from the terminal — never from an argument, which would put it in your
shell history and in the process list where any user on the host can read it. The reset
clears any lockout, revokes the account's sessions, and is written to the audit log as
`users.password_reset.local`.

Requires a shell on the appliance and `sudo`. There is deliberately no way to do this over
the network.

### `cloudinfra tls show`

The certificate the console is serving: subject, names, validity, and the SHA-256
fingerprint your browser shows you.

```bash
sudo cloudinfra tls show
```

### `cloudinfra tls install`

Replaces the console's certificate, safely.

```bash
sudo cloudinfra tls install --cert fullchain.pem --key privkey.pem
```

Checks the pair, keeps the one in use, restarts the console, and waits for it to answer —
restoring the previous certificate if it does not. `--no-restart` installs without touching
the running console.

See [Replacing the TLS certificate](ports-and-paths.md#replacing-the-tls-certificate).

## Service management

The appliance's own services are ordinary systemd units:

```bash
systemctl status cloudinfra-manager
systemctl status cloudinfra-agent
sudo systemctl restart cloudinfra-agent

sudo journalctl -u cloudinfra-manager -n 100
sudo journalctl -u cloudinfra-agent -n 100
```

The manager keeps its own structured log at `/var/log/cloudinfra/manager.log`, and the agent
keeps an append-only journal at `/var/log/cloudinfra/agent-journal.jsonl` — written
independently of the appliance's database, so a compromised console cannot erase the record
of what it asked for.
