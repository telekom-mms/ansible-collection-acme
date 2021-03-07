# Variables for openstack dns-challenge

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| dns_openstack_user_domain           | yes      |         | user domain name like OTC-EU-DE-00000000001000000000
| dns_openstack_auth_url              | yes      |         | authentification api-url
| dns_openstack_project_name          | yes      |         | project name

## Usage

### wildcard certificate

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  roles:
  - acme
  vars:
    acme_do_http_challenge: false
    acme_do_dns_challenge: true
    acme_dns_provider: openstack
    acme_use_live_directory: false
    dns_openstack_user_domain: "OTC-EU-DE-00000000001000000000"
    dns_openstack_auth_url: "https://iam.eu-de.otc.t-systems.com:443/v3"
    dns_openstack_project_name: "eu-de"
    domain:
      acme_certificate_name: "wildcard.example.com"
      acme_dns_zone: "example.com"
      acme_email_address: "ssl-admin@example.com"
      acme_subject_alt_name:
        - "*.example.com"
    account_email: "ssl-admin@example.com"
    acme_dns_user: "example_dns"
    acme_dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```
