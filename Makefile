## help: list all available commands
help: Makefile
	@sed -n 's/##//p' $<

.PHONY: all
.DELETE_ON_ERROR:
.SECONDARY:

## all: Upload votes to production db
all: rating_pid.csv rating_pid_url.csv
	python rating_csv2mongo.py

## clean: Removes all intermediate files
clean:
	rm rating_pid.csv
	rm rating_pid_url.csv

## rating_pid.csv: extracts list of ratings from sql dump
rating_pid.csv: w4grb.sql
	python sql2csv.py

## rating_pid_url.csv: adds url to csv (needs to go online -> takes a while)
rating_pid_url.csv: pid2url.py rating_pid.csv
	python $<
