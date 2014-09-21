ohlife-replacement
==================

ohlife was an email-based diary thing that shutdown in October 2014. This aims to do basically the same thing.

Make a sqlite3 database called db.db with one table:

```sql
create table entries (day date primary key, entry text);
```
