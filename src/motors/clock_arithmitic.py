def return_to_zero_from(v):
    """
    Return the number of steps required to get back
    to 0 if 1 rotation is 512 steps.
    The current steps may be negative or positive.
    Half rotation is 256, and this is as far as
    it is possible to get away from 0
    """
    s = v % 512
    steps = 256 - (s - 256) if s > 256 else s
    return steps, s > 256


return_to_zero_from(1)
return_to_zero_from(-1)
return_to_zero_from(255)
return_to_zero_from(256)
return_to_zero_from(257)
return_to_zero_from(511)
return_to_zero_from(-511)
return_to_zero_from(0)