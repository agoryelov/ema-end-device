# Copyright Clinton Fernandes (clint.fernandes@gmail.com) 2021


def ppb_to_ppm(measurement) -> float:
    return measurement / 1000

# Change micro grams per meter cubed
# To grams per litre
def μgm3_to_gpl(measurement)->float:
    return measurement / 1000

# 0.1 liter to 1 liter
def pms_gt_output_to_si(measurement)->float:
    return measurement * 10
