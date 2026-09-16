# Support

## Before raising a request

Collect a diagnostics bundle. It contains the configuration, versions, recent logs and
health readings, with passwords, tokens and keys removed.

From the console: **Administration → Download diagnostics**.

From the appliance:

```bash
sudo cloudinfra diagnostics --output /tmp/bundle.tar.gz
```

## What to include

| | |
|---|---|
| The diagnostics bundle | |
| What you expected to happen | |
| What happened instead | |
| The correlation ID | Shown in any error message, and ties the console request to the privileged action behind it |
| The appliance version | **Administration**, or `cloudinfra status` |

## Useful commands

```bash
# Is the appliance running?
systemctl status cloudinfra-manager cloudinfra-agent

# Is the agent reachable?
sudo cloudinfra agent ping

# What has it been doing?
cloudinfra jobs list
sudo journalctl -u cloudinfra-manager -n 100

# What is it permitted to do?
sudo cloudinfra agent actions
```

## Reporting a security issue

Please report suspected vulnerabilities privately rather than in a public issue, so a fix
can be prepared before the detail is public.

Include the version, what you observed, and how to reproduce it.

## A note on findings

If a finding does not tell you what was observed and where it was read from, that is a bug
worth reporting. Every verdict should be traceable to an observation — a security product
that asserts without evidence is asking to be trusted rather than checked.
