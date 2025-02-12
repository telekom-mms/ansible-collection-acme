# Variables for nsupdate dns-challenge

None

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
    acme_domain:
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "*.example.com"
    acme_challenge_provider: nsupdate
    acme_use_live_directory: false
    acme_account_email: "ssl-admin@example.com"
    acme_nsupdate_server: "{{ lookup('community.general.dig', 'primary.nsforexample.com', qtype='A') }}"
    acme_nsupdate_dns_key:
          name: 'nsupdate_key'
          algorithm: hmac-sha512
          secret: ""
```

### SAN certificate

```yaml
- name: create the certificate for example.com
  hosts: localhost
  collections:
    - telekom_mms.acme
  roles:
    - acme
  vars:
    acme_domain:
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "example.com"
        - "domain1.example.com"
        - "domain2.example.com"
    acme_challenge_provider: nsupdate
    acme_use_live_directory: false
    acme_account_email: "ssl-admin@example.com"
    acme_nsupdate_server: "{{ lookup('community.general.dig', 'primary.nsforexample.com', qtype='A') }}"
    acme_nsupdate_dns_key:
        name: 'nsupdate_key'
        algorithm: hmac-sha512
        secret: ""
```

### acme_nsupdate_server
The acme_nsupdate_server MUST be a IPv4/IPv6 address (limitation of the nsupdate ansible module). To work with a DNS 
name, you can use the dig lookup: 
```
acme_nsupdate_server: "{{ lookup('community.general.dig', 'primary.nsforexample.com', qtype='A') }}"
```

### acme_nsupdate_override_domain
In some cases your DNS server may not be authoritative for a subdomain but the parent domain. In such cases you can override
which zone is used when the nsupdate is issued. For example:

* certificate zone (acme_domain.zone) = mysub.example.org
* DNS is authoritative for example.org and the zonefile should contain the following entry
```
_acme-challenge.mysub.example.org. 120 IN TXT   "nsupdate-test123"
```
In this scenario the following dictionary should be placed in acme_nsupdate_override_domain
```
acme_nsupdate_override_domain: 
  mysub.example.org: example.org
```

### acme_nsupdate_replication_delay
If you are using a primary/secondary DNS server setup it might be a good idea to wait a second or two after the 
nsupdate on the primary was issued.
