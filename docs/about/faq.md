# FAQ

### Does it change anything on its own?

No. Assessments, drift checks and alerts run on a schedule and are read-only. Nothing is
changed without an administrator approving the specific change they were shown.

### Can I use it on a host that is not from the Marketplace image?

The appliance installs on Ubuntu 24.04 LTS. Other Ubuntu releases will warn but install;
other distributions are refused.

### It says my configuration is wrong, but I set it correctly

Check which server block the finding names. On a reverse proxy, a setting in one server
block does not apply to another, and a control passes only when every server block satisfies
it. The finding names which ones do and which do not.

### Why does a control say "not applicable"?

The control has nothing to measure here — a TLS version control on a server that terminates
no TLS. Reporting it as failed would be a finding with no fix; reporting it as passed would
claim a protection that is not in place.

### Why can't the appliance fix everything it finds?

Some controls have no single correct value. The clearest is the NGINX request body size
limit: the right value is whatever your application accepts, and choosing too low silently
breaks uploads. Where the appliance cannot know the right answer, it reports the finding and
leaves the decision to you.

### I applied a fix and the control still fails

Re-run the assessment. The controls page shows the last assessment, not a live reading. A
reassessment is queued automatically after a remediation, and may not have finished.

If it still fails afterwards, open the remediation record — it will say whether the change
was applied or rolled back, and why.

### I locked myself out of the console

If you made the change through the appliance and it was assessed as risky, the connectivity
guard will revert it — wait for the window to pass.

Otherwise check, in order: your Security Group, the host firewall (`sudo ufw status`), and
whether the manager is running (`systemctl status cloudinfra-manager`).

### The banner says the privileged agent is not responding

The console is showing the last readings it collected, not current state. Start the agent:

```bash
sudo systemctl start cloudinfra-agent
sudo journalctl -u cloudinfra-agent -n 50
```

The console recovers on its own once the agent is back; it does not need restarting.

### Are the backups enough to restore my server?

No. They are configuration backups — enough to undo a change the appliance made. Use EBS
snapshots for machine-level recovery.

### Can I add my own controls?

Not in this release. Controls come from modules, and modules are compiled in rather than
loaded at runtime — a runtime plugin mechanism in a product with a root agent is a way to
run arbitrary code as root.

### Does it send anything off the appliance?

Only what you configure: alert emails to the SMTP server you specify. Reports and
diagnostics bundles are generated and stored locally until you download them. There is no
telemetry.
