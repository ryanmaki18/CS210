'''
Uses Monte Carlo to estimate the area of a unit circle.
author: Petraea
credits:

also see credits in points_plot.py.
'''

import random
import doctest
import points_plot


def in_unit_circle(coords:list) -> bool:
    
    if coords[0]**2 + coords[1]**2 <= 1:
        return True
    
    return False


def generate_random_coord_pair(max_x=1, max_y=1, min_x=0, min_y=0) -> list:
    '''Returns random coordinates with the bounds x:[min_x, max_x] y:[min_y, max_y], returns list length 2 of [x, y].'''
    x_coord = random.uniform(min_x, max_x)
    y_coord = random.uniform(min_y, max_y)
    return [x_coord, y_coord]
    print([x_coord, y_coord])

def plot_random_points(no_to_plot:int=500):
    '''Randomly plots 500 points on new window.'''
    points_plot.init()
    for q in range(no_to_plot):
        x, y = generate_random_coord_pair()
        points_plot.plot(x, y, color_rgb=(50,50,50))
    points_plot.wait_to_close()


def estimate_pi(resolution:int=2**8, show_graphics=False, method="riemann_trap") -> float:
    '''estimates pi using one of several methods.
"monte" method uses a Monte Carlo method to estimate pi.
"grid" uses a grid of points, similar to the monte carlo method. recommend setting "resolution" to a number squared.
"riemann" method uses a riemann sum in the first quadrant to estimate pi.
"riemann_trap" uses a riemann sum, but with trapezoids rather than rectangles as "riemann".'''

    assert type(resolution) == int, "resolution for estimate_pi() must be type int."
    assert resolution > 0, "resolution for estimate_pi() must be greater than zero."
    
    if method == "monte":
        # Monte Carlo method
        hits = 0
        if not show_graphics:
            for q in range(resolution):
                new_point = generate_random_coord_pair()
                if in_unit_circle(new_point):
                    hits += 1
                else:
                    pass
        else:
            points_plot.init()
            for q in range(resolution):
                new_point = generate_random_coord_pair()
                if in_unit_circle(new_point):
                    hits += 1
                    color = (255,56,128)
                else:
                    color = (50,50,50)
                points_plot.plot(new_point[0], new_point[1], color_rgb = color)
        
        pi_approximate = (hits / resolution) * 4

    elif method == "grid":
        true_res = int(resolution ** 0.5)
        assert true_res > 1, "resolution for 'grid' method must be greater than 4."
        true_interval = 1/(true_res - 1) # This generates a square grid of true_res^2 points with points at edges of the unit square.
        
        hits = 0
        if not show_graphics:
            for y in range(0, true_res):
                y *= true_interval
                for x in range(0, true_res):
                    x *= true_interval
                    if in_unit_circle([x, y]):
                        hits += 1
                    else:
                        pass
        else:
            points_plot.init()
            for y in range(0, true_res):
                y *= true_interval
                for x in range(0, true_res):
                    x *= true_interval
                    if in_unit_circle([x, y]):
                        hits += 1
                        color = (255,56,128)
                    else:
                        color = (50,50,50)
                    points_plot.plot(x, y, color_rgb = color)
        pi_approximate = (hits / resolution) * 4

    elif method == "riemann":
        # Riemann Sum method
        step = 1/resolution
        current_integral_sum = 0
        
        for x in range(0, resolution):
            x /= resolution
            y = (1 - (x ** 2)) ** 0.5
            current_integral_sum += y
        
        current_integral_sum /= resolution

        pi_approximate = current_integral_sum * 4
    
    elif method == "riemann_trap":
        # Riemann Sum, but with a parallelogram
        assert resolution > 1, "resolution for 'riemann_trap' method must be two or more."
        step_size = 1/resolution
        current_integral_sum = 0
        last_step_amount = 1
        current_step = 0
        
        while current_step < 1:
            current_step += step_size
            
            current_step_amount = (1 - (current_step ** 2)) ** 0.5
            current_integral_sum += (current_step_amount + last_step_amount) / 2
            
            last_step_amount = current_step_amount
        
        current_integral_sum /= resolution
        pi_approximate = current_integral_sum * 4

    else: # throws error, method must be valid.
        assert False, f"pi estimation method '{method}' not valid."
    
    return pi_approximate


def relative_error(item:float, target:float) -> float:
    return abs((item-target) / target)


def percent_off_pi(item:float) -> float:
    return relative_error(item, 3.141592653589793)


def main():
    doctest.testmod()
    our_guess = estimate_pi(2**0, show_graphics = False,
              method = "riemann")
    print(f"{our_guess}, {percent_off_pi(our_guess)}")
    points_plot.wait_to_close()


if __name__ == "__main__":
    main()
