# Variables for openstack dns-challenge

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| dns_openstack_user_domain           | yes      |         | user domain name like OTC-EU-DE-00000000001000000000
| dns_openstack_auth_url              | yes      |         | authentification api-url
| dns_openstack_project_name          | yes      |         | project name

## Examples

### wildcard certificate

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  roles:
    - letsencrypt
  vars:
    letsencrypt_do_http_challenge: false
    letsencrypt_do_dns_challenge: true
    letsencrypt_dns_provider: openstack
    letsencrypt_use_acme_live_directory: false
    dns_openstack_user_domain: "OTC-EU-DE-00000000001000000000"
    dns_openstack_auth_url: "https://iam.eu-de.otc.t-systems.com:443/v3"
    dns_openstack_project_name: "eu-de"
    domain:
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "*.example.com"
    account_email: "ssl-admin@example.com"
    dns_user: "example_dns"
    dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```
