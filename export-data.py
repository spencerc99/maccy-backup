#!/Users/spencerchang/anaconda/bin/python3
# NOTE: you should make the above path wherever your python3 is
import sqlite3
from datetime import datetime
import os

now = datetime.now()
home_directory = os.path.expanduser('~')
# TODO: support customizing this path
filepath = f'{home_directory}/Library/Containers/org.p0deje.Maccy/Data/Library/Application Support/Maccy/Storage.sqlite'

# Setup sqlite connection to the database
conn = sqlite3.connect(filepath)
cur = conn.cursor()

# Ignore image data types for now
CONTENT_TYPES_TO_IGNORE = [
    'public.png',
    'public.rtf',
    'public.tiff',
    'org.chromium.web-custom-data',
]

def main():
    # Setup sqlite connection to the database
    conn = sqlite3.connect(filepath, detect_types=sqlite3.PARSE_DECLTYPES |
                                                            sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()

    # Try to get last id we exported
    last_id = None
    try: 
        with open('last-export', 'r') as last_export:
            last_id = int(last_export.readline().strip())
    except Exception as e:
        pass

    print(f"Looking for entries to export starting after {last_id}...")
    export_script = f'''
    SELECT
        Z_PK AS id,
        ZTYPE AS type,
        ZVALUE AS value
    FROM
        ZHISTORYITEMCONTENT
    WHERE
        {'TRUE' if last_id is None else f"Z_PK > {last_id}"} AND
        ZTYPE NOT IN ({', '.join(f"'{ct}'" for ct in CONTENT_TYPES_TO_IGNORE)})
    ORDER BY
        Z_PK ASC;
    '''

    new_rows = cur.execute(export_script)
    # Support datetime if the sync is quicker than daily by adding %H:%M:%S to the date string
    today_str = now.strftime("%Y-%m-%d")

    print("Beginning export..")
    with open('export.csv', 'a') as f:
        row = None
        for i, row in enumerate(new_rows):
            # Data Schema
            # date,id,type,value
            # 2021-02-20 00:00:00,123,public.utf8-plain-text,hello world copy paste content, with commas too!
            f.write(f'{today_str},{row[0]},{row[1]},{row[2]}\n')

        if not row:
            print("No new data to export")
            return

        print(f"Successfully exported {i} new entries")
        # Update last export id
        with open('last-export', 'w') as last_export:
            last_export.write(str(row[0]))
            print(f"Updated last export id to {row[0]}")


if __name__ == '__main__':
    main()
