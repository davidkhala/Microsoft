
# Install
```
npm install -g yo @microsoft/generator-sharepoint
yo @microsoft/sharepoint
```

## Option: Application Customizer
> Which type of client-side component to create?
- Extension -> Application Customizer

找到文件`.\src\extensions\appCustomizer\AppCustomizerApplicationCustomizer.ts`，然后在 `onInit()` 方法中写入注入代码
```TODO validate
const head = document.getElementsByTagName("head")[0];
const style = document.createElement("link");
style.rel = "stylesheet";
style.href = "/sites/YourSite/SiteAssets/custom.css";
head.appendChild(style);
```



Build: 打包并部署到 App Catalog：
1. 使用 `gulp bundle --ship` 和 `gulp package-solution --ship`
2. 上传 .sppkg 文件到 App Catalog 并部署