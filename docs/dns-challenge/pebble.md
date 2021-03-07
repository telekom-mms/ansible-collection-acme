# Variables for pebble dns-challenge

This provider gets used in our integration tests for the DNS challenge.
**This provider should not be used in other environments than for testing!
The certificates are not trusted**.

We start a Pebble and challtestsrv to validate a certificate for testing the role.
This is also done for the provider of the local http-challenge.

## Usage

```yaml
- name: create the certificate for example.com with dns-challenge provider "pebble"
  hosts: localhost
  collections:
    - t_systems_mms.acme
  roles:
    - acme_letsencrypt
  vars:
    acme_letsencrypt_domain:
      certificate_name: "dns-pebble.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "example.com"
    acme_letsencrypt_challenge_provider: "pebble"
    acme_letsencrypt_use_live_directory: false
    acme_letsencrypt_account_email: "ssl-admin@example.com"
    acme_letsencrypt_staging_directory: "https://localhost:14000/dir"
    acme_letsencrypt_validate_certs: false
  post_tasks:
    - name: validate certs
      community.crypto.x509_certificate_info:
        path: "{{ acme_letsencrypt_cert_path }}"
      register: result

    - debug:
        msg: "{{ result }}"

    - assert:
        that:
          - result.subject.commonName == "example.com"
          - "'DNS:example.com' in result.subject_alt_name"
          - "'Pebble Intermediate CA' in result.issuer.commonName"
```
