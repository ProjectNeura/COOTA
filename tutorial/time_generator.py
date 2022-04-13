from coota.preset import *
import datetime


# generate a datetime from April 1, 2022 to June 1, 2022
# can be either str or datetime.datetime object or integer time stamp
range_from, range_to = "2022-4-1", "2022.6.1"   # optional, the default range is from now to next year
# range_from, range_to = datetime.datetime(year=2022, month=4, day=1), datetime.datetime(year=2022, month=6, day=1)
# range_from, range_to = 1648791336, 1654061736

generator = TimeGenerator(start=range_from, stop=range_to)
time = generator.generate()
print(type(time), time)
