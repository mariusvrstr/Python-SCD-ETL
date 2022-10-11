# Python SCD ETL Spike
A python example of reading and processing excel files into SCD table

Backlog
- [ ] Batch read standard excel template
- [ ] Generate file hash and check for existing batched (not deleted)
- [ ] Monitor root ETL folder for new files
- [ ] Block processing of files that was already processed
- [ ] Import file data as a batch into staging
- [ ] Process completed batches into SCD type 2 table
- [ ] Archive file when completed
- [ ] Report on error and bubble up details
- [ ] Move the local file path to a remote SFTP path