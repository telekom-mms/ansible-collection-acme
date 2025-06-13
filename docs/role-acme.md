# Acme role

This role issues certificates via the ACME protocol. By default the API of Let's Encrypt is used.

This role does not distribute certificates - it only creates them. You have to implement the distribution in your own playbooks or roles.

## Providers

The role supports multiple providers for http- and dns-challenges.
Please see the corresponding readme files for specific variables and examples.

Feel free to contribute more DNS or HTTP APIs :)

* DNS-01
  * [AutoDNS](/docs/dns-challenge/autodns.md)
  * [Azure](/docs/dns-challenge/azure.md)
  * [Domain Offensive](/docs/dns-challenge/domain-offensive.md)
  * [hetzner](/docs/dns-challenge/hetzner.md)
  * [openstack](/docs/dns-challenge/openstack.md)
  * [pebble](/docs/dns-challenge/pebble.md)
* HTTP-01
  * [local](/docs/http-challenge/local.md)
  * [s3](/docs/http-challenge/s3.md)

## General variables

| Variable                             | Required | Default | Description                                                                                                                                                                                                                                                       |
|--------------------------------------|----------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **domain configuration acme_domain** |          |         |                                                                                                                                                                                                                                                                   |
| certificate_name                     | yes      |         | Name of the resulting certificate. Most useful for wildcard certificates to not have files named '*.example.com' on the filesystem                                                                                                                                |
| zone                                 | yes      |         | zone in which the dns records should be created                                                                                                                                                                                                                   |
| subject_alt_name                     | yes      |         | Domain(s) for which the certificate(s) should be validated. If you are issuing a wildcard certificate you should also add the main domain for which you are issuing the certificate                                                                               |
| email_address                        | yes      |         | Mail address which is used for the certificate (reminder mails are sent here) and the field `email_address` as specified in section [4.1.2.6. Subject](https://datatracker.ietf.org/doc/html/rfc5280#section-4.1.2.6 "Link to the IETF RFC 5280") of the RFC 5280 |
| country                              | no       |         | containing a digraph for the country as in ISO 3166                                                                                                                                                                                                               |
| state_or_province                    | no       |         | a string representing the state or province to be put into the subject field of the certificate                                                                                                                                                                   |
| locality                             | no       |         | a string representing a locality to be put into the subject field of the certificate                                                                                                                                                                              |
| organization                         | no       |         | a string representing the organization to be put into the subject field of the certificate                                                                                                                                                                        |
| organizational_unit                  | no       |         | a string representing the organizational unit to be put into the subject field of the certificate                                                                                                                                                                 |
| common_name                          | yes*no   |         | MUST be set, if any of the other fields `country`, `state_or_province`, `locality`, `organization` or `organizational_unit` does contain any value. MUST be a domain name as you would give it for a Subject Alternative Name                                     |
| **configuration options**            |          |         |                                                                                                                                                                                                                                                                   |
| acme_account_key_content             | no       |         | Content of the created account key                                                                                                                                                                                                                                |
| acme_private_key_content             | no       |         | Content of the created private key for the certificate (allows reuse of keys)                                                                                                                                                                                     |
| acme_use_live_directory              | no       | false   | Choose if production certificates should be created, the staging directory of LE will be used by default                                                                                                                                                          |
| acme_force_renewal                   | no       |         | Force renewal of certificate before `remaining_days` is reached                                                                                                                                                                                                   |
| acme_challenge_provider              | yes      |         | Which DNS provider should be used. See "Usage" of provider for the correct keyword                                                                                                                                                                                |
| acme_challenge_handling              | no       | default | Changes the handling of API response (see below)  ('default', or 'with_authorizations')                                                                                                                                                                           |
| acme_challenge_timeout               | no       | 3600    | How long to wait on a challenge check to succeed before a failure is thrown                                                                                                                                                                                       |

## Variables for dns-challenge

| Variable          | Required | Default | Description                    |
|-------------------|----------|---------|--------------------------------|
| acme_dns_user     | yes      |         | Username to access the DNS api |
| acme_dns_password | yes      |         | Password to access the DNS api |

## Variables for Certificate Download

If you are running this role in a temporary environment such as a CI runner and you use your certificates on a https server you can enable the download of the current certificate from the web server. This prevents unnecessary renewal of certificates which aren't due for renewal yet.

| Variable                | Required | Default                           | Description                                  |
|-------------------------|----------|-----------------------------------|----------------------------------------------|
| acme_download_cert      | no       | false                             | Enable Certificate Download                  |
| acme_cert_download_host | no       | uses first SAN of the Certificate | Hostname/IP to Download the Certificate from |
| acme_cert_download_port | no       | 443                               | Port to Download the Certificate from        |
| acme_cert_san_name      | no       | uses first SAN of the Certificate | Hostname for SNI for Cert File Download      |

## Global role variables

| Variable                          | Required | Default                              | Description                                                                                                                              |
|-----------------------------------|----------|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| acme_conf_dir                     | no       | $HOME/letsencrypt                    | Overwrite acme_conf_dir if you want to use another directory which is accessible to the user which runs the playbook                     |
| acme_prerequisites_packagemanager | no       | yum                                  | Set the packagemanager which is used of the ansible_host. Possible values are all supported package managers from ansible package module |
| acme_staging_directory            | no       | acme-staging-v02.api.letsencrypt.org | Acme directory which will be used for certificate challenge                                                                              |
| acme_live_directory               | no       | acme-v02.api.letsencrypt.org         | Acme directory which will be used for certificate challenge                                                                              |
| acme_account_key_path             | no       | $acme_conf_dir                       | Path for account key                                                                                                                     |
| acme_account_key_size             | no       | 4096                                 | Account key size                                                                                                                         |
| acme_account_key_type             | no       | ECC                                  | Account key type                                                                                                                         |
| acme_account_key_curve            | no       | secp384r1                            | Account key curve used                                                                                                                   |
| acme_csr_path                     | no       | $acme_conf_dir/certs                 | Path for csr which is created for challenge                                                                                              |
| acme_cert_path                    | no       | $acme_conf_dir/certs                 | Path for issued certificate                                                                                                              |
| acme_intermediate_path            | no       | $acme_conf_dir/certs                 | Path for intermediate chain                                                                                                              |
| acme_fullchain_path               | no       | $acme_conf_dir/certs                 | Path for full chain file (certificate + intermediate)                                                                                    |
| acme_private_key_path             | no       | $acme_conf_dir/certs                 | Path for private key                                                                                                                     |
| acme_private_key_size             | no       | 4096                                 | Private key size                                                                                                                         |
| acme_private_key_type             | no       | ECC                                  | Private key type                                                                                                                         |
| acme_private_key_curve            | no       | secp384r1                            | Private key curve used                                                                                                                   |
| acme_remaining_days               | no       | 30                                   | Min days remaining before certificate will be renewed                                                                                    |
| acme_convert_cert_to              | no       |                                      | Format to convert the certificate to: `pfx`                                                                                              |
| acme_validate_certs               | no       |                                      | Only used in integration tests with pebble server                                                                                        |

### Usage

```bash
ansible-playbook playbooks/domain1.yml [--ask-vault]
```

### gitlab-pipeline

* create a job which runs the certificate playbook

  ```yaml
  stages:
    - renew-certificates

  certificates:
    stage: renew-certificates
    script:
      - echo $ANSIBLE_VAULT_PASSWORD > .vault_password.txt
      - ansible-playbook playbooks/acme-certificates/domain1.yml --vault-password-file .vault_password.txt --diff
      - rm -f .vault_password.txt
  ```

* if you have multiple domains, for which a certificate should be created, create a job in gitlab-ci to run a playbook which imports all certificate playbooks of your domains
  * playbook to import certificate playbooks

    ```yaml
    - name: import play for domain1
      import_playbook: domain1.yml

    - name: import play for domain2
      import_playbook: domain2.yml
    ```

  * run playbook

    ```yaml
    stages:
    - renew-certificates

    certificates:
      stage: renew-certificates
      script:
        - echo $ANSIBLE_VAULT_PASSWORD > .vault_password.txt
        - ansible-playbook playbooks/acme-certificates/all-certificates.yml --vault-password-file . vault_password.txt --diff
        - rm -f .vault_password.txt
    ```

# notes
## Handling of API responses
ACME providers seam to have slightly different formats in the Response when validation a process already has started 
for a domain. To be more flexible on that, this change adds the find_challenges filter plugin which parses the data 
into a standardized format for the challenge provider task modules.

## default handling (acme_challenge_handling: 'default')
The default handling will search the tokens for challenge validations always in the `challenge_data` field. An 
AssertionError will be raised of the data is not present.

### Handling with 'authorizations' (acme_challenge_handling: 'with_authorizations')
The DTAG Telesec API will only respond with the challenge data in the `challenge_data` field only if the certificate
is new, or the due date has reached. The problem with that is, that if the ansible run fails or you want to renew
the certificate prior to the due date, the role will fail as `challenge_data` is empty. In such cases the API will
use the `authorizations` field.

An AssertionError will be raised of the data is not present.

**new or due-date reached**
```
authorizations:
  blahtest1.example.org:
    challenges:
    - status: pending
      token: Uwqt4U_l6lp04J2KW5nvgJ6LMPXvSrhr
      type: dns-01
      url: https://ACME.telesec.de/v2/...
    - status: pending
      token: ukTTEZIqv_KM9J0iEnysAaiiO31-Rpxg
      type: http-01
      url: https://ACME.telesec.de/v2/....
    expires: '2025-03-26T09:00:45Z'
    identifier:
      type: dns
      value: blahtest1.example.org
    status: pending
    uri: https://ACME.telesec.de/v2/...
    cert_days: -1
challenge_data:
  blahtest1.example.org:
   dns-01:
     record: _acme-challenge.blahtest1.example.org
     resource: _acme-challenge
     resource_value: bob4Yd3_SVv-7JET__3G5ZDVWaeGIOxAQmRf3SURbSY
   http-01:
     resource: .well-known/acme-challenge/ukTTEZIqv_KM9J0iEnysAaiiO31-Rpxg
     resource_value: L0bB8aZyOyuw5LNDlslQptrKYBw5P0nPpmt6bGhTYyWP1wTogi9W3V.L0bB8aZyOyuw5LNDlslQptrKYBw5P0nPpmt6bGhTYyWP1wTogi9W3V
  blahtest2.example.org:
   dns-01:
     record: _acme-challenge.blahtest2.example.org
     resource: _acme-challenge
     resource_value: eksnHDhxBOzrTlOgiDzKlUXZtccjSwKIhc
   http-01:
     resource: .well-known/acme-challenge/ukTTEZIqv_KM9J0iEnysAaiiO31-Rpxg
     resource_value: 8fV3Wc5hIqxMohz4llcqLqHuCv7WriMrgWYRogPypoTY5KRT84sfeU.8fV3Wc5hIqxMohz4llcqLqHuCv7WriMrgWYRogPypoTY5KRT84sfeU
challenge_data_dns:
  _acme-challenge.blahtest1.example.org:
    - bob4Yd3_SVv-7JET__3G5ZDVWaeGIOxAQmRf3SURbSY
  _acme-challenge.blahtest2.example.org:
    - eksnHDhxBOzrTlOgiDzKlUXZtccjSwKIhc
```

**due date not reached**
```
authorizations:
  blahtest1.example.org:
    challenges:
      - status: valid
        token: Uwqt4U_l6lp04J2KW5nvgJ6LMPXvSrhr
        type: dns-01
        url: https://ACME.telesec.de/v2/...
        validated: '2025-03-15T13:15:53Z'
    identifier:
      type: dns
      value: blah.nicoint.de
    expires: '2025-04-15T09:00:45Z'
    identifier:
      type: dns
      value: blahtest1.example.org
    status: valid
    uri: https://ACME.telesec.de/v2/...
cert_days: 30
challenge_data: {}
challenge_data_dns: {}
```