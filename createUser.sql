CREATE USER powerupuser IDENTIFIED BY powerupadmin
TEMPORARY TABLESPACE "TEMP";
ALTER USER powerupuser QUOTA UNLIMITED ON USERS;
GRANT "RESOURCE" TO powerupuser;
GRANT "CONNECT" TO powerupuser;
ALTER USER powerupuser DEFAULT ROLE "RESOURCE","CONNECT";