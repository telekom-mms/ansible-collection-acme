# letsencrypt

This role issues Let's Encrypt certificates via DNS-01 or HTTP-01 challenge.


For distribution of certificates please implement your own playbooks/roles/tasks

## Installation

```bash
ansible-galaxy collection install t_systems_mms.letsencrypt
```

## Providers

The role supports multiple providers for http- and dns-challenges.
Please see the corresponding readme files for specific variables and examples.

Feel free to contribute with more DNS APIs or more HTTP variants :)

### http-challenge

Following providers for a http-challenge are currently supported.

| Provider                         | Description
|----------------------------------|-------------
| [s3](http-challenge/s3.md)       | uses a aws s3 bucket for validation/hash files
| [local](http-challenge/local.md) | uses a local path at your server/machine for validation/hash files

### dns-challenge

Following providers for a dns-challenge are currently supported.

| Provider                                | Description
|-----------------------------------------|-------------
| [AutoDNS](dns-challenge/autodns.md)     |
| [Azure](dns-challenge/azure.md)         |
| [hetzner](dns-challenge/hetzner.md)     |
| [openstack](dns-challenge/openstack.md) |
| [pebble](dns-challenge/pebble.md)       | used for integration tests in github workflow

## General variables

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| **domain configuration**
| certificate_name                    | yes      |         | name of the resulting certificate. Most useful for wildcard certificates to not have files named '*.example.com' on the filesystem
| zone                                | yes      |         | zone in which the dns records should be created
| subject_alt_name                    | yes      |         | if you want to use wildcard-certificates use base name again as otherwise DNS txt record creation could fail
| email_address                       | yes      |         | mail address which is used for the certificate (reminder mails are sent here)
| **configuration options**           |          |         |
| account_key_content                 | no       |         | content of the created letsencrypt account key
| private_key_content                 | no       |         | content of the created private key for the certificate (allows reuse of keys)
| letsencrypt_do_http_challenge       | yes      | false   | use http challenge
| letsencrypt_do_dns_challenge        | yes      | false   | use dns challenge
| letsencrypt_use_acme_live_directory | no       | false   | choose if production certificates should be created, the staging directory of LE will be used by default
| force_renewal                       | no       |         | Force renewal of certificate before `remaining_days` is reached

## Variables for http-challenge

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| letsencrypt_http_provider           | yes      |         | which http provider should be used: s3, local

## Variables for dns-challenge

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| dns_user                            | yes      |         | username to access the DNS api
| dns_password                        | yes      |         | password to access the DNS api
| letsencrypt_dns_provider            | yes      |         | which DNS provider should be used: autodns, azure, hetzner, pebble, openstack

## Global role variables

| Variable                                 | Required | Default                              | Description
|------------------------------------------|----------|--------------------------------------|------------
| letsencrypt_conf_dir                     | no       | $HOME/letsencrypt                    | overwrite letsencrypt_conf_dir if you want to use another directory which is accessible to the user which runs the playbook
| letsencrypt_prerequisites_packagemanager | no       | yum                                  | set the packagemanager which is used of the ansible_host. Possible values are all supported package managers from ansible package module
| acme_staging_directory                   | no       | acme-staging-v02.api.letsencrypt.org | acme directory which will be used for certificate challenge
| acme_live_directory                      | no       | acme-v02.api.letsencrypt.org         | acme directory which will be used for certificate challenge
| account_key_path                         | no       | $letsencrypt_conf_dir                | path for account key of letsencrypt
| csr_path                                 | no       | $letsencrypt_conf_dir/certs          | path for csr which is created for challenge
| cert_path                                | no       | $letsencrypt_conf_dir/certs          | path for issued certificate
| intermediate_path                        | no       | $letsencrypt_conf_dir/certs          | path for intermediate chain
| fullchain_path                           | no       | $letsencrypt_conf_dir/certs          | path for full chain file (certificate + intermediate)
| private_key_path                         | no       | $letsencrypt_conf_dir/certs          | path for private key
| remaining_days                           | no       | 30                                   | min days remaining before certificate will be renewed
| convert_cert_to                          | no       |                                      | format to convert the certificate to: `pfx`
| validate_certs (bool)                    | no       |                                      | Gets used during integration tests with pebble server

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
      - ansible-playbook playbooks/letsencrypt/domain1.yml --vault-password-file .vault_password.txt --diff
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
        - ansible-playbook playbooks/letsencrypt/all-certificates.yml --vault-password-file . vault_password.txt --diff
        - rm -f .vault_password.txt
    ```
