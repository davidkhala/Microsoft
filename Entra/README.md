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

- Administrators don't need to manage, update, and monitor domain controllers.
- Administrators don't need to deploy and manage Active Directory replication.
- There’s no need to have Domain Admins or Enterprise Admins groups for domains that Microsoft Entra ID manages.
- No more computer class.
  - Only the base computer AD object is supported.
  - Entra Solution: Use device class
- No more organizational unit (OU) class.
  - The organizational unit (OU) structure is flat and nested OUs aren't currently supported.
  - Entra Solution: Organizing objects based on their group membership
- > The process of joining devices to Microsoft Entra differs considerably from the process of joining computers to AD
  - You cannot use Group Policy Objects (GPOs)
  - There’s a built-in Group Policy Object (GPO), and it exists for computer and user accounts.
  - You cannot target OUs with built-in GPOs. 
  - You can't use Windows Management Instrumentation filters or security-group filtering.
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
- It’s not possible to extend the schema for the Microsoft Entra Domain Services domain.

## Paid Tiers
license
- Standalone: You can procure them as an extra license
- Included in Microsoft Enterprise Mobility + Security

### P1 tier
Features
- Self-service group management
  - users are given the rights to create and manage the groups
  - End user can request and get approved to join other group
- Advanced security reports and alerts (ML based)
  - advanced anomalies and inconsistent access pattern reports
- Multi-factor authentication
  - Limit: It doesn't work with non-browser off-the-shelf apps, such as Microsoft Outlook
- Microsoft Identity Manager (MIM) licensing
  - MIM can bridge multiple on-premises authentication stores such as AD DS, LDAP, Oracle, and other applications with Microsoft Entra ID.
  - This provides consistent experiences to on-premises line-of-business (LOB) applications and SaaS solutions.
- Password reset with writeback
  - Self-service password reset follows the AD on-premises password policy.
- Entra Connect Health

### P2 tier
P1 tier features plus:
- Microsoft Entra ID Protection
  - define policies for user risk and sign-in
  - review user behavior and flag users for risk
- Microsoft Entra Privileged Identity Management: additional security levels for privileged users
  - define permanent and temporary administrators.
  - define a policy workflow that activates whenever someone wants to use administrative privileges to perform some task (sudo like).