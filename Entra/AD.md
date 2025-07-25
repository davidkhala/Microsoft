https://learn.microsoft.com/en-us/windows-server/identity/active-directory-federation-services

# Active Directory
- It runs as a service on Windows Server, referred to as a domain controller.


## AD Domain Services (AD DS)
- aka. AD
- A true directory service, with a hierarchical X.500-based structure.
- Uses Domain Name System (DNS) for locating resources such as domain controllers.
- You can query and manage AD DS by using LDAP calls.
- AD DS primarily uses the Kerberos protocol for authentication.
- uses OUs and GPOs for management.
- computer objects
  - representing computers that join an Active Directory domain.
- AD DS uses trusts between domains for delegated management.

Deploy on Azure
- Deploying AD DS on an Azure virtual machine requires one extra Azure data disk
- because you shouldn't use drive C for AD DS storage.
- These disks are needed to store the AD DS database, logs, and the sysvol folder.
- The Host Cache Preference setting for these disks must be set to None.


## AD Certificate Services (AD CS)

## AD Rights Management Services (AD RMS)

## AD Lightweight Directory Services (AD LDS)

## AD Federation Services (AD FS)

