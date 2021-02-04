# Let's Encrypt Collection for Ansible

This collection manages Let's Encrypt certificates.

Required Ansible version: 2.9

## Installation

These modules are distributed as [collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).
To install them, run:

```bash
ansible-galaxy collection install t_systems_mms.letsencrypt
```

Alternatively put the collection into a `requirements.yml`-file:

```yaml
---
collections:
- t_systems_mms.letsencrypt
```

## Usage

Role `letsencrypt` for issuing certificates.
Please see [documentation](docs/role-letsencrypt.md) for variables, usage and further information for all the different providers.

## License

GPLv3

## Author Information

* Sebastian Gumprich
* Andreas Hering
