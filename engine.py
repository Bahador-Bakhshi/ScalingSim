import numpy as np
import logging
import sys
import heapq
import queue

from enum import IntEnum

import request_generator

class EventTypes(IntEnum):
    arrival     = 0 # new demand arrival, it will be enqueued
    dequeue     = 1 # a server dequeues a request
    finish      = 2 # processing the service is finished
    no_empty    = 3 # there is at least one requst in the queue, wake up if any idle server


class Event:
    def __init__(self, time, event_type, processor, data):
        self.time = time
        self.event_type = event_type
        self.processor = processor
        self.data = data

    def __lt__(self, other):
        return self.time < other.time


requsts_queue = queue.Queue()

def arrival_event_processor(request):
    requsts_queue.put(request)

def arrival_event_creator(request):
    event = Event(request.arrival_time, EventTypes.arrival, arrival_event_processor, request)
    return event

event_creators={}
event_creators[EventTypes.arrival] = arrival_event_creator


def fill_arrival_events(requests, events):
    for req in requests:
        eve = event_creators[EventTypes.arrival](req)
        events.append(eve)
    
    heapq.heapify(events)

def print_events(events):
    for event in events:
        print("time = ", event.time, ", type = ", event.event_type, ", proc = ", event.processor, ", data = ", event.data)


def start():
    events = []
    return events


if __name__ == "__main__":

    
    arrival_rates = [request_generator.ArrivalRateDynamics(0.9, 1), request_generator.ArrivalRateDynamics(0.1, 10)]
    service_type = request_generator.ServiceType(5)
    simulation_time = 10

    requests = request_generator.generate_requests_per_type(arrival_rates, service_type, simulation_time)

    events = start()
    fill_arrival_events(requests, events)
    print_events(events)
