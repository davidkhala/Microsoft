DECLARE @SAMI VARCHAR(MAX);
SET @SAMI = 'admin-david';
DECLARE @sql NVARCHAR(MAX);

SET @sql = 'CREATE USER ' + @SAMI + ' FROM EXTERNAL PROVIDER;';
EXEC sp_executesql @sql;

EXEC sp_addrolemember 'db_owner', @SAMI

CREATE MASTER KEY
GO



