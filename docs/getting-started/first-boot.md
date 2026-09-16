# First boot

The image ships **unprovisioned**. It contains no certificate, no encryption key, no
database and no administrator account.

That is deliberate. Anything secret created while the image was built would be identical on
every instance launched from it, and a key that every customer shares is not a key. So the
appliance creates its own the first time it starts.

## What happens

Within a few seconds of the first boot:

```
cloudinfra-firstboot.service: generated the secrets key
cloudinfra-firstboot.service: generated a self-signed certificate for ip-10-0-1-42
```

| Created | Where | Unique to |
|---|---|---|
| Secrets key | `/etc/cloudinfra/appliance-manager/secret.key` | this instance |
| TLS certificate and key | `/etc/cloudinfra/appliance-manager/tls/` | this instance |
| Database | `/var/lib/cloudinfra/state/appliance.db` | this instance |

The certificate's common name is the instance's own hostname, and it is valid for two years.

You can confirm it happened on your instance:

```bash
sudo journalctl -u cloudinfra-firstboot -b
sudo openssl x509 -in /etc/cloudinfra/appliance-manager/tls/server.crt -noout -subject -dates
```

## Creating the administrator

Browse to `https://<instance-address>:8443`. Because no account exists yet, the appliance
shows a setup form rather than a sign-in page.

Choose a username and a password. There is no default password to change, and no account
exists until you create one — an appliance that shipped with a known password would be
reachable by anyone who read the documentation.

!!! note "Setup happens once"

    Once an administrator exists, the setup form is closed permanently. A second attempt is
    refused, so an image that has been configured cannot be taken over by somebody
    re-running setup.

After creating the account you are signed in automatically.

## If you lose the administrator password

Another administrator can reset it from **Administration → Users**.

!!! danger "Create a second administrator account"

    If the appliance has only one administrator and that password is lost, **there is no
    recovery path**. Setup cannot be re-run — it is closed permanently once an account
    exists — and there is no command line reset.

    Create a second administrator before you need one, and keep the credentials somewhere
    your team can reach them.
