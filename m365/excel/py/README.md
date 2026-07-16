# Excel

.xlsx 本质上是一个 zip 压缩包，里面的 `xl/worksheets/sheet1.xml` 才是真正的数据

- 绝大多数工具在zip文件下载好之前，都不能处理
    - 文件必须完整到达后才能开始读行。整个文件的字节数据还是会存在 BytesIO 里。

如果需要公式字符串：使用 pip openpyxl
- read_only=True, data_only=False

只需要公式计算结果值，追求速度：使用 pip calamine
- 已经用 pandas 做数据处理 → pd.read_excel(..., engine="calamine")
