# Variables for azure dns-challenge

| Variable                        | Required | Default | Description
|---------------------------------|----------|---------|------------
| acme_azure_resource_group       | yes      |         | Azure Resource Group for zone_name
| subject_alt_name: top_level:    | no       |         | list of top-level domains
| subject_alt_name: second_level: | no       |         | list of second_level domains

## Usage

### wildcard certificate

```yaml
- name: create the certificate for *.example.com
  hosts: localhost
  collections:
    - t_systems_mms.acme
  roles:
    - acme
  vars:
    acme_challenge_provider: azure
    acme_use_live_directory: true
    acme_account_email: "ssl-admin@example.com"
    acme_azure_resource_group: "azure_resource_group"
    acme_convert_cert_to: pfx
    acme_domain:
      email_address: "ssl-admin@example.com"
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      subject_alt_name:
        top_level:
          - "*.example.com"
```

### SAN certificate

```yaml
- name: create the certificate for example.com
  hosts: localhost
  collections:
    - t_systems_mms.acme
  roles:
    - acme
  vars:
    acme_challenge_provider: azure
    acme_use_live_directory: true
    acme_account_email: "ssl-admin@example.com"
    acme_azure_resource_group: "azure_resource_group"
    acme_convert_cert_to: pfx
    acme_domain:
      certificate_name: "example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        top_level:
          - example.com
          - domain1.example.com
          - domain2.example.com
        second_level:
          - domain1.example.co.uk"
```
