Describe "cli.exe"{
    $cliPath = "./dist/cli.exe"
    It "cli.exe should exists" {
        Test-Path -Path $cliPath | Should Be $true
    }
    It "rename"{
        & $cliPath `
            --entra.tenant-id="54b02cc9-5a7b-42a5-9476-a4f0d3ab0460" `
            --entra.client-id="6195f590-fbd0-461e-be86-ac63d78e447d" `
            --entra.client-secret="$env:CLIENT_SECRET" `
            rename `
            --databricks.host="adb-2367537008441771.11.azuredatabricks.net" `
            --databricks.token="$env:DATABRICKS_TOKEN" `

    }
    It "lineage"{
        & $cliPath `
            --entra.tenant-id="54b02cc9-5a7b-42a5-9476-a4f0d3ab0460" `
            --entra.client-id="6195f590-fbd0-461e-be86-ac63d78e447d" `
            --entra.client-secret="$env:CLIENT_SECRET" `
            --dataset=nyctlc
        lineage desktop

    }

}
