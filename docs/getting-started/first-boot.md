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

!!! danger "Restrict port 8443 before the instance boots"

    Between the first boot and the moment you create the administrator, the appliance shows
    a setup form to whoever reaches it. It has no way to tell you from anyone else: no
    account exists yet, so there is nothing to authenticate against.

    If you launch with port 8443 open to the internet, a stranger can reach the form before
    you do and become the administrator of your appliance. Set the Security Group to your
    own administrative addresses **when you launch**, not afterwards.

    Once you have created the account, the window is closed for good.

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

If no other administrator exists, you can reset the password from a shell on the appliance:

```bash
sudo cloudinfra users list
sudo cloudinfra users reset-password --username admin
```

The new password is typed at the terminal, so it does not reach your shell history or the
process list. Resetting also clears any lockout and signs the account out everywhere.

!!! warning "Keep a second administrator anyway"

    The command line reset needs SSH access to the instance and `sudo`. If you lose both
    the console password and shell access, nothing else will get you in — setup cannot be
    re-run once an account exists.

    Create a second administrator before you need one, and keep the credentials somewhere
    your team can reach them.
