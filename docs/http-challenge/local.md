# Variables for local http-challenge

| Variable                               | Required | Default       | Description
|----------------------------------------|----------|---------------|------------
| acme_letsencrypt_local_validation_path | no       | /var/www/html | Path where the validation-/ hashfiles get created

## Validation

Make sure that the validation-/ hashfile(s) is/are reachable by your configured vhost(s).

## Usage

```yaml
- name: create the certificate for example.com
  hosts: localhost
  collections:
    - t_systems_mms.acme
  roles:
    - acme_letsencrypt
  vars:
    acme_letsencrypt_domain:
      certificate_name: "example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - example.com
        - domain1.example.com
        - domain2.example.com
    acme_letsencrypt_challenge_provider: "local"
    acme_letsencrypt_use_live_directory: false
    acme_letsencrypt_account_email: "ssl-admin@example.com"
```
