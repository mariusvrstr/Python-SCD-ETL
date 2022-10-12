# Python SCD ETL Spike
A python example of reading and processing excel files into SCD table

### Conceptual Architecture
![image](https://user-images.githubusercontent.com/2478826/195299688-09855829-7808-4350-bc63-40f1a02c776d.png)

### ERD Diagram
![image](https://user-images.githubusercontent.com/2478826/195299375-ce7858c0-0f7c-4612-9eda-1556847bef46.png)

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
- Is it necessary to batchbreading of file for large files?
- Is there a need to customize the validity period e.g. 30 days?

## Backlog

### Completed
- [X] Read excel into type accurate class
- [X] Automate setup (requirements.txt)
- [X] Add Data Access with SQLAlchemy & SQLLite
- [X] Read excel data into a batched staging
- [X] Archive file when completed
- [X] Block processing of files that was already processed

### Do Nex
- [ ] Add SCD Type 2 for MasterRecord insert latest
- [ ] Soft delete a previously inserted batch entries (Re link SCD chain)
- [ ] Update existing SCD chain with historic data (a) Replace placeholder (b) More granular
- [ ] Fail if start date already exist (First remove can't have duplicates)
- [ ] Unit testing
- [ ] Monitor (Asyncio) and process files in seperate threads up to X
- [ ] Monitor (Asyncio) for batches that are ready and process them in seperate thread up to x
- [ ] Before SCD batch processing run client cleanup (a) items that has missing submissions for client gets placeholder (b) items that was missing in previous submissions amounts are zero's

### Backlog
- [ ] Keep transactions on item level and skip update if current batch reference <> current batch (Re-Run batch without re processing)
- [ ] Process completed batches into SCD type 2 table
- [ ] Report on error and bubble up details
- [ ] Move the local file path to a remote SFTP path
- [ ] Add Success and failure totals on batch (Threadsafe updates)

