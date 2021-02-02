# Variables for local http-challenge

| Variable                            | Required | Default       | Description
|-------------------------------------|----------|---------------|------------
| letsencrypt_local_validation_path   | no       | /var/www/html | Path where the validation-/ hashfiles get created

## Validation

Make sure that the validation-/ hashfile(s) is/are reachable by your configured vhost(s).

## Example

```yaml
- name: create the certificate for example.com
  hosts: localhost
  roles:
    - letsencrypt
  vars:
    domain:
      certificate_name: "example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - example.com
        - domain1.example.com
        - domain2.example.com
    letsencrypt_do_http_challenge: true
    letsencrypt_http_provider: "local"
    letsencrypt_do_dns_challenge: false
    letsencrypt_use_acme_live_directory: false
    account_email: "ssl-admin@example.com"
```
