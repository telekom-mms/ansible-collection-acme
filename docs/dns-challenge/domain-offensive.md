# Variables for Domain Offensive dns-challenge

| Variable                | Required | Default | Description
|-------------------------|----------|---------|------------
| acme_dns_password       | yes      |         | Let`s Encrypt API-Token, you can get here: [do.de](https://my.do.de/settings/domains/general)

## Usage

### wildcard certificate

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  collections:
    - telekom_mms.acme
  roles:
    - acme
  vars:
    acme_domain:
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "*.example.com"
    acme_challenge_provider: domain-offensive
    acme_use_live_directory: false
    acme_account_email: "ssl-admin@example.com"
    acme_dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```

### SAN certificate

```yaml
- name: create the certificate for example.com
  hosts: localhost
  collections:
    - telekom_mms.acme
  roles:
    - acme
  vars:
    acme_domain:
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "example.com"
        - "domain1.example.com"
        - "domain2.example.com"
    acme_challenge_provider: domain-offensive
    acme_use_live_directory: false
    acme_account_email: "ssl-admin@example.com"
    acme_dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```
