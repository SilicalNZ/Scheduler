import pprint

from Scheduler import *
from datetime import timedelta


nap_prep = Action('Nap Prep', Time(minutes=10))
nap = Action('Nap', Time(minutes=20))

main_s = Action('Main Sleep', Time(hours=3))
main_sleep = RelativeEvent('Main Sleep')
main_sleep.add_action(nap_prep)
main_sleep.add_action(main_s)

napping = RelativeEvent('Nap')
napping.add_action(nap_prep)
napping.add_action(nap)

sleeps = Event('Sleeps', Time(3*60*60))


sleeps.add_action(napping, Time(minutes=35))
sleeps.add_action(napping, Time(hours=7))
sleeps.add_action(napping, Time(hours=11, minutes=45))
sleeps.add_action(main_sleep, Time(hours=20))

display = visualizer(sleeps, Time(hours = 24))
display = [str(i) for i in display]
print(''.join(display))