# letsencrypt

This role issues Let's Encrypt certificates via DNS-01 or HTTP-01 challenge.

**Please note that you have to use a dns-challenge if you want to issue wildcard certificates.**

For distribution of certificates please implement your own playbooks/roles/tasks

## Installation

```bash
ansible-galaxy collection install t_systems_mms.letsencrypt
```

## http-challenge

The validation via http-challenge currently supports the usage of a local path at the webserver and also an AWS S3 bucket to safe the hashfiles.

Please see [the corresponding README](README-http-challenge.md) for usage hints and variables of the HTTP-01 challenge

## dns-challenge

Currently the role supports the InternetX autodns, Azure DNS, and Hetzner API. Feel free to contribute with other DNS APIs.

Please see [the corresponding README](README-dns-challenge.md) for variables of the DNS-01 challenge

## Shared variables for DNS & HTTP challenge

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| **domain configuration**
| certificate_name                    | yes      |         | name of the resulting certificate. Most useful for wildcard certificates to not have files named '*.example.com' on the filesystem
| zone                                | yes      |         | zone in which the dns records should be created
| subject_alt_name                    | yes      |         | list of names which should be validated, this includes the deprecated common_name (see [here](https://tools.ietf.org/html/rfc2818#section-3.1))
| subject_alt_name: top_level:        | no       |         | list of top-level domains
| subject_alt_name: second_level:     | no       |         | list of second_level domains
| email_address                       | yes      |         | mail address which is used for the certificate (reminder mails are sent here)
| **configuration options**           |          |         |
| private_key_content                 | no       |         | content of the created private key for the certificate (allows reuse of keys)
| letsencrypt_do_http_challenge       | yes      | false   | use http challenge
| letsencrypt_do_dns_challenge        | yes      | false   | use dns challenge
| letsencrypt_use_acme_live_directory | no       | false   | choose if production certificates should be created, the staging directory of LE will be used by default
| azure_resource_group                | no       |         | Azure Resource Group for zone_name
| force_renewal                       | no       |         | Force renewal of certificate

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

## Usage

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
