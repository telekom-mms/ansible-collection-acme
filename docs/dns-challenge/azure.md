# Variables for azure dns-challenge

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| azure_resource_group                | no       |         | Azure Resource Group for zone_name
| subject_alt_name: top_level:        | no       |         | list of top-level domains
| subject_alt_name: second_level:     | no       |         | list of second_level domains

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
    letsencrypt_dns_provider: azure
    letsencrypt_use_acme_live_directory: true
    account_email: "ssl-admin@example.com"
    azure_resource_group: "azure_resource_group"
    convert_cert_to: pfx
    domain:
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
  roles:
    - letsencrypt
  vars:
    letsencrypt_do_http_challenge: false
    letsencrypt_do_dns_challenge: true
    letsencrypt_dns_provider: azure
    letsencrypt_use_acme_live_directory: true
    account_email: "ssl-admin@example.com"
    azure_resource_group: "azure_resource_group"
    convert_cert_to: pfx
    domain:
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
