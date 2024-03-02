#!/bin/bash

db_name=database
pathB=/backups
find $pathB \( -name "*-1[^5].*" -o -name "*-[023]?.*" \) -ctime +61 -delete
pg_dump $db_name | gzip > /backups/db_backup_$(date "+%Y-%m-%d").sql.gz
