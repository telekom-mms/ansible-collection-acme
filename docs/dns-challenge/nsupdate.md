# Variables for nsupdate dns-challenge

| Variable                          | Required | Default      | Description                                                                                                                         |
|-----------------------------------|----------|--------------|-------------------------------------------------------------------------------------------------------------------------------------|
|                                   |          |              |                                                                                                                                     |
| acme_nsupdate_server              | yes      |              | The IPv4/IPv6 address of the DNS server where nsupdate manages the _acme-challenge TXT records. (can also be a DNS name, see below) |
| acme_nsupdate_dns_key:            | yes      |              | The acme_nsupdate_dns_key dictionary mirrors the settings of a bind DNS keyfile.                                                    |
| acme_nsupdate_dns_key: name:      | no       | nsupdate_key | Name of the                                                                                                                         |
| acme_nsupdate_dns_key: algorithm: | no       | hmac-sha512  | Hash algo of the key (i.e. hmac-sha512, hmac-sha256)                                                                                |
| acme_nsupdate_dns_key: secret:    | yes      |              | The key                                                                                                                             |
| acme_nsupdate_replication_delay   | no       | 2            | Wait time after the TXT record is issued, before the certificate is fetched via ACME                                                |
| acme_nsupdate_ttl                 | no       | 60           | The TTL for the TXT record                                                                                                          |

## Usage

### wildcard certificate

```yaml
- name: create the certificate for *.example.org
  hosts: localhost
  collections:
    - telekom_mms.acme
  roles:
    - acme
  vars:
    acme_domain:
      certificate_name: "wildcard.example.org"
      zone: "example.org"
      email_address: "ssl-admin@example.org"
      subject_alt_name:
        - "*.example.org"
    acme_challenge_provider: nsupdate
    acme_use_live_directory: false
    acme_account_email: "ssl-admin@example.org"
    acme_nsupdate_server: "{{ lookup('community.general.dig', 'primary.nsforexample.org', qtype='A') }}"
    acme_nsupdate_dns_key:
          name: 'nsupdate_key'
          algorithm: hmac-sha512
          secret: ""
```

### SAN certificate

```yaml
- name: create the certificate for example.org
  hosts: localhost
  collections:
    - telekom_mms.acme
  roles:
    - acme
  vars:
    acme_domain:
      certificate_name: "test.example.org"
      zone: "example.org"
      email_address: "ssl-admin@example.org"
      subject_alt_name:
        - "test.example.org"
        - "domain1.example.org"
        - "domain2.example.org"
    acme_challenge_provider: nsupdate
    acme_use_live_directory: false
    acme_account_email: "ssl-admin@example.org"
    acme_nsupdate_server: "{{ lookup('community.general.dig', 'primary.nsforexample.org', qtype='A') }}"
    acme_nsupdate_dns_key:
        name: 'nsupdate_key'
        algorithm: hmac-sha512
        secret: ""
```

### acme_nsupdate_server
The acme_nsupdate_server MUST be a IPv4/IPv6 address (limitation of the nsupdate ansible module). To work with a DNS 
name, you can use the dig lookup: 
```
acme_nsupdate_server: "{{ lookup('community.general.dig', 'primary.nsforexample.org', qtype='A') }}"
```

### acme_domain.zone
In some cases your DNS server may not be authoritative for a subdomain but the parent domain. In such cases you can 
override which zone is used when the nsupdate is issued. For example:

* certificate zone (acme_domain.zone) = mysub.example.org
* DNS is authoritative for example.org and the zonefile should contain the following entry
```
_acme-challenge.mysub.example.org. 120 IN TXT   "nsupdate-test123"
```
In this scenario the following dictionary should be placed in acme_nsupdate_override_domain
```
acme_domain:
  certificate_name: "mysub.example.org"
  zone: "example.org"
  subject_alt_name:
    - "test.example.org"
    - "domain1.example.org"
    - "domain2.example.org"
```

The same is true for SAN certificates. Please note, that SAN certificates can have multiple subdomain names but
are limited to one zone.
```
acme_domain:
  certificate_name: "mysub.example.org"
  zone: "example.org"
```

### acme_nsupdate_replication_delay
If you are using a primary/secondary DNS server setup it might be a good idea to wait a second or two after the 
nsupdate on the primary was issued.
