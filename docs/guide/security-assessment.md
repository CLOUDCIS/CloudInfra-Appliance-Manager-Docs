# Security assessment

An assessment reads the host and compares what it finds against a set of controls. It
changes nothing.

## Running one

From **Security**, select **Run assessment**. Assessments also run on a schedule so the
dashboard does not go stale.

Each run is a point-in-time snapshot. The appliance does not patch new readings into an old
assessment: a snapshot whose rows were measured at different moments produces a score you
cannot reproduce from any single observation.

## What is covered

48 controls across 11 categories:

| Category | Controls | Examples |
|---|---:|---|
| SSH | 11 | Root login, password authentication, attempt limits |
| Networking | 12 | ICMP redirects, router advertisements, forwarding |
| Services | 10 | Unnecessary daemons, time synchronisation |
| Accounts & Authentication | 5 | Password ageing, empty passwords |
| Filesystem | 5 | Permissions and mount options |
| Application Security | 5 | The NGINX module's controls |
| Firewall, Logging, Operating System, Privileges, Updates | — | Distributed across the above |

The full list is in the [control catalogue](../reference/controls.md).

## Reading a verdict

Every verdict is backed by an observation. A control reports:

- **Current value** — what is set now
- **Expected value** — what the control requires
- **Source** — the file or interface it was read from
- **Rationale** — why it matters
- **Recommendation** — what to do

A control that cannot be assessed reports **error**, never **passed**. The two are different
facts, and reporting the first as the second is how a host comes to look secure because
something failed to run.

## Not applicable

Some controls do not apply to some hosts. A TLS version control on a proxy that terminates
no TLS has nothing to measure: reporting it as failed is a finding with no fix, and
reporting it as passed claims a protection that is not in place.

Not-applicable controls do not count against the score.

## Scoring

The score weights by severity — a failing high-severity control costs more than a failing
low one. Not-applicable controls are excluded entirely.

Treat it as a trend, not a target. A score of 100 on a host nobody uses means less than a
score of 80 on one serving traffic, and the individual findings are what you act on.
