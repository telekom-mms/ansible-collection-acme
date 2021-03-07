# Variables for AutoDNS dns-challenge

None

## Usage

### wildcard certificate

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  collections:
    - t_systems_mms.acme
  roles:
    - letsencrypt
  vars:
    domain:
      acme_certificate_name: "wildcard.example.com"
      acme_dns_zone: "example.com"
      acme_email_address: "ssl-admin@example.com"
      acme_subject_alt_name:
        - "*.example.com"
    acme_challenge_provider: autodns
    acme_use_live_directory: false
    account_email: "ssl-admin@example.com"
    acme_dns_user: "example_dns"
    acme_dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```

### SAN certificate

```yaml
- name: create the certificate for example.com
  hosts: localhost
  collections:
    - t_systems_mms.acme
  roles:
    - letsencrypt
  vars:
    domain:
      acme_certificate_name: "wildcard.example.com"
      acme_dns_zone: "example.com"
      acme_email_address: "ssl-admin@example.com"
      acme_subject_alt_name:
        - "example.com"
        - "domain1.example.com"
        - "domain2.example.com"
    acme_challenge_provider: autodns
    acme_use_live_directory: false
    account_email: "ssl-admin@example.com"
    acme_dns_user: "example_dns"
    acme_dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```
