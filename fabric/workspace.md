# Fabric workspace
> Workspaces are environments where users can collaborate to create groups of data items

## permission

### Workspace roles
- **Workspace roles** are preconfigured sets of permissions for all items within the workspace as object
  - principals (aka. users) can be either individuals, security groups, Microsoft 365 groups, or distribution lists
  - types:
    - `Admin`
    - `Member`: `Contributor` + share permission + Add members or others with lower permissions.
    - `Contributor`
    - `Viewer`

### Item permissions
- **Item permissions** control access to individual Fabric items
  - **at least lakehouse metadata read**: if you add the user and don't select any of the checkboxes under Additional permissions, the user will have read access to the lakehouse metadata

## License
In the Workspace settings, you can configure the license type to use Fabric features
- Default License mode: `Pro`
