def acceleration_formula(v_0, v_max, x_remaining, a):
    # Make sure everything is a float!
    v_0 = float(max(v_0, 0))
    v_max = float(v_max)
    x_remaining = float(max(x_remaining, 0))
    a = float(a)

    if abs(v_0 - v_max) <= 1e-5:
        # Assume that they are already equal, as otherwise there might be some catastrophic rounding
        return (v_max, x_remaining / v_max)

    if x_remaining <= 1e-3:
        return (v_0, 0.0)

    # Solve x = v_0 * t + 0.5 * a * t^2 for t
    # Equivalent to 0.5 * a * t^2 + v_0 * t - x = 0
    d = v_0**2 - 2 * a * (-x_remaining)
    t_1 = (-v_0 + d**0.5) / a
    t_2 = (-v_0 - d**0.5) / a
    t_solve = max(t_1, t_2)

    # Determine the velocity we have at the end, with this acceleration
    v = v_0 + a * t_solve

    # Check if we would go too fast
    if v > v_max:
        # We would go to fast, so cap it
        # First check at what time we reach the velocity
        t_v_max = (v_max - v_0) / a

        # Now find out at what place we reach this, and the remaining distance
        x_a = v_0 * t_v_max + a / 2 * t_v_max**2
        x_i = x_remaining - x_a

        # Now travel the first part with acceleration, but the final part at maximal velocity
        t = t_v_max + x_i / v_max
        return (v_max, t)
    else:
        # Everything is fine
        return (v, t_solve)

def brake_formula(v_0, t_poll, x_remaining):
    v_0 = float(v_0)
    t_poll = float(t_poll)
    x_remaining = float(x_remaining)

    if v_0 <= 1e-4 or x_remaining <= 1e-4:
        return (0, 0)

    # Find out how long it takes in seconds to stop in the alloted distance
    t = 2 * x_remaining / v_0

    # Find the acceleration we needed to do this
    a = -v_0 / t

    # Determine the values after the polling interval
    new_v = v_0 + a * t_poll
    x_travelled = v_0 * t_poll + a / 2 * t_poll**2

    # Make sure it is positive
    new_v = max(new_v, 0)
    x_travelled = max(x_travelled, 0)

    return (new_v, x_travelled)
