# Observability
This script allows you to determine when an astronomical target is observable during some period of time from a particular location, where 'observable' is subject to user-defined constraints. The output is a list of time windows when the target is observable, subject to the precision chosen by the user, with each line of output containing two comma-separated times, the first being the start time when the target first becomes observable, and the second being the end time when the target is last observable before becoming unobservable again.
The script is rather slow and just a simple solution I made relatively quickly when I didn't find any other ready-made solution. The more fine the precision and the longer the period of time, the longer the script takes to complete execution.
# How to use
The steps all involve modifying variables defined in the script. The script as uploaded contains values for these variables as an example.
1. Modify the variable `constraint` to the contain the conditions the target needs to satisfy for it to be observable. See [this](https://astroplan.readthedocs.io/en/latest/tutorials/constraints.html) and [this](https://astroplan.readthedocs.io/en/latest/api.html) for more info on how to define constraints. For the example given, there is only one constraint placed: that the object needs to be at least 30 degrees above the horizon.
2. Modify the variable `Observer` to include the detains of the location from which the target is to be observed. For the format of the latitude and longitude, see [this](https://docs.astropy.org/en/stable/api/astropy.coordinates.Angle.html), and for the format of the units of the elevation see [this](https://docs.astropy.org/en/stable/units/) and [this](https://docs.astropy.org/en/stable/units/#module-astropy.units). See [this](https://astroplan.readthedocs.io/en/latest/api/astroplan.Observer.html) for more details on available arguments for the Observer object. For the example given, the observer is defined by the latitude, longitude, and elevation of [Royal Observatory, Edingburgh](https://en.wikipedia.org/wiki/Royal_Observatory,_Edinburgh).
3. Modify the variable `coord` to the coordinates of the target to be observed. See [this](https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html) for more info on that. The example given is for [ACO 963](http://simbad.u-strasbg.fr/simbad/sim-id?Ident=ACO+++963).
4. Modify the variable `interval` to your desired precision, in minutes. This represents how accurate the start and end times in the output are. In the example shown, the interval is 5 minutes, so the start and end times of each time window in which the object is observable are given to the nearest 5 minutes.
5. Modify the variable `p` to the time period during which you're interested in observing the target. In the example given, it's from 23 January 2021 to 27 March 2021, further constrained by the `byhour` argument which specifies which hours of the day to consider. In the example given, it's known the target isn't observable in the daylight hours from 09:00 to 15:00, so only the hours from 16:00 to 08:00 are considered (inclusive, so this includes times like 08:55). See more info, including other arguments similar to `byhour`, [here](https://dateutil.readthedocs.io/en/stable/rrule.html).
6. Run the script and wait for all the output.
# How it works
The way the script works is that for an `interval` value of n, `p` is an iterable object for the time every n minutes, for times between the start of the time period and the end of it and which satisfy the constraints of the `byhour` argument and/or other similar arguments that are used. It checks for each of these times in order whether the constraints for the target's observability is satisfied. When the answer changes from 'no' to 'yes', that indicates the start of a time window during which the target is observable, so that time for which the answer became 'yes' is output as the start time. When the answer changes from 'yes' to 'no', that indicates the end of a time window during which the target is observable, so the time n minutes prior to that time for which the answer became 'no' is the last time the object was known to be observable, and it's output as the end time (separated from the start time by a comma).
When the interval is larger or the time period of `p` is further constrained, there are less times to iterate through so the code completes execution quicker, but of course at the cost of accuracy for a larger interval.
# Possible improvements
As I said, the script was made relatively quickly and is not the best possible solution, the biggest issue perhaps being how long it takes to complete execution. A possible improvemnt to implement:

Decide on a minimum length for an observing window, either the minimum possible time that the target would be observable for (if that's known) or the minimum length of an observability window that the user is willing to try observing it in. Set this as the interval between subsequent checks of the target's observability, rather than 5 minutes (or whatever the precision is). When the observability of the target changes between subsequent checks, call a recursive function to further narrow down the time at which the change occurs until the user's desired precision is reached.