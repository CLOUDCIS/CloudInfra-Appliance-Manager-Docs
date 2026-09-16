# Modules

A module teaches the appliance about one application. It brings its own security controls,
knows where that application keeps its configuration and logs, and supplies the plans that
fix what it finds.

The core ships the parts every Linux host has. It cannot ship knowledge of an application it
has never heard of, so the application brings its own.

## What a module can provide

| Capability | What it means |
|---|---|
| **Detection** | Whether the application is installed here |
| **Health** | Whether it is working, as distinct from running |
| **Security controls** | Checks specific to the application |
| **Remediation** | Plans that fix those checks |
| **Configuration view** | Read-only access to its configuration, redacted |
| **Logs** | Its own log files, where they are not in the journal |
| **Metrics** | Numbers about it, recorded over time |
| **Drift** | Files and settings worth watching for change |
| **Backup** | What to capture so a change can be undone |
| **Service state** | The units it owns |

A module implements what makes sense for its application. Nothing is mandatory beyond
detection.

## Modules in this image

| Module | Capabilities | Controls |
|---|---:|---:|
| [NGINX](nginx.md) | 10 | 5 |
| [Generic Linux](generic-linux.md) | 3 | 43 |

Generic Linux is present on every image. The application module is the one the listing you
launched is named after — NGINX today, with GitLab and Redis to follow. An image carries the
module for its own application, so the console only ever offers you controls for software
that is actually there.

## When an application is not installed

A module whose application is absent reports itself not installed, and its pages disappear
from the console rather than showing empty panels.

Its security controls report **not applicable** and do not count against the score. Its drift
targets report **not installed here** rather than errors — an error nobody can clear teaches
you to ignore the ones that matter.
