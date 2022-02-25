# Maccy Backup
This project is intended to provide an easy way to automatically back up your [Maccy](https://maccy.app/) database of copy + pastes. It produces a CSV of the clipboard data from Maccy and supports regular exporting of this data to view your clipboard history over time. You can see a sample CSV export in `example-export.csv`

# Context
Maccy is an incredibly useful app that keeps track of recent clipboard history, but by default it keeps the last 200 entries. You can raise this limit arbitrarily high because it is open-source (❤️), but you probably don't want to surface all of these when searching in your daily use of Maccy given how noisy the data is. Most copy and paste data naturally should be ephemeral and the beauty of Maccy is giving you access and control over the recent entries.

However, it can be fun and useful to look back over months and years at what kinds of things you were focusing on copying. Imagine being able to open a time capsule of your copy clipboard from a few years ago. What would it reveal your time and attention was focused on? For this fun reason, I developed this small utility to periodically backup your clipboard content from Maccy to a lightweight CSV.

# Setup
To run the export, clone this repo and run the following command:
```bash
python export-data.py
```

You will see some content indicating your successful export:
```bash
Looking for entries to export starting after None...
Beginning export..
Successfully exported 463 new entries
Updated last export id to 12755
```

This will export into a `export.csv` with the following data format:
```
date,id,type,value
```
For example, a sample row might look like:
`2021-02-20,123,public.utf8-plain-text,hello world copy paste content, with commas too!`
* Note that the date will correspond to when you run the export and not when the content was copied at for now—looking into grabbing that from Maccy.
* Also note that if you want to parse this data later, the final column may have commas in it because it's the clipboard content. Intentionally left this at the end so you can parse the rest of the line into the value and not get confused with the comma separator.

At this point, you could stop if you want to manually maintain this export or just do a one-time export.

## Automated Export
To make it automated, I've provided a simple cron job template for you to use under `cronjob.template` which runs this script every 10 minutes. Create a new file called `cronjob` and fill the template in. You can test the logic of your cronjob using this site https://crontab.guru/. 

If you're on Mac, I ran into folder permissioning issues, which you'll need to resolve by following [this thread](https://apple.stackexchange.com/questions/378553/crontab-operation-not-permitted).

After that, you can run `install-cronjob.sh` in order to add it to your list of cron jobs.

NOTE: cron jobs are unfortunately brittle and will not run if your computer is not open and on at the time specified. 

TODO:
1. setup cron job to auto-backup every X (like roam export)
2. make sure can upload to github

# Functionality Details
This assumes a standard Mac setup with Maccy and also ignores any image content (but this ignore list is probably incomplete) to focus on preserving a history of text data to be lightweight.

# Final Notes

This is a very simple tool for own workflow, so I won't be planning on any regular updates. That said, feel free to make issues and add pull requests for features you'd like.

Ideally, this would support
* pulling the last copied date for the content from Maccy's database itself, have an [issue](https://github.com/p0deje/Maccy/issues/375) open to explore this
* Upload the `export.csv` github/icloud/other cloud provider
* maybe do a sqlite export instead of CSV? just did csv for now because its plain text for you to read and search and easy to parse and accessible but not as easy to manipulate bulk data as sql.
