$ErrorActionPreference = "Stop"
function Pause
{
    param(
        [string]$name,
        [string]$resourceGroup
    )
    if ( [string]::IsNullOrEmpty($resourceGroup))
    {
        $resourceGroup = Get-ResourceGroup
    }
    az fabric capacity suspend --capacity-name=$name --resource-group=$resourceGroup
}

function List
{
    az fabric capacity list
}
function Get-ResourceGroup
{
    az fabric capacity list --query "[?name=='payg'].resourceGroup | [0]"
}
function Resume
{
    param(
        [string]$name,
        [string]$resourceGroup
    )
    if ( [string]::IsNullOrEmpty($resourceGroup))
    {
        $resourceGroup = Get-ResourceGroup
    }

    az fabric capacity resume --capacity-name=$name --resource-group=$resourceGroup
}

if ($args.Count -gt 0)
{
    Invoke-Expression ($args -join " ")
}
