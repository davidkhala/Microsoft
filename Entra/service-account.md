# System-assigned Managed Identity (SAMI)
- SAMI works like a service account.

grant access to resource
1. In each resource, go the left panel `Access Control (IAM)`
2. Click [+ Add v] above the main widget to open drop down menu. Then click [Add role assignment]
3. Select a **Role** and click [Next]
   - **Recommend**: `Contributor` role under `Privileged administrator roles`
4. Choose **O Managed identity** and click <ins>Select members</ins>
5. Choose your Subscription, Managed identity and **Select** to choose **Selected members**, then click [Select]
6. Click [Review + assign]
