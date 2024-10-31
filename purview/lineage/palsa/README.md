# [Purview-ADB-Lineage-Solution-Accelerator (PALSA)](https://github.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator)

```

git clone https://github.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator.git
cd ./Purview-ADB-Lineage-Solution-Accelerator/deployment/infra/
rm ./settings.sh
curl https://raw.githubusercontent.com/davidkhala/Microsoft/refs/heads/main/purview/lineage/palsa/demo-context.sh | bash
chmod +x openlineage-deployment.sh
./openlineage-deployment.sh
cd -
```
