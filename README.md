# Python SCD ETL Spike
A python example of reading and processing excel files into SCD table

![image](https://user-images.githubusercontent.com/2478826/195193457-017be171-4451-40d8-84de-b85df3678fc7.png)

DOR
- Is it necessary to batchbreading of file for large files?
- Is there a need to customize the validity period e.g. 30 days?

Completed
- [X] Read excel into type accurate class
- [X] Automate setup (requirements.txt)

Do Next
- [ ] Add Data Access with SQLAlchemy & SQLLite
- [ ] Add SCD Type 2 for MasterRecord insert latest
- [ ] Soft delete a previously inserted batch entries (Re link SCD chain)
- [ ] Update existing SCD chain with historic data (a) Replace placeholder (b) More granular
- [ ] Fail if start date already exist (First remove can't have duplicates)
- [ ] Unit testing
- [ ] Monitor (Asyncio) and process files in seperate threads up to X
- [ ] Monitor (Asyncio) for batches that are ready and process them in seperate thread up to x
- [ ] Before SCD batch processing run client cleanup (a) items that has missing submissions for client gets placeholder (b) items that was missing in previous submissions amounts are zero's

Backlog
- [ ] Block processing of files that was already processed
- [ ] Process completed batches into SCD type 2 table
- [ ] Archive file when completed
- [ ] Report on error and bubble up details
- [ ] Move the local file path to a remote SFTP path
- [ ] Add Success and failure totals on batch (Threadsafe updates)

