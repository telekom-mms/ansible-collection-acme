# Let's Encrypt Collection for Ansible

This role issues Let's Encrypt certificates. Currently DNS-01 and HTTP-01 challenges are supported

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

## Examples

Please see [README](docs/README.md) for variables, usage and further information for the different providers.

## License

GPLv3

## Author Information

* Sebastian Gumprich
* Andreas Hering
