# Variables for local http-challenge

| Variable                              | Required | Default       | Description
|---------------------------------------|----------|---------------|------------
| acme_local_validation_path            | no       | /var/www/html | Path where the validation-/ hashfiles get created
| acme_local_validation_path_file_owner | no       |               | User who owns the validation-/ hash- files and path
| acme_local_validation_path_file_group | no       |               | Group who owns the validation-/ hash- files and path

## Validation

Make sure that the validation-/ hashfile(s) is/are reachable by your configured vhost(s).

## Usage

```yaml
- name: create the certificate for example.com
  hosts: localhost
  collections:
    - telekom_mms.acme
  roles:
    - acme
  vars:
    acme_domain:
      certificate_name: "example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - example.com
        - domain1.example.com
        - domain2.example.com
    acme_challenge_provider: "local"
    acme_use_live_directory: false
    acme_account_email: "ssl-admin@example.com"
```
