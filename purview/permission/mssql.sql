-- A good SQL runtime is **Query Editor** in Azure SQL DB db level

-- Create

CREATE USER "[SAMI name]" FROM EXTERNAL PROVIDER
GO

EXEC sp_addrolemember 'db_owner', "[SAMI name]"
GO

CREATE MASTER KEY
GO

-- Cleanup  

SELECT name, credential_identity 
FROM sys.database_scoped_credentials 
WHERE principal_id = USER_ID('[SAMI name]'); -- Identify the Credentials

DROP DATABASE SCOPED CREDENTIAL [YourCredentialName];

DROP USER "[SAMI name]";
