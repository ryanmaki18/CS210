"""Summarize a path in a map, using the standard Ramer-Douglas-Peucher (aka Duda-Hart)
split-and-merge algorithm.
Author: Ryan Maki
Credits: TBD
"""

import csv
import doctest

import geometry
import map_view
import config

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def read_points(path: str) -> list[tuple[float, float]]:
    """
    Read the CSV file into a list of (easting, northing) tuples filled with
    floats (they are distance calculations).
    """
    with open(path, newline="", encoding="utf-8") as source_file: 
        reader = csv.DictReader(source_file)        
        location = []
        for row in reader:                      # function from wildfire.py
            easting = float(row["Easting"])
            northing = float(row["Northing"])
            location.append((easting, northing))
        return location


def summarize(points: list[tuple[float, float]],
              tolerance: int = config.TOLERANCE_METERS
              ) -> list[tuple[float, float]]:
    """
    >>> path = [(0,0), (1,1), (2,2), (2,3), (2,4), (3,4), (4,4)]
    >>> expect = [(0,0), (2,2), (2,4), (4,4)]
    >>> simple = summarize(path, tolerance=0.5)
    >>> simple == expect
    True
    """
    summary: list[tuple[float, float]] = [points[0]]
    epsilon = float(tolerance * tolerance)

    def simplify(start: int, end: int):
        """Add necessary points in (start, end] to summary."""
        log.debug(f"Simplifying from {start}: {points[start]} to {end}: {points[end]}, {points[start+1:end]}")
        log.debug(f"Summary so far: {summary}")
        if end - start < 2:
            summary.append(points[end])
            return
        else:
            map_view.scratch(points[start], points[end])
            max_dev = 0
            max_dev_index = start
            for point in range(start + 1, end):
                curr_dev = geometry.deviation_sq(points[start], points[end], points[point])
                if curr_dev > max_dev:
                    max_dev_index = point
                    max_dev = curr_dev
            if max_dev > epsilon:
                simplify(start, max_dev_index)
                simplify(max_dev_index, end)
            else:
                summary.append(points[end])
                map_view.plot_to(points[end])
        return

    simplify(0, len(points)-1)
    map_view.clean_scratches()
    return summary


def main():
    points = read_points(config.UTM_CSV)
    map_view.init()
#    for point in points:
#        map_view.plot_to(point)
    print(f"{len(points)} raw points")
    summary = summarize(points, config.TOLERANCE_METERS)
    print(f"{len(summary)} points in summary")
    map_view.wait_to_close()
    

if __name__ == "__main__":
    doctest.testmod()
    print("Tested")
    main()
