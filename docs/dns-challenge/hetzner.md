# Variables for hetzner dns-challenge

| Variable               | Required | Default | Description
|------------------------|----------|---------|------------
| dns_hetzner_auth_token | yes      |         | Access token for hetzner DNS API

## Usage

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  roles:
    - letsencrypt
  vars:
    letsencrypt_do_http_challenge: false
    letsencrypt_do_dns_challenge: true
    letsencrypt_dns_provider: hetzner
    letsencrypt_use_acme_live_directory: true
    account_email: "ssl-admin@example.com"
    dns_hetzner_auth_token: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
    domain:
      email_address: "ssl-admin@example.com"
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      subject_alt_name:
        - "*.example.com"
```
