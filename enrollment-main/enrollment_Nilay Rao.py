"""Enrollment analysis:  Summary report of majors enrolled in a class.
CS 210 project, Fall 2022.
Author:  Nilay Rao
Credits: TBD
"""
import doctest
import csv


def read_csv_column(path: str, field: str) -> list[str]:
    """Read one column from a CSV file with headers into a list of strings.

    >>> read_csv_column("data/test_roster.csv", "Major")
    ['DSCI', 'CIS', 'BADM', 'BIC', 'CIS', 'GSS']
    """
    
    with open('data/test_roster.csv', newline='') as csvfile:
     data = csv.DictReader(csvfile)
     majors = []
     for row in data:
       majors.append(row[field])
    return (majors)



def counts(column: list[str]) -> dict[str, int]:
    """Returns a dict with counts of elements in column.

    >>> counts(["dog", "cat", "cat", "rabbit", "dog"])
    {'dog': 2, 'cat': 2, 'rabbit': 1}
    """
    
    count = {}
   
    for i in column:
        count[i] = count.get(i, 0) + 1
    return count

def read_csv_dict(path: str, key_field: str, value_field: str) -> dict[str, dict]:
    """Read a CSV with column headers into a dict with selected
    key and value fields.

    >>> read_csv_dict("data/test_programs.csv", key_field="Code", value_field="Program Name")
    {'ABAO': 'Applied Behavior Analysis', 'ACTG': 'Accounting', 'ADBR': 'Advertising and Brand Responsibility'}
    """
    
    with open('data/test_programs.csv', newline='') as csvfile:
        data = csv.DictReader(csvfile)
        code = {}
        keys = []
        items = []
        for row in data:
            keys.append(row[key_field])
            items.append(row[value_field])
            
        code = dict(zip(keys,items))
        
    return (code)

    




def main():
    doctest.testmod()
    majors = read_csv_column("data/roster_selected.csv", "Major")
    
    counts_by_major = counts(majors)
    program_names = read_csv_dict("data/programs.csv", "Code", "Program Name")
    
    for code, count in counts_by_major.items():
        program = program_names[code]
        print(count, program)


if __name__ == "__main__":
    main()
    doctest.testmod()
    print("Tests ran!")

###                   Prof Example
# result =[keys]
# with open(path, newline='') as csvfile:
#     table_reader = csv.DictReader(csvfile)
#     for row in table_reader:
#        print(row['Theater name'], row['City'])
#        result.append([row['Theater name'], row['City']])
