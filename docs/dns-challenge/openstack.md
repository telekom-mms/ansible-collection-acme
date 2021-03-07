# Variables for openstack dns-challenge

| Variable                                | Required | Default | Description
|-----------------------------------------|----------|---------|------------
| acme_letsencrypt_openstack_user_domain  | yes      |         | user domain name like OTC-EU-DE-00000000001000000000
| acme_letsencrypt_openstack_auth_url     | yes      |         | authentification api-url
| acme_letsencrypt_openstack_project_name | yes      |         | project name

## Usage

### wildcard certificate

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  collections:
    - t_systems_mms.acme
  roles:
    - acme_letsencrypt
  vars:
    acme_letsencrypt_challenge_provider: openstack
    acme_letsencrypt_use_live_directory: false
    acme_letsencrypt_openstack_user_domain: "OTC-EU-DE-00000000001000000000"
    acme_letsencrypt_openstack_auth_url: "https://iam.eu-de.otc.t-systems.com:443/v3"
    acme_letsencrypt_openstack_project_name: "eu-de"
    acme_letsencrypt_domain:
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "*.example.com"
    acme_letsencrypt_account_email: "ssl-admin@example.com"
    acme_letsencrypt_dns_user: "example_dns"
    acme_letsencrypt_dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```
