# Variables for hetzner dns-challenge

| Variable                | Required | Default | Description
|-------------------------|----------|---------|------------
| acme_hetzner_auth_token | yes      |         | Access token for hetzner DNS API

## Usage

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  collections:
    - t_systems_mms.acme
  roles:
    - acme
  vars:
    acme_challenge_provider: hetzner
    acme_use_live_directory: true
    acme_account_email: "ssl-admin@example.com"
    acme_hetzner_auth_token: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
    acme_domain:
      email_address: "ssl-admin@example.com"
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      subject_alt_name:
        - "*.example.com"
```
