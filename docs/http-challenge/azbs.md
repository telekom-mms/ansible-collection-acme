# Variables for Azure blob storage http-challenge

| Variable              | Required | Default   | Description
|-----------------------|----------|-----------|------------
| acme_azbs_resource_group   | yes      |           | Name of the Azure resource group to which the storage account has been allocated
| acme_azbs_storage_account_name    | yes      |           | Azure storage account name which should be used
| acme_azbs_container_name    | yes      |           | Azure container name which will be used/created in Azure storage account
| acme_azbs_subscription_id | yes       | | Azure subscription id
| acme_azbs_client_id | yes | | Client ID of service principal/application
| acme_azbs_secret | yes | | Value of secret of service principal/application (Note: not the ID)
| acme_azbs_tenant_id | yes | | Tenant ID of service principal/application

## Validation

You have to create a service principal/application in the Azure Active Directory.
This can be done via Frontend, Azure CLI or terraform.

### Frontend

`Azure Login > Active directory >  App registrations`

### Azure CLI

```bash
az login # open link and insert code from console to "login"
az ad sp create-for-rbac --name https://somedomain.onmicrosoft.com/my-app-name --scopes /subscriptions/my-subscription-id/resourceGroups/my-resource-group-name

# Example:
az login
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code xxxx to authenticate.

az ad sp create-for-rbac --name https://example.onmicrosoft.com/my-app-name --scopes /subscriptions/00000-111111-22222-333333-44444-/resourceGroups/my-resource-group-name
```

> Note that you have to set a verified domain name of your organization or its subdomains when service principal is created via CLI.

You have to set a redirect rule in your proxy or webserver to allow the acme challenge bot to read the file, during the http-01 challenge to work.

*Please note that the URL for the bucket needs to be adjusted to the name of your used bucket.*

**HaProxy:**
*works with version >= 1.6*

```bash
http-request redirect code 301 location https://your-storage-account-name.blob.core.windows.net[url,regsub(^/.well-known/acme-challenge,/my-containername,)] if { path_beg /.well-known/acme-challenge }
```

(can be set in frontend or backend definition)

**Apache:**

```bash
RewriteRule \.well-known/acme-challenge/(.*) https://your-storage-account-name.blob.core.windows.net/your-container-name/$1
```

**Nginx:**

```bash
rewrite \.well-known/acme-challenge/(.*) https://your-storage-account-name.blob.core.windows.net/your-container-name/$1
```

## Usage

> you should think about encrypting all azure account infos

```yaml
- name: create the certificate for example.com
  hosts: localhost
  collections:
    - t_systems_mms.acme
  roles:
    - acme
  vars:
    acme_domain:
      certificate_name: "example.com"
      zone: "example.com"
      email_address: "ssl-admin@example.com"
      subject_alt_name:
        - example.com
        - domain1.example.com
        - domain2.example.com
    acme_challenge_provider: "azbs"
    acme_use_live_directory: false
    acme_account_email: "ssl-admin@example.com"
    acme_azbs_resource_group: "my-resource-group"
    acme_azbs_storage_account_name: "my-storage-account-name"
    acme_azbs_container_name: "my-container"
    acme_azbs_subscription_id: "0000-11111-2222-3333-444444"
    acme_azbs_client_id: "1234-21231-14152-1231"
    acme_azbs_secret: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              ...
    acme_azbs_tenant_id: "2132184-3534543-54354-3543"
```
