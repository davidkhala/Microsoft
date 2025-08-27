# Security model

3 security levels to be evaluated sequentially to determine data access

## 1. Microsoft Entra ID authentication

## 2. Fabric access

## 3. Data security

build blocks

- Workspace roles
- Item permissions
  - Item in Lakehouse | Warehouse | Semantic model
  - permission type: (`Read` | `ReadData`|`R`)
- Compute or granular permissions
  - compute engine like SQL Endpoint | Semantic model
- OneLake data access controls (a RBAC)
  - targeting files or folders
