# ACME Collection for Ansible

This collection manages ACME certificates.

## Requirements
* Ansible >= 2.9
* Python >= 3 (when you want to use http-challenge via S3)

## Installation

These modules are distributed as [collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).
To install them, run:

```bash
ansible-galaxy collection install t_systems_mms.acme
```

Alternatively put the collection into a `requirements.yml`-file:

```yaml
---
collections:
- t_systems_mms.acme
```

## Usage

Role `acme` for issuing certificates from a certificate authority which implements the ACME protocol.
Please see [documentation](docs/role-acme.md) for variables, usage and further information for all the different providers.

## Testing

We automatically test key-creation and csr-creation, the `local` http-provider and test the challenge with the local pebble provider.

Automatically testing the various dns-challenge providers is hard, because we'd need to maintain accounts and zones on them (and pay for them). We'd also need to store credentials in CI which is a security risk.

Here we list ways to manually test the dns-providers if you have access:

* Hetzner

```
ansible-playbook tests/integration/targets/acme_letsencrypt/dns-challenge-hetzner.yml -e acme_hetzner_auth_token=YOUR_AUTH_TOKEN -e hetzner_domain_name="example.com" -e hetzner_zone="example.com"
```

## License

GPLv3

## Author Information

* Sebastian Gumprich
* Andreas Hering
