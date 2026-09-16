# Alerts

Alerts tell you when the appliance notices something, without you having to be looking at it.

## What raises one

| | |
|---|---|
| A security control starts failing | Critical controls raise a critical alert |
| A remediation fails or is rolled back | |
| Configuration drift is detected | |
| A watched service stops or fails | |
| Disk, memory or CPU crosses a threshold | |
| A backup or restore fails | |
| Security updates become available | |

Thresholds use hysteresis: an alert clears at a lower level than it fires at, so a value
sitting on the boundary does not produce a stream of identical alerts.

![Alerts](../assets/screenshots/alerts.png)
/// caption
What the appliance has noticed, and who it told.
///

## Managing them

**Acknowledge** records that somebody has seen it. **Resolve** closes it. Both are recorded
in the audit log with who did it.

Repeated occurrences of the same condition are deduplicated rather than listed again.

## Email delivery

**Alerts → Channels** configures SMTP.

| Field | Notes |
|---|---|
| Host, port | Your mail server |
| Username, password | Optional |
| From, To | Addresses |
| StartTLS | Recommended |
| Allow insecure | Only for a trusted relay on localhost |

**Send test message** delivers immediately so you find out now rather than during an
incident.

The stored password is never returned to the console. Once set, the interface shows that a
password exists, not what it is.

!!! note "Credentials in alert emails"

    Alert messages are redacted like everything else, and the appliance's own SMTP password
    never appears in one. But an alert may quote a configuration line, so treat the
    destination mailbox as somewhere appliance detail ends up.
