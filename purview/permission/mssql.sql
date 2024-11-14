-- A good SQL runtime is **Query Editor** in Azure SQL DB db level

-- Create
DECLARE @SAMI VARCHAR(20);
SET @SAMI = 'admin-david'
CREATE USER "[SAMI name]" FROM EXTERNAL PROVIDER

EXEC sp_addrolemember 'db_owner', "[SAMI name]"

CREATE MASTER KEY
GO

-- Cleanup  
-- Step 0. in SSMS, go to `Databases` > [database] > `Extended Events` > `Sessions` > stop and delete Purview sessions first
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

