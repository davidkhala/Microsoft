# Service Principal

User created Service Principal is found in Microsoft Entra > `Applications` > `App registrations`

## System-assigned Managed Identity (SAMI)
- SAMI is a type of Service Principal??
- aka. 托管标识, Azure Managed Service Identity (MSI)
- It is listed in Microsoft Entra > `Applications` > `Enterprise applications`

Grant access to resource such as Azure Subscription 
1. In each resource, go the left panel `Access Control (IAM)`
2. Click [+ Add v] above the main widget to open drop down menu. Then click [Add role assignment]
3. Select a **Role** and click [Next]
   - **Recommend**: `Contributor` role under `Privileged administrator roles`
4. Choose **O Managed identity** and click <ins>Select members</ins>
5. Choose your Subscription, Managed identity and **Select** to choose **Selected members**, then click [Select]
6. Click [Review + assign]