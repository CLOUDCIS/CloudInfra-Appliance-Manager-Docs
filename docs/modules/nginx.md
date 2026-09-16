# NGINX module

Manages the NGINX reverse proxy: its health, configuration, logs, metrics, security controls
and backups.

## How it reads the configuration

NGINX assembles its configuration from includes. On a reverse proxy, essentially everything
worth assessing lives in an included file rather than in `nginx.conf`.

So the appliance asks NGINX what its configuration actually is, rather than reading one file
and guessing. That has two consequences worth knowing:

**Findings name the server block and the file.** A finding reads like

```
server_tokens: "off" in server listening on 8080; not set in server listening on [::]:80
```

rather than telling you something is wrong somewhere.

**It works with either packaging layout.** Ubuntu's NGINX uses `sites-available` and
`sites-enabled`; the packages from nginx.org use `conf.d` only. The appliance handles both
because it reads the assembled configuration, not a fixed set of paths.

## A control passes only when every server block satisfies it

A host serving one hardened site and one unhardened site is not hardened. Where server blocks
disagree, the finding names which ones have the setting and which do not.

## Health

| Check | Answers |
|---|---|
| **Service** | Running, and separately whether it starts at boot |
| **Loaded configuration** | Whether the running process is using the file on disk |

The second exists because NGINX does not reload when its configuration changes. A server can
be up, green in every systemd view, and serving the configuration from before your edit.

## Remediation

The appliance edits the **server block that is failing**, in the file that defines it — not
a global default.

That distinction matters for security headers. NGINX *replaces* inherited `add_header`
directives the moment a block declares one of its own, so writing a header into the `http`
block does nothing at all for a server block with its own headers. A fix written there would
flip the control to passed while the browser received nothing.

Existing directives are corrected in place rather than duplicated, commented-out lines are
left commented out, and a directive inside a `location` is left alone because it belongs to a
scope the finding was not about.

Every change is validated with `nginx -t` before it is applied and again afterwards, with a
backup taken first and a rollback if either check fails.

## Configuration viewer

**Services → NGINX configuration** shows the configuration read-only, with credentials
masked. Patterns are resolved against the host, so you see the server blocks that exist
rather than only `nginx.conf`.

The viewer will only show a file the module publishes. A path that is merely readable by the
appliance is refused.

## Logs

`/var/log/nginx/error.log` and `/var/log/nginx/access.log`, tailed rather than read whole —
an access log's first bytes are its oldest entries.

Credentials in request URLs are masked before the lines leave the host.

## Metrics

Memory and uptime, from systemd's accounting, recorded on the telemetry cycle.

Nothing is derived from the access log: a tail is a sample, not a rate, and
requests-per-second computed from the last two hundred lines would look precise and would
not be.

A stopped application reports **no readings at all** rather than zeroes. A zero in a chart
reads as an idle application when the truth is that it is down.

## Backups

Captures the whole configuration — the main file and the included ones. Restoring
`nginx.conf` without the server blocks it includes would bring back a web server that starts
and serves nothing anybody asked for.
