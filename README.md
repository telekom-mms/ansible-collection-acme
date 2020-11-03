# Let's Encrypt Collection for Ansible
**NOT STABLE - DO NOT USE IN PRODUCTION ENVIRONMENTS**

This role issues Let's Encrypt certificates. Currently DNS-01 and HTTP-01 challenges are supported

Required Ansible version: 2.9

Installation
------------

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

Examples
--------

Please see [README](roles/letsencrypt/README.md) of the role.

License
-------

GPLv3

Author Information
------------------

* Sebastian Gumprich
* Andreas Hering
