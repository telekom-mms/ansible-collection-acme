# letsencrypt

This role issues Let's Encrypt certificates via DNS-01 or HTTP-01 challenge.

**Please note that you have to use a dns-challenge if you want to issue wildcard certificates.**

For distribution of certificates please implement your own playbooks/roles/tasks

## Installation

```bash
ansible-galaxy collection install t_systems_mms.letsencrypt
```

## http-challenge

It currently uses an AWS S3 bucket to safe the hashfiles. You have to set a redirect rule in your proxy or webserver to allow the acme challenge bot to read the file, during the http-01 challenge to work:

**HaProxy(Version <=> 1.5):**

```bash
  # lets encrypt redirect
  http-request del-header X-REWRITE
  http-request add-header X-REWRITE %[url] if { path_beg /.well-known/acme-challenge }
  http-request replace-header X-REWRITE ^(.well-known/acme-challenge/.*)?$ /\1 if { hdr_cnt(X-REWRITE) gt 0 }
  http-request redirect code 301 location https://letsencrypt-challenge-bucket.s3.amazonaws.com%[hdr(X-REWRITE)] if { hdr_cnt(X-REWRITE) gt 0 }
```

**HaProxy(Version >= 1.6):**

```bash
http-request redirect code 301 location https://letsencrypt-challenge-bucket.s3.amazonaws.com%[url,regsub(^/.well-known/acme-challenge,/.well-known/acme-challenge,)] if { path_beg /.well-known/acme-challenge }
```

(can be set in frontend oder backend definition)

**Apache:**

```bash
RewriteRule (\.well-known/acme-challenge.*) https://letsencrypt-challenge-bucket.s3.amazonaws.com/$1
```

**Nginx:**

```bash
rewrite (\.well-known/acme-challenge.*) https://letsencrypt-challenge-bucket.s3.amazonaws.com/$1
```

## dns-challenge
Currently the role supports the InternetX autodns API and the Azure DNS API. Feel free to contribute with other DNS APIs.

## Variables for DNS & HTTP challenge

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| **domain configuration**
| certificate_name                    | yes      |         | name of the resulting certificate. Most useful for wildcard certificates to not have files named '*.example.com' on the filesystem
| zone                                | yes      |         | zone in which the dns records should be created
| subject_alt_name                    | yes      |         | if you want to use wildcard-certificates use base name again as otherwise DNS txt record creation could fail
| subject_alt_name: top_level:        | no       |         | list of top-level domains
| subject_alt_name: second_level:     | no       |         | list of second_level domains
| email_address                       | yes      |         | mail address which is used for the certificate (reminder mails are sent here)
| **configuration options**           |          |         |
| account_key_content                 | no       |         | content of the created letsencrypt account key
| private_key_content                 | no       |         | content of the created private key for the certificate (allows reuse of keys)
| letsencrypt_do_http_challenge       | yes      | false   | use http challenge
| letsencrypt_do_dns_challenge        | yes      | false   | use dns challenge
| letsencrypt_use_acme_live_directory | no       | false   | choose if production certificates should be created, the staging directory of LE will be used by default
| azure_resource_group                | no       |         | Azure Resource Group for zone_name
| force_renewal                       | no       |         | Force renewal of certificate

## Variables for HTTP challenge

| Variable                            | Required | Default   | Description
|-------------------------------------|----------|-----------|------------
| letsencrypt_s3_bucket_name          | yes      |           | name of the s3 bucket which should be used
| letsencrypt_s3_access_key           | yes      |           | aws access key for API user of s3 bucket
| letsencrypt_s3_secret_key           | yes      |           | aws secret key for API user of s3 bucket
| letsencrypt_s3_config_region        | no       | us-west-1 | aws s3 region in which bucket can be found

## Variables for dns-challenge

| Variable                 | Required | Default   | Description
|--------------------------|----------|-----------|------------
| dns_user                 | yes      |           | username to access the DNS api
| dns_password             | yes      |           | password to access the DNS api
| letsencrypt_dns_provider | no       |         | which DNS provider should be used: autodns, azure

## global role variables

| Variable                                 | Required | Default                              | Description
|------------------------------------------|----------|--------------------------------------|------------
| letsencrypt_conf_dir                     | no       | $HOME/letsencrypt                    | overwrite letsencrypt_conf_dir if you want to use another directory which is accessible for the user which runs the playbook
| letsencrypt_prerequisites_packagemanager | yes      | yum                                  | set the packagemanager which is used of the ansible_host. Possible values are all supported package managers from ansible package module
| acme_staging_directory                   | no       | acme-staging-v02.api.letsencrypt.org | acme directory which will be used for certificate challenge
| acme_live_directory                      | no       | acme-v02.api.letsencrypt.org         | acme directory which will be used for certificate challenge
| account_key_path                         | yes      | $letsencrypt_conf_dir                | path for account key of letsencrypt
| csr_path                                 | yes      | $letsencrypt_conf_dir/certs          | path for csr which is created for challenge
| cert_path                                | yes      | $letsencrypt_conf_dir/certs          | path for issued certificate
| intermediate_path                        | yes      | $letsencrypt_conf_dir/certs          | path for intermediate chain
| fullchain_path                           | yes      | $letsencrypt_conf_dir/certs          | path for full chain file (certificate + intermediate)
| private_key_path                         | yes      | $letsencrypt_conf_dir/certs          | path for private key
| remaining_days                           | yes      | 30                                   | min days remaining before certificate will be renewed
| convert_cert_to                          | no       |                                      | format to convert the certificate to: `pfx`

### Usage

```bash
ansible-playbook playbooks/letsencrypt.yml --ask-vault
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
      - ansible-playbook playbooks/letsencrypt/domain1.yml --vault-password-file .vault_password.txt --diff
      - rm -f .vault_password.txt
  ```

* if you have multiple domains for which a certificate should be created, create a job in gitlab-ci to run a playbook which imports all certificate playbooks of your domains
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
        - ansible-playbook playbooks/letsencrypt/all-certificates.yml --vault-password-file . vault_password.txt --diff
        - rm -f .vault_password.txt
    ```

## Example playbooks
### SAN certificate

```yaml
- name: create the certificate for domain1
  hosts: localhost
  roles:
    - letsencrypt
  vars:
    domain:
      certificate_name: "domain1.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - domain2.example.com
    letsencrypt_do_http_challenge: true
    letsencrypt_do_dns_challenge: false
    letsencrypt_use_acme_live_directory: false
    account_email: "ssl-admin@example.com"
    private_key_content: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          ....
    letsencrypt_s3_bucket_name: "example-ssl-bucket"
    letsencrypt_s3_access_key: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
    letsencrypt_s3_secret_key: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```

### Wildcard certificate

```yaml
- name: create the certificate for domain1
  hosts: localhost
  roles:
    - letsencrypt
  vars:
    domain:
      certificate_name: "wildcard.example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - "example.com"
    letsencrypt_do_http_challenge: false
    letsencrypt_do_dns_challenge: true
    letsencrypt_use_acme_live_directory: false
    account_email: "ssl-admin@example.com"
    private_key_content: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          ....
    dns_user: "example_dns"
    dns_password: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
```
