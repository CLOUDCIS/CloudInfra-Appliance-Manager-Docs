# GitLab module

Manages a GitLab CE instance installed from the omnibus package: its health, configuration,
logs, security controls, drift and backups.

It does not manage GitLab. Users, projects, groups, runners and CI are GitLab's own
administration area, and this module does not duplicate any of it. What it manages is the
appliance around GitLab - the file an administrator would otherwise edit over SSH, the
questions nobody thinks to ask until something is wrong, and the things a Marketplace image
gets wrong by default.

## How it reads the configuration

GitLab does not read `/etc/gitlab/gitlab.rb`. Chef does, when `gitlab-ctl reconfigure` runs,
and it renders the real configuration into `/var/opt/gitlab` - which the next reconfigure
overwrites.

So `gitlab.rb` is the only file worth reading, showing and changing, and every change to it
is inert until the renderer has run. The appliance runs it for you and waits for GitLab to
come back, which is not the same as waiting for the renderer to finish.

Settings that live in GitLab's database rather than in any file - whether sign-up is open,
whether two-factor is enforced, the minimum password length - are read with a fixed query
and **reported, never changed**. Changing them is administering GitLab.

## Health

Two sources, because either can be right while the other is wrong.

| Check | Answers |
|---|---|
| **Service supervisor** | Whether `gitlab-runsvdir` is running at all |
| **GitLab processes** | How many of the fifteen supervised processes are up, and which are not |
| **GitLab readiness** | Whether GitLab can reach its database, Redis, Gitaly and its queues - its own answer, from `/-/readiness` |

The third exists because the first two can be perfectly healthy while GitLab serves nothing.
Measured on a real instance: after stopping and starting Puma, the process list reported all
fifteen running 27 seconds later, and GitLab did not serve a request for a further 43.

## Changing configuration takes about two minutes

A remediation edits `gitlab.rb`, backs it up, runs `gitlab-ctl reconfigure`, waits for
GitLab to serve again, and re-runs the control that prompted it. If any of that fails, the
file is restored and the configuration re-applied.

Measured on a two-core instance:

| | |
|---|---|
| Reconfigure with nothing to change | 17 seconds |
| Reconfigure applying a change | 85 seconds |
| Time after that before GitLab served a request | a further 41 seconds |

The preview says so before you approve it. GitLab is unavailable for roughly two minutes.

## What it checks

Nine controls. The full text of each is in the [control catalogue](../reference/controls.md).

| | |
|---|---|
| **Transport** | Whether GitLab is reached over HTTPS, and whether `external_url` is still the placeholder the package ships |
| **Instance identity** | Whether this instance's encryption keys were generated here, and whether the initial root password file is still present |
| **Accounts** | Whether sign-up is closed or gated by administrator approval, and whether two-factor authentication is enforced |
| **Exposure** | Whether the NGINX status page and the Prometheus endpoints answer to anything but this host |
| **Filesystem** | Whether the secrets file is readable only by root |

### Two of those deserve explaining

**"GitLab's secrets were generated on this instance."** `/etc/gitlab/gitlab-secrets.json`
holds the keys every encrypted column in GitLab's database is encrypted with - 32 of them on
a default install, covering CI/CD variables, personal access tokens and two-factor secrets.
They are created by the first `gitlab-ctl reconfigure`. If that ran while an image was being
built, every instance launched from that image has the same keys, and anyone who can launch
the image can decrypt data belonging to anyone else who did.

The appliance answers this by comparing the file against the life of the instance it is on.
A secrets file older than the instance did not come from the instance.

**"The monitoring endpoints are not reachable from outside"** is answered by looking at what
is listening, not by reading the setting back out of `gitlab.rb`. A default install serves
NGINX's status page on `0.0.0.0:8060` and runs alertmanager on every interface.

## What it does not do

- **It does not change GitLab's application settings.** Sign-up, two-factor and password
  policy are reported. Changing them is Admin Area work, and the appliance does not
  reimplement it.
- **It does not run `gitlab-backup`.** GitLab's own backups are repositories, database,
  uploads and artifacts - gigabytes, and tens of minutes. The appliance backs up the
  configuration it changes, and reports on GitLab's backups rather than pretending to
  replace them.
- **It does not back up `gitlab-secrets.json`.** That would put the keys to every encrypted
  column into a second location on the same instance, in an archive built to be easy to
  restore from - and it would not help, because a restored GitLab still needs its database.
  Keep that file in your own backups, somewhere other than the instance it came from.
- **It does not manage GitLab's bundled NGINX, PostgreSQL or Redis** as though they were the
  standalone products. Omnibus supervises them with runit, and the appliance's NGINX module
  correctly reports NGINX as not installed on a GitLab host.

## Logs

Omnibus writes one log per supervised service under `/var/log/gitlab`, and `journalctl` sees
none of it: the journal records that `gitlab-runsvdir` started and nothing about Puma
refusing a request. All eighteen are readable in the console, labelled by service, with
credentials removed on the way out.

## Configuration view

`gitlab.rb` is shown read-only, redacted. That matters here more than for most files: it is
where SMTP passwords, LDAP bind credentials and object storage keys are written, and the
appliance masks all of them while leaving every ordinary setting readable.
