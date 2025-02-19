Describe "cli.exe"{
    BeforeAll{
        $cliPath = "./dist/cli.exe"
    }
    It "cli.exe should exists" {
        Test-Path -Path $cliPath | Should -Be $true
    }
    #DATABRICKS_HOST: adb-2367537008441771.11.azuredatabricks.net
    #TENANT_ID: 54b02cc9-5a7b-42a5-9476-a4f0d3ab0460
    #CLIENT_ID: 6195f590-fbd0-461e-be86-ac63d78e447d
    It "rename"{
        & $cliPath `
            --entra.tenant-id="$env:TENANT_ID" `
            --entra.client-id="$env:CLIENT_ID" `
            --entra.client-secret="$env:CLIENT_SECRET" `
            rename `
            --databricks.host="$env:DATABRICKS_HOST" `
            --databricks.token="$env:DATABRICKS_TOKEN" `
            | Write-Host

    }
    It "lineage"{
        & $cliPath `
            --entra.tenant-id="$env:TENANT_ID" --entra.client-id="$env:CLIENT_ID" `
            --entra.client-secret="$env:CLIENT_SECRET" `
            lineage desktop --dataset="nyctlc" | Write-Host

    }

}
