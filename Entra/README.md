# MicroSoft Entra

The new unified IAM

- PaaS [portal](https://entra.microsoft.com/)
  - > It’s the world’s largest multi-tenant directory
  - > hosting over a million directory services instances - > billions of authentication requests per week.
- A new tenant will be automatically provisioned and assigned to any new Azure subscription or any Microsoft Online business services (M365 or Microsoft Intune) subscription.
  - suffiex `onmicrosoft.com`

[manage by Azure CLI `az`](https://github.com/davidkhala/azure-utils/blob/main/cli/entra)

Features

- multi-tenant
  - Within an Azure subscription, you can create multiple Microsoft Entra tenants
  - You can associate the same Microsoft Entra tenant with multiple Azure subscriptions.
- MFA
- Enabling federation between organizations
- self-service password reset
- Extending existing on-premises Active Directory implementations to Microsoft Entra ID
- Configuring Application Proxy for cloud and local applications
- Configuring Conditional Access for users and devices

## Microsoft Entra schema

Diff than AD

- Contains fewer object types
  - No more computer class. Use device class instead
  - No more organizational unit (OU) class. Accomplish equivalent arrangements by organizing objects based on their group membership.
- > The process of joining devices to Microsoft Entra differs considerably from the process of joining computers to AD
  - You cannot use Group Policy Objects (GPOs)
- Represent applications in Microsoft Entra ID.
  - An object in the Application class contains an application definition
  - An object in the servicePrincipal class constitutes its instance in the current Microsoft Entra tenant.
    - Provisioned when you register the corresponding application in that Microsoft Entra tenant
    - define the binding between app and Entra tenant
  - You can define an application in one tenant and use it across multiple tenants by creating a service principal object for this application in each tenant.
