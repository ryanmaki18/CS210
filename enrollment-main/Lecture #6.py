### October 13, 2022 -- Thursday @ 10:00 AM
### Live Code Demo

"""Demonstrate dictreader for theatre database"""
import csv

THEATERS = "/Users/ryanmaki/Documents/temp/theaters.csv"

def extract_table(path:str, keys: list[str]) -> list[str]:
    """
    Returns a list )rows) of lists (columns),with columns corresponding
    to keys as column-headers in the CSV file.
    """
    result = [keys]
    with open(path, newline="") as csv_file:
        table_reader = csv.DictReader(csv_file)
        for row in table_reader:    
            result_row = []
            for key in keys:
                result_row.append(row[key])
            result.append(result_row)
    print(result)


def main():
    keys = ["Theater name", "City"]
    tbl = extract_table (THEATERS, keys)
#    print(keys)
#    for row in tbl:
#        print(row)

if __name__ == "__main__":
    main()
    
