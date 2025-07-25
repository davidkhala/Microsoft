# MicroSoft Entra ID

The new unified IAM

- PaaS [portal](https://entra.microsoft.com/)
  - > It’s the world’s largest multi-tenant directory
  - > hosting over a million directory services instances - > billions of authentication requests per week.
- A new tenant will be automatically provisioned and assigned to any new subscription of
  - Azure
  - Microsoft Online business services (M365 or Microsoft Intune)
  - D365
- suffiex `onmicrosoft.com`

[manage by Azure CLI `az`](https://github.com/davidkhala/azure-utils/blob/main/cli/entra)

Features

- multi-tenant
  - Within an Azure subscription, you can create multiple Microsoft Entra tenants
  - You can associate the same Microsoft Entra tenant with multiple Azure subscriptions.
- MFA
- **SSO**: Enabling federation between organizations
  - third-party services (e.g. Facebook, Google, Yahoo) are federated with and trust Microsoft Entra ID.
- self-service password reset
- Extending existing on-premises Active Directory implementations to Microsoft Entra ID
- Configuring Application Proxy for cloud and local applications
- Configuring Conditional Access for users and devices

## Microsoft Entra schema

Diff than AD

- No more computer class.
  - Use device class instead
- No more organizational unit (OU) class.
  - Organizing objects based on their group membership, instead
- > The process of joining devices to Microsoft Entra differs considerably from the process of joining computers to AD
  - You cannot use Group Policy Objects (GPOs)
- Represent applications in Microsoft Entra ID.
  - An object in the Application class contains an application definition
  - An object in the servicePrincipal class constitutes its instance in the current Microsoft Entra tenant.
    - Provisioned when you register the corresponding application in that Microsoft Entra tenant
    - define the binding between app and Entra tenant
  - You can define an application in one tenant and use it across multiple tenants by creating a service principal object for this application in each tenant.
- You can't query Microsoft Entra ID by using LDAP
  - Use REST API instead
- Microsoft Entra ID doesn't use Kerberos authentication
  - Use SAML, WS-Federation, and OpenID Connect for authentication,
  - Use OAuth for authorization

## Paid Tiers
