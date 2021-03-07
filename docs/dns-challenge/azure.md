# Variables for azure dns-challenge

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| azure_resource_group                | yes      |         | Azure Resource Group for acme_dns_zone_name
| acme_subject_alt_name: top_level:        | no       |         | list of top-level domains
| acme_subject_alt_name: second_level:     | no       |         | list of second_level domains

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
    acme_dns_provider: azure
    acme_use_live_directory: true
    account_email: "ssl-admin@example.com"
    azure_resource_group: "azure_resource_group"
    convert_cert_to: pfx
    domain:
      acme_email_address: "ssl-admin@example.com"
      acme_certificate_name: "wildcard.example.com"
      acme_dns_zone: "example.com"
      acme_subject_alt_name:
        top_level:
          - "*.example.com"
```

### SAN certificate

```yaml
- name: create the certificate for example.com
  hosts: localhost
  roles:
  - acme
  vars:
    acme_do_http_challenge: false
    acme_do_dns_challenge: true
    acme_dns_provider: azure
    acme_use_live_directory: true
    account_email: "ssl-admin@example.com"
    azure_resource_group: "azure_resource_group"
    convert_cert_to: pfx
    domain:
      acme_certificate_name: "example.com"
      acme_dns_zone: "example.com"
      acme_email_address: "ssl-admin@example.com"
      acme_subject_alt_name:
        top_level:
          - example.com
          - domain1.example.com
          - domain2.example.com
        second_level:
          - domain1.example.co.uk"
```
