import itertools


TIME_RELATIVE_TO_SECONDS = {
    'days': 60*60*24,
    'hours': 60*60,
    'minutes': 60
}



class Time:
    def __init__(self, seconds=0, minutes=0, hours=0, days=0):
        self._seconds = seconds \
                        + minutes * TIME_RELATIVE_TO_SECONDS['minutes'] \
                        + hours * TIME_RELATIVE_TO_SECONDS['hours'] \
                        + days * TIME_RELATIVE_TO_SECONDS['days']

    @property
    def seconds(self):
        return self._seconds

    @property
    def minutes(self):
        return self._seconds // TIME_RELATIVE_TO_SECONDS['minutes']

    @property
    def hours(self):
        return self._seconds // TIME_RELATIVE_TO_SECONDS['hours']


class Action:
    def __init__(self, name: str, duration: Time):
        self.name = name
        self.duration = duration

    def __str__(self):
        return f'{self.name}: {self.duration}'


class KeyList:
    """
    Emulates a dictionary except you can have unlimited keys
    pop is handled by removal of first find
    """
    def __init__(self):
        self._x = []

    def append(self, x, y):
        self._x.append((x, y))

    def pop(self, x):
        for x, i in enumerate(self._x):
            if i[0] == x: return self._x.pop(x)

    def keys(self):
        yield from (x for x, _ in self._x)

    def values(self):
        yield from (y for _, y in self._x)

    def items(self):
        yield from self._x

    def insert(self, position: int, x, y):
        self._x.insert(position, (x, y))



class Event:
    def __init__(self, name, duration: Time):
        self.name = name
        self.duration = duration
        self.actions = KeyList()

    def add_action(self, action, time_insertion: Time):
        self.actions.append(action, time_insertion)

    def remove_action(self, action: Action):
        self.actions.pop(action)

    def __str__(self):
        return f'{self.name}: {self.duration}'


class RelativeEvent:
    def __init__(self, name):
        self.name = name
        self.actions = []

    @property
    def duration(self):
        return Time(seconds=sum(i.duration.seconds for i in self.actions))

    def add_action(self, action):
        self.actions.append(action)

    def remove_action(self, action):
        self.actions.remove(action)

    def __str__(self):
        return f'{self.name}: {self.duration}'


def split_every(iterable, n):
    i = iter(iterable)
    slice = list(itertools.islice(i, n))
    while slice:
        yield slice
        slice = list(itertools.islice(i, n))


def visualizer(event: Event, timespan: Time):
    template = sum([[str(h % 10)] * 60 for h in range(timespan.hours)], [])

    for action, insertion in event.actions.items():
        insertion = insertion.minutes
        duration = action.duration.minutes
        for i in range(insertion, insertion + duration):
            template[i] = '_'

    template = [''.join(i) for i in split_every(template, 60)]
    template = '\n'.join(template)


    return template
