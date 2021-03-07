# Variables for hetzner dns-challenge

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| acme_letsencrypt_hetzner_auth_token | yes      |         | Access token for hetzner DNS API

## Usage

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  collections:
    - t_systems_mms.acme
  roles:
    - acme_letsencrypt
  vars:
    acme_letsencrypt_challenge_provider: hetzner
    acme_letsencrypt_use_live_directory: true
    acme_letsencrypt_account_email: "ssl-admin@example.com"
    acme_letsencrypt_hetzner_auth_token: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
    acme_letsencrypt_domain:
      email_address: "ssl-admin@example.com"
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      subject_alt_name:
        - "*.example.com"
```
