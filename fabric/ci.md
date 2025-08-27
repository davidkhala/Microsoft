# *Git* fashion
workspace connect with Git branch
- for finer-control, it is optional to point to folder level

## Best practice
- develop in an isolated workspace, outside of a shared (production) workspace
  - connect to dedicated (feat) branches instead of main code branch
# *Fabric deployment pipelines* fashion

deploy your Fabric items across different stages
- you need to assign workspace to stage
- The deployment process lets you clone content from one stage in the pipeline to another
  - At least one item must be selected
- **Conflict with GitOps**: if you had Git integration on workspace of next stage, the newly cloned content is considered as uncommitted changes in **Source Control** pane

## Stages
- Default stages: Development | Test | Production
- 2-10 stages in a deployment pipeline

## [Item pairing](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/assign-pipeline?tabs=new-ui#item-pairing)
The process by which an item in one stage of the deployment pipeline is associated with the same item in the adjacent stage
- It occurs when you 
  - assign a workspace to a deployment stage, or
  - **clean deploy**: deploy new unpaired content from one stage to another

### case: clean deploy
- **No pair no overwrite**: If items aren't paired, they don't overwrite on deployment
  - even if they appear to be the same (have the same name, type, and folder)
  - Instead, a duplicate copy is created and paired with the item in the previous stage.
  - **Magic: same name coexist** The duplicate copy can have the same name as the unpaired item
- **overwrite the paired**: upon deploy, the items being copied from the source stage overwrite the paired item in the target stage
- **Immutable**: Items that are paired remain paired after renaming
  - Therefore, paired items can have different names.
### case: assign to stage
pairing criteria: Item Name, Item Type & Folder Location
- **Folder Location as tie breaker**: if Item Name & Type are same but Folder Location are not, **pairing fails**

## Copy
Limit
- [list of Supported items](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines?tabs=new-ui#supported-items)
- [properties aren't copied during deployment](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/understand-the-deployment-process?tabs=new-ui#item-properties-that-are-not-copied)
  - Data: only metadata is copied
  - URL
  - ID
  - Workspace settings: including Permissions
  - Personal bookmarks
  - powerbi
    - App content and settings: [how to update](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/understand-the-deployment-process?tabs=new-ui#update-content-to-power-bi-apps)
    - semantic model properties
      - Role assignment
      - **Refresh schedule**
      - Data source credentials
      - Query caching settings (can be inherited from the capacity)
      - Endorsement settings