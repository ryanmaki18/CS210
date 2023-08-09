"""
Enrollment analysis:  Summary report of majors enrolled in a class.
CS 210 project, Fall 2022.
Author:  Ryan Maki
Credits: Help Hours (like 4 times all different LAs)
"""


import doctest
import csv


def read_csv_column(path: str, field: str) -> list[str]:
    """
    Read one column from a CSV file with headers into a list of strings.

    >>> read_csv_column("data/test_roster.csv", "Major")
    ['DSCI', 'CIS', 'BADM', 'BIC', 'CIS', 'GSS']
    
    """
    with open (path, "r", newline="") as the_file:
        reader = csv.DictReader(the_file)
        column_info = []
        for row in reader:
            key_field = row["Major"]
            column_info.append(key_field)
        return column_info
    

def counts(column: list[str]) -> dict[str, int]:
    """
    Returns a dict with counts of elements in column.
    >>> counts(["dog", "cat", "cat", "rabbit", "dog"])
    {'dog': 2, 'cat': 2, 'rabbit': 1}
    
    """
    counts = {}
    for key in column:
        if key in counts:
            #adding one to the count if found
            counts[key] += 1
        else:
            #first time we found this one
            counts[key] = 1
    return counts


def read_csv_dict(path: str, key_field: str, value_field: str) -> dict[str, dict]:
    """
    Read a CSV with column headers into a dict with selected
    key and value fields.

    >>> read_csv_dict("data/test_programs.csv", key_field="Code", value_field="Program Name")
    {'ABAO': 'Applied Behavior Analysis', 'ACTG': 'Accounting', 'ADBR': 'Advertising and Brand Responsibility'}

    """
    with open (path, "r", newline="") as the_file:
        reader = csv.DictReader(the_file)
        key_count = {}
        for row in reader:
            key_field = row["Code"]
            val_field = row["Program Name"]
            key_count [key_field] = val_field
        return key_count


def items_v_k(v_k: dict[int, str]) -> list[tuple]:
    tuple_list = []
    for key, value in v_k.items():
        temp_tuple = (value, key)
        tuple_list.append(temp_tuple)
    return sorted(tuple_list)


def main():
    doctest.testmod()
    majors = read_csv_column("data/roster_selected.csv", "Major")
    counts_by_major = counts(majors)
    program_names = read_csv_dict("data/programs.csv", "Code", "Program Name")
    # --- Next line replaces several statements
    by_count = items_v_k(counts_by_major)
    # ---  
    by_count.sort(reverse=True)  # From largest to smallest
    for count, code in by_count:
        program = program_names[code]
        print(count, program)


if __name__ == "__main__":
    main()
