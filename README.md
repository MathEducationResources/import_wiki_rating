# import_wiki_rating
Python script to import UBC wiki rating to merapp production database

You need the environment variables in `.env` (local db) and/or `prod.env` (production db), as well as the sql dump of the UBC wiki ratings.

Run `make all` to update the corresponding (local or production) mongodb
