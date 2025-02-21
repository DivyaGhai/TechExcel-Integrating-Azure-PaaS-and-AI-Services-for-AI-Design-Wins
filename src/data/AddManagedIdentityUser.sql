CREATE USER [id-dfz3eae5z7ulu] FROM EXTERNAL PROVIDER;

ALTER ROLE db_datareader ADD MEMBER [id-dfz3eae5z7ulu];
ALTER ROLE db_datawriter ADD MEMBER [id-dfz3eae5z7ulu];