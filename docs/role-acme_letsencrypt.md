# Let's Encrypt role

This role issues Let's Encrypt certificates via DNS-01 or HTTP-01 challenge.

This role does not distribute certificates - it only creates them. You have to implement the distribution in your own playbooks roles.

## Providers

The role supports multiple providers for http- and dns-challenges.
Please see the corresponding readme files for specific variables and examples.

Feel free to contribute more DNS or HTTP APIs :)

* DNS
  * [AutoDNS](dns-challenge/autodns.md)
  * [Azure](dns-challenge/azure.md)
  * [hetzner](dns-challenge/hetzner.md)
  * [openstack](dns-challenge/openstack.md)
  * [pebble](dns-challenge/pebble.md)
* HTTP
  * [local](http-challenge/local.md)
  * [s3](http-challenge/s3.md)

## General variables

| Variable                             | Required | Default | Description
|--------------------------------------|----------|---------|------------
| **domain configuration**
| certificate_name                     | yes      |         | Name of the resulting certificate. Most useful for wildcard certificates to not have files named '*.example.com' on the filesystem
| zone                                 | yes      |         | zone in which the dns records should be created
| subject_alt_name                     | yes      |         | Domain(s) for which the certificate(s) should be validated. If you are issuing a wildcard certificate you should also add the main domain for which you are issuing the certificate
| email_address                        | yes      |         | Mail address which is used for the certificate (reminder mails are sent here)
| **configuration options**
| acme_letsencrypt_account_key_content | no       |         | Content of the created letsencrypt account key
| acme_letsencrypt_private_key_content | no       |         | Content of the created private key for the certificate (allows reuse of keys)
| acme_letsencrypt_use_live_directory  | no       | false   | Choose if production certificates should be created, the staging directory of LE will be used by default
| acme_letsencrypt_force_renewal       | no       |         | Force renewal of certificate before `remaining_days` is reached
| acme_letsencrypt_challenge_provider  | yes      |         | Which DNS provider should be used. See "Usage" of provider for the correct keyword

## Variables for dns-challenge

| Variable                            | Required | Default | Description
|-------------------------------------|----------|---------|------------
| acme_letsencrypt_dns_user           | yes      |         | Username to access the DNS api
| acme_letsencrypt_dns_password       | yes      |         | Password to access the DNS api


## Global role variables

| Variable                                      | Required | Default                              | Description
|-----------------------------------------------|----------|--------------------------------------|------------
| acme_letsencrypt_conf_dir                     | no       | $HOME/letsencrypt                    | Overwrite acme_letsencrypt_conf_dir if you want to use another directory which is accessible to the user which runs the playbook
| acme_letsencrypt_prerequisites_packagemanager | no       | yum                                  | Set the packagemanager which is used of the ansible_host. Possible values are all supported package managers from ansible package module
| acme_letsencrypt_staging_directory            | no       | acme-staging-v02.api.letsencrypt.org | Acme directory which will be used for certificate challenge
| acme_letsencrypt_live_directory               | no       | acme-v02.api.letsencrypt.org         | Acme directory which will be used for certificate challenge
| acme_letsencrypt_account_key_path             | no       | $acme_letsencrypt_conf_dir           | Path for account key of letsencrypt
| acme_letsencrypt_csr_path                     | no       | $acme_letsencrypt_conf_dir/certs     | Path for csr which is created for challenge
| acme_letsencrypt_cert_path                    | no       | $acme_letsencrypt_conf_dir/certs     | Path for issued certificate
| acme_letsencrypt_intermediate_path            | no       | $acme_letsencrypt_conf_dir/certs     | Path for intermediate chain
| acme_letsencrypt_fullchain_path               | no       | $acme_letsencrypt_conf_dir/certs     | Path for full chain file (certificate + intermediate)
| acme_letsencrypt_private_key_path             | no       | $acme_letsencrypt_conf_dir/certs     | Path for private key
| acme_letsencrypt_remaining_days               | no       | 30                                   | Min days remaining before certificate will be renewed
| acme_letsencrypt_convert_cert_to              | no       |                                      | Format to convert the certificate to: `pfx`
| acme_letsencrypt_validate_certs               | no       |                                      | Only used in integration tests with pebble server

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
