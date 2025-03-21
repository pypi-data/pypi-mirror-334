import itertools
from dataclasses import dataclass
from threading import Thread
import time
from typing import *

def generate_laggy(values, lag=1):
    for v in values:
        time.sleep(lag)
        yield v

class NonblockingStreams:
    def __init__(self, *iterators):
        self.iterators = iterators

        self.collected = {i: [] for i in range(len(self.iterators))}
        self.returned_count = {i: 0 for i in range(len(self.iterators))}
        self.stop_iteration = {i: False for i in range(len(self.iterators))}
        self.threads = [Thread(target=self.collect, args=[i]) for i in range(len(self.iterators))]
        [thread.start() for thread in self.threads]

    def collect(self, i):
        self.collected[i] = []
        self.returned_count[i] = 0
        self.stop_iteration[i] = False
        
        for it in self.iterators[i]:
            self.collected[i].append(it)

        self.stop_iteration[i] = True
    
    def get(self, i = None, timeout: int | None = None):

        if i == None:
            I = list(range(len(self.iterators)))
        elif isinstance(i, int):
            I = [i]
        else:
            I = i

        
        result = None
        start = time.time() * 1000

        while not result and (not timeout or time.time() * 1000 - start < timeout):
            for i in I:
                if self.returned_count[i] < len(self.collected[i]):
                    returned = self.returned_count[i]
                    collected = self.collected[i][returned]
                    result = (i, collected)
                    break
    
        if not result:
            raise TimeoutError

        self.returned_count[i] += 1
        return result
    
    def returned(self, which: int | List[int] | None = None):
        which = range(len(self.iterators)) if which is None else which
        which = [which] if isinstance(which, int) else which
        result = {}
        for i in which:
            result[i] = self.collected[i][:self.returned_count[i]]
        return result

    def all_returned(self, check=None):
        check = range(len(self.iterators)) if check is None else check
        check = [check] if isinstance(check, int) else check
        return all([self.returned_count[i] == len(self.collected[i]) and self.stop_iteration[i] for i in check])

def product(*iterables: Iterable):
    streams = NonblockingStreams(*iterables)
    while not streams.all_returned():
        i, n = streams.get(timeout=None)
        returned = streams.returned()
        returned[i] = [n]

        yield from itertools.chain(itertools.product(*list(returned.values())))


def combinations(iterable: Iterable, r: int):
    streams = NonblockingStreams(iterable)
    while not streams.all_returned():
        i, n = streams.get(timeout=None)
        returned = streams.returned()[0][:-1]
        for c in itertools.combinations(returned, r-1):
            yield tuple([*c, n])

def combinations_with_replacement(iterable: Iterable, r: int):
    streams = NonblockingStreams(iterable)
    while not streams.all_returned():
        _, n = streams.get(timeout=None)
        returned = streams.returned()[0][:-1]
        for _r in range(0, r):
            for c in itertools.combinations_with_replacement(returned, _r):
                yield tuple([*c, *[n]*(r-_r)])

def permutations(iterable: Iterable, r=None):
    streams = NonblockingStreams(iterable)
    while not streams.all_returned():
        _, n = streams.get(timeout=None)
        returned = streams.returned()[0][:-1]
        for c in itertools.combinations(returned, r-1):
            yield from itertools.permutations([*c, n], r)

def chain(*iterables: List[Iterable]):
    streams = NonblockingStreams(*iterables)
    for i in range(len(iterables)):
        while not streams.all_returned(i):
            _, n = streams.get(i)
            yield n
