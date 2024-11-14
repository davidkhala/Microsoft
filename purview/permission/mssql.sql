-- A good SQL runtime is **Query Editor** in Azure SQL DB db level

-- Create

CREATE USER "[SAMI name]" FROM EXTERNAL PROVIDER
GO

EXEC sp_addrolemember 'db_owner', "[SAMI name]"
GO

CREATE MASTER KEY
GO

-- Cleanup  
--  by Transact-SQL syntax
DECLARE @SAMI VARCHAR(20);
SET @SAMI = 'admin-david'
DECLARE @name VARCHAR(91);

SELECT @name = name 
	FROM sys.database_scoped_credentials 
	WHERE principal_id = USER_ID(@SAMI);

-- TODO syntax error
DROP DATABASE SCOPED CREDENTIAL @name
-- TODO syntax error
DROP USER @SAMI
