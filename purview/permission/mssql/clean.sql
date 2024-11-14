DECLARE @SAMI VARCHAR(20);
SET @SAMI = 'admin-david'
DECLARE @name VARCHAR(91);

SELECT @name = name
	FROM sys.database_scoped_credentials
	WHERE principal_id = USER_ID(@SAMI);

DECLARE @sql NVARCHAR(MAX);

SET @sql = 'DROP DATABASE SCOPED CREDENTIAL [' + @name + ']';
EXEC sp_executesql @sql;

SET @sql = 'DROP USER [' + @SAMI + ']';
EXEC sp_executesql @sql;