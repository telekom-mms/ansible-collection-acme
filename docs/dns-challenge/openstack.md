# Variables for openstack dns-challenge

| Variable                    | Required | Default | Description
|-----------------------------|----------|---------|------------
| acme_openstack_user_domain  | yes      |         | user domain name like OTC-EU-DE-00000000001000000000
| acme_openstack_auth_url     | yes      |         | authentication api-url
| acme_openstack_project_name | yes      |         | project name

## Usage

### wildcard certificate

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  collections:
    - telekom_mms.acme
  roles:
    - acme
  vars:
    acme_challenge_provider: openstack
    acme_use_live_directory: false
    acme_openstack_user_domain: "OTC-EU-DE-00000000001000000000"
    acme_openstack_auth_url: "https://iam.eu-de.otc.t-systems.com:443/v3"
    acme_openstack_project_name: "eu-de"
    acme_domain:
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "*.example.com"
    acme_account_email: "ssl-admin@example.com"
    acme_dns_user: "example_dns"
    acme_dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```
