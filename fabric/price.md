# [trial](https://learn.microsoft.com/zh-cn/fabric/get-started/fabric-trial)
- Fabric 试用版的有效期为 60 天
- 其中包括 Power BI 个人试用版（如果你还没有 Power BI 付费许可证）和一个 Fabric 试用版容量。

# SKU
https://learn.microsoft.com/en-us/power-bi/developer/embedded/embedded-capacity#sku-computing-power
- A: Power BI Embedded
- EM/P: Power BI Premium

Saving options
- PAYG: [Delete a capacity](https://learn.microsoft.com/en-us/fabric/admin/capacity-settings?tabs=fabric-capacity#delete-a-capacity)
  - > non-Power BI Fabric items in workspaces assigned to the capacity are soft deleted
    - > These Fabric items can still be seen in Onelake Data Hub and in the workspace list, but can't be opened or used.
    - Restore: If the workspace that holds these items is associated to a capacity from the **same region** as the deleted capacity **within seven days**, the deleted items are restored.
  - Delete "Power BI Embedded" capcity will hard delete Fabric items in associated workspace
  
