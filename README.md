# Python SCD ETL Spike
A python example of reading and processing excel files into SCD table

### Conceptual Architecture

<img src="https://user-images.githubusercontent.com/2478826/195299688-09855829-7808-4350-bc63-40f1a02c776d.png" width="600" />

### Overview
File Template

![image](https://user-images.githubusercontent.com/2478826/195708755-a099193e-3317-4b38-9500-2d7b61b5f801.png)

ERD Diagram

![image](https://user-images.githubusercontent.com/2478826/195708826-c7a89885-7ace-45be-a4db-88c10abbf839.png)

## Setup

## Python Project
1. Run the "setup.ps1" powershell script to create local virtual environment and install dependancies

## Execute
1. Copy sample files from "../etl/sample_files/*.xlsx" into root "../etl/"
2. Run main.py

## View PlantUML Documentation
This is optional to view the [documentation](https://github.com/mariusvrstr/Python-SCD-ETL/tree/main/docs), not needed to run the solution.
1. Install [Java Runtime](https://www.java.com/download/ie_manual.jsp)
2. Install [Graphviz](https://graphviz.org/#what-is-graphviz)
3. Install the [PlantUML VSCode Extention](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml)
4. Open the *.puml file and press Alt+D to preview

## Things to unpack
- Is it necessary to batch reading of file for large files?
- Is there a need to customize the validity period e.g. 30 days?

## Backlog

### General Backlog
- [X] Automate setup (requirements.txt)
- [X] Add Data Access with SQLAlchemy & SQLLite
- [ ] Unit testing with transaction rollback
- [ ] Monitor (Asyncio) and process files in seperate threads up to X
- [ ] Monitor (Asyncio) for batches that are ready and process them in seperate thread up to x
- [ ] Move the local file path to a remote SFTP path (Run from a cloud service without access to local HDD)

## SCD Type 2 Backlog
- [X] Append new (latest) item to en of SCD chain 
- [ ] Soft delete one/batch of existing records in the SCD chain
- [ ] Insert new SCD record in between 2 existing entries
- [ ] Before item level SCD run client cleanup (a) items that has missing submissions for client gets placeholder (b) items that was missing in previous submissions amounts are zero's
- [ ] Replace existing placeholder record if new insert covers 80% or more of the placeholder duration

## Resiliance and Error Backlog
- [X] Minor errors should optionally be able to allow to proceed
- [X] Block processing of files that was already processed
- [X] Must be able to continue processing of a file or batch if it was interupted without re-processing all entries (service was restarted while it was busy)
- [X] Must be able to re-run a batch that previously failed
- [ ] From (date) get me X instances every day/month
- [ ] Report on error and bubble up details
- [ ] Add Success and failure totals on batch (Threadsafe updates)

## ETL and Reporting Backlog
- [X] Read excel into type accurate class
- [X] Read excel data into a batched staging
- [X] Archive file when completed
- [X] Fail if start date already exist (First remove can't have duplicates)
- [ ] Check client account that the chain is healthy (a) instances are not longer than X from each other and that (b) there are no missing chains from the first to last entry
- [X] Add stage item process_status, for batches in READY status get all pending items x at a time then mark batch as complete 
