## dns-challenge

## Variables for dns-challenge

| Variable                 | Required | Default   | Description
|--------------------------|----------|-----------|------------
| dns_user                 | yes      |           | username to access the DNS api
| dns_password             | yes      |           | password to access the DNS api
| letsencrypt_dns_provider | yes      |           | which DNS provider should be used: autodns, azure, hetzner(, pebble)

## Example playbooks
### Wildcard certificate

```yaml
- name: create the certificate for domain1
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
    letsencrypt_do_http_challenge: false
    letsencrypt_do_dns_challenge: true
    letsencrypt_use_acme_live_directory: false
    account_email: "ssl-admin@example.com"
    private_key_content: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          ....
    dns_user: "example_dns"
    dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```

More examples can be found in the examples folder of the collection.
