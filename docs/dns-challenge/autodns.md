# Variables for AutoDNS dns-challenge

## Examples

### wildcard certificate

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  roles:
    - letsencrypt
  vars:
    domain:
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "*.example.com"
    letsencrypt_do_http_challenge: false
    letsencrypt_do_dns_challenge: true
    letsencrypt_dns_provider: autodns
    letsencrypt_use_acme_live_directory: false
    account_email: "ssl-admin@example.com"
    dns_user: "example_dns"
    dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```

### SAN certificate

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  roles:
    - letsencrypt
  vars:
    domain:
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "example.com"
        - "domain1.example.com"
        - "domain2.example.com"
    letsencrypt_do_http_challenge: false
    letsencrypt_do_dns_challenge: true
    letsencrypt_dns_provider: autodns
    letsencrypt_use_acme_live_directory: false
    account_email: "ssl-admin@example.com"
    dns_user: "example_dns"
    dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```
