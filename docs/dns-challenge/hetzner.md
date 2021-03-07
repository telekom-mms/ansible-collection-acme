# Variables for hetzner dns-challenge

| Variable               | Required | Default | Description
|------------------------|----------|---------|------------
| dns_hetzner_auth_token | yes      |         | Access token for hetzner DNS API

## Usage

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  roles:
  - acme
  vars:
    acme_challenge_provider: hetzner
    acme_use_live_directory: true
    account_email: "ssl-admin@example.com"
    dns_hetzner_auth_token: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
    domain:
      acme_email_address: "ssl-admin@example.com"
      acme_certificate_name: "wildcard.example.com"
      acme_dns_zone: "example.com"
      acme_subject_alt_name:
        - "*.example.com"
```
