"""Estimate the value of Pi with Monte Carlo simulation.
Author:  Ryan Helms
Credits:  TBD
"""
import random
import doctest
import points_plot


GOOD_PI = 3.141592653589793  # A very good estimate, from math.pi
SAMPLES = 42069   # More =>  more precise, but slower


def in_unit_circle(x: float, y: float) -> bool:
    """Returns True if and only if (x,y) lies within the circle
    with origin (0,0) and radius 1.0.
    
    >>> in_unit_circle(0.0, 0.0)
    True
    >>> in_unit_circle(1.0, 1.0) # You were wondering, weren't you?
    False
    >>> in_unit_circle(0.5, -0.5)
    True
    >>> in_unit_circle(-0.9, -0.5)
    False
    """
    if x**2 + y**2 < 1:
        return True
    else:
        return False
    

def  rand_point_unit_sq() -> tuple[float, float]:
    """Returns random x,y both in range 0..1.0, 0..1.0."""
    x = random.random()
    y = random.random()
    return x, y


def plot_random_points(n_points: int = 500):
    """Generate and plot n_points points
    in interval (0,0) to (1,1).
    Creates a window and prompts the user before
    closing it.
    """
    points_plot.init()
    for i in range(n_points):
        x, y = rand_point_unit_sq()
        points_plot.plot(x, y, color_rgb=(50, 50, 50))
    points_plot.wait_to_close()


def relative_error(est: float, expected: float) -> float:
    """Relative error of estimate (est) as non-negative fraction of expected value.
    Note estimate and expected are NOT interchangeable (see test cases).
    For example, if expected value is 5.0 but estimate is 3.0, the
    absolute error is -2.0, but the relative error is 2.0/5.0 = 0.4.
    If the expected value is 3.0 but the estimate is 5.0, the
    absolute error is 2.0, but the relative error is 2.0/3.0 = 0.66.
    >>> round(relative_error(3.0, 5.0), 2)
    0.4
    >>> round(relative_error(5.0, 3.0), 2)
    0.67
    """
    abs_error = est - expected
    rel_error = abs(abs_error / expected)
    return rel_error


def pi_grid_approx(n_rows: int = 100) -> float:
    """Return an estimate of pi by plotting points on a grid, then comparing the
    number inside the unit circle and outside to estimate the value.
    """
    points_plot.init()
    x, y = 0, 0
    pts_inside = 0
    total_pts = 0

    for i in range(n_rows):
        for i in range(n_rows):
            total_pts = total_pts + 1
            x, y = x + 1/n_rows, y
            if in_unit_circle(x, y) and x <= 1.0:
                points_plot.plot(x, y, color_rgb=(255, 10, 10)) ## Red
                pts_inside = pts_inside + 1
            elif x <= 1.0:
                points_plot.plot(x, y, color_rgb=(240, 240, 240)) ## Light grey
        x, y = 0, y + 1/n_rows
            
    return (pts_inside/total_pts)*4


def pi_approx(error_bound: float = 0.01) -> float:
    """Return an estimate of pi by sampling random points.
    >>> relative_error(pi_approx(0.01), GOOD_PI) <= 0.01 
    True
    """
    good_est = False
    total_pts1 = 0
    pts_inside1 = 0
    total_pts2 = 0
    pts_inside2 = 0
    est1 = 1
    est2 = 1
    
    while good_est == False:
        x1, y1 = rand_point_unit_sq()
        x2, y2 = rand_point_unit_sq()
        total_pts1 = total_pts1 + 1
        total_pts2 = total_pts2 + 1
        
        if in_unit_circle(x1, y1): 
            pts_inside1 = pts_inside1 + 1
            if total_pts1 <= 10000:
                points_plot.plot(x1, y1, color_rgb=(255, 10, 10)) ## Red
        elif total_pts1 <= 10000:
            points_plot.plot(x1, y1, color_rgb=(240, 240, 240)) ## Light grey
            
        if in_unit_circle(x2, y2):
            pts_inside2 = pts_inside2 + 1

        if pts_inside1 > 0 and pts_inside2 > 0:
            est1 = (pts_inside1/total_pts1) * 4
            est2 = (pts_inside2/total_pts2) * 4

        if relative_error(est1, est2) <= error_bound * .05 and relative_error(est2, est1) <= error_bound * .05 and total_pts1 >= 4250:
            good_est = True
            
    return (est1 + est2)/2
    

def main():
    doctest.testmod()
    #plot_random_points() # Eyeball test
    points_plot.init() # Enables plotting
    estimate = pi_approx(0.01)
    print(f"Pi estimated using a series of random points is approximately {estimate}")
    points_plot.wait_to_close()
    n_rows = 100
    grid_est = pi_grid_approx(n_rows)
    print(f"Pi estimated using a {n_rows} by {n_rows} grid is approximately {grid_est}")
    points_plot.wait_to_close()

if __name__ == "__main__":
    main()
    
