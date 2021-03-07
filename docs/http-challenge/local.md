# Variables for local http-challenge

| Variable                            | Required | Default       | Description
|-------------------------------------|----------|---------------|------------
| acme_local_validation_path   | no       | /var/www/html | Path where the validation-/ hashfiles get created

## Validation

Make sure that the validation-/ hashfile(s) is/are reachable by your configured vhost(s).

## Usage

```yaml
- name: create the certificate for example.com
  hosts: localhost
  roles:
  - acme
  vars:
    domain:
      acme_certificate_name: "example.com"
      acme_dns_zone: "example.com"
      acme_email_address: "ssl-admin@example.com"
      acme_subject_alt_name:
        - example.com
        - domain1.example.com
        - domain2.example.com
    acme_challenge_provider: "local"
    acme_use_live_directory: false
    account_email: "ssl-admin@example.com"
```
