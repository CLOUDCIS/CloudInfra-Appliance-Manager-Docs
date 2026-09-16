# Architecture

## Privilege separation

The appliance is two processes.

```
  Browser ──HTTPS:8443──▶  cloudinfra-manager        (user: cloudinfra, no privileges)
                                   │
                            Unix socket, peer-verified
                                   ▼
                           cloudinfra-agent          (user: root)
                                   │
                                   ▼
                              the host
```

The part exposed to the network holds no privileges. It cannot write a configuration file,
restart a service or change a firewall rule. It asks the agent.

The agent accepts only actions from a list compiled into it, each with a typed request, a
validator and an audit record. **There is no "run this command" action at any privilege
level.** Adding one would make every other control in this design decorative.

The agent verifies the identity of whatever connects to its socket at the operating system
level, so a process running as another user cannot ask it for anything.

## What the agent will not do

Beyond the action list, the agent enforces allowlists on the actions themselves:

| Allowlist | Governs |
|---|---|
| Readable paths | Which files can be read |
| Writable paths | Which files can be written — much narrower |
| Statable paths | Which files can be inspected without reading |
| Tailable paths | Which log files can be tailed |
| Listable paths | Which directories can be listed |
| Units | Which services can be controlled |
| Validators | Which external checkers can be run, and with what arguments |

These are separate on purpose. Being able to read a file does not imply being able to write
it; being able to tail a log does not imply being able to read it whole.

A module extends them by declaring what it needs, and the declarations are checked: a module
cannot grant itself access to `/etc/shadow`, and cannot name an interpreter as a validator.

## Modules

A module is compiled in, not loaded at runtime. There is no plugin directory, because a
runtime plugin mechanism in a product with a root agent is a way to run arbitrary code as
root.

Both processes derive their allowlists from the same module descriptors, so the manager and
the agent cannot disagree about what a module may see.

## Safety properties

**Nothing is applied without a preview.** An approval carries a hash of the plan you were
shown, and is refused if the host changed since.

**Nothing is written without a backup.** The agent refuses a write that does not reference an
intact, verified backup covering the file.

**A change that cannot be completed is undone.** The pipeline restores from the backup it
took, and records why.

**A change that could disconnect you is made behind a timer.** If you do not confirm you are
still connected, it is reverted without you.

**Secrets are removed on the host.** Redaction happens before data crosses the privilege
boundary, not before it is displayed.

## Where the record lives

The appliance's database holds assessments, remediations and the audit log. The agent
separately keeps an append-only journal of every privileged action it performed, written
independently — so a compromised console cannot erase the evidence of what it asked for.
