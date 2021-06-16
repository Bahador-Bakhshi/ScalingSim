import numpy as np
import logging
import sys
import heapq
import queue

from enum import IntEnum

import request_generator

requests_queue = queue.Queue()
number_of_empty_instances = 0

class EventTypes(IntEnum):
    arrival     = 0 # new demand arrival, it will be enqueued
    dequeue     = 1 # a server dequeues a request
    finish      = 2 # processing the service is finished
    instantiate = 3 # processing the service is finished
    terminate   = 4 # processing the service is finished

class Event:
    def __init__(self, time, event_type, processor, data):
        self.time = time
        self.event_type = event_type
        self.processor = processor
        self.data = data

    def __lt__(self, other):
        return self.time < other.time

def add_event(events, event):
    if len(events) > 0:
        heapq.heappush(events, event)
    else:
        events.append(event)
        heapq.heapify(events)


def print_queue(requests_queue):
    while not requests_queue.empty():
        req = requests_queue.get()
        print("req = ", req)

def arrival_event_processor(current_time, request, events):
    logging.debug("arrival_event_processor: time = %f, req = %s", current_time, request)
    requests_queue.put(request)

    global number_of_empty_instances
    if number_of_empty_instances > 0:
        number_of_empty_instances -= 1
        event_creators[EventTypes.dequeue](current_time, events)

def arrival_event_creator(request, events):
    event = Event(request.arrival_time, EventTypes.arrival, arrival_event_processor, request)
    add_event(events, event)

def dequeue_event_processor(current_time, dummy, events):
    if requests_queue.empty():
        logging.debug("Queue is empty")
        global number_of_empty_instances
        number_of_empty_instances += 1
    else:
        request = requests_queue.get()
        logging.debug("dequeue_event_processor: time = %f, req = %s", current_time, request)
        logging.debug("dequeue_event_processor: queue len = %d", requests_queue.qsize())
    
        event_creators[EventTypes.finish](current_time, request, events)

def dequeue_event_creator(time, events):
    logging.debug("dequeue_event_creator")
    event = Event(time, EventTypes.dequeue, dequeue_event_processor, None)
    add_event(events, event)

def sla_penalty(current_time, request):
    time = current_time - request.arrival_time
    return request.service_type.sla_penalty(time)

def finish_event_processor(current_time, request, events):
    logging.debug("finish_event_processor: time = %f, request = %s", current_time, request)
    penalty = sla_penalty(current_time, request)
    logging.debug("finish_event_processor: SLA penalty = %f", penalty)
    event_creators[EventTypes.dequeue](current_time, events)
    
def finish_event_creator(current_time, request, events):
    logging.debug("finish_event_creator")
    time = current_time + request.holding_time
    event = Event(time, EventTypes.finish, finish_event_processor, request)
    add_event(events, event)

class InstanceLifeTime:
    def __init__(self):
        self.instantiation_time = 0
        self.terminatation_time = 0

instances = []

INSTANTIATION_TIME = 10
def get_instantiation_time():
    return INSTANTIATION_TIME

def instantiate_event_processor(current_time, dummy, events):
    logging.debug("instantiate_event_processor: time = %s", current_time)
    slt = InstanceLifeTime()
    slt.instantiation_time = max(current_time, 0)
    global number_of_empty_instances
    number_of_empty_instances += 1

def instantiate_event_creator(current_time, events):
    logging.debug("instantiate_event_creator: time = %s", current_time)
    time = current_time + get_instantiation_time()
    event = Event(time, EventTypes.instantiate, instantiate_event_processor, None)
    add_event(events, event)


event_creators={}
event_creators[EventTypes.arrival] = arrival_event_creator
event_creators[EventTypes.dequeue] = dequeue_event_creator
event_creators[EventTypes.finish]  = finish_event_creator
event_creators[EventTypes.instantiate] = instantiate_event_creator

def fill_arrival_events(requests, events):
    for req in requests:
        event_creators[EventTypes.arrival](req, events)
    
def print_events(events):
    for event in events:
        print("time = ", event.time, ", type = ", event.event_type, ", proc = ", event.processor, ", data = ", event.data)


def start():
    events = []
    return events

def run(events):
    while len(events) > 0:
        event = heapq.heappop(events)
        event.processor(event.time, event.data, events)
        print("number_of_empty_instances = ", number_of_empty_instances)


if __name__ == "__main__":

    
    arrival_rates = [request_generator.ArrivalRateDynamics(0.9, 3), request_generator.ArrivalRateDynamics(0.1, 5)]
    service_type = request_generator.ServiceType1(0.5, 5)
    simulation_time = 10

    requests = request_generator.generate_requests_per_type(arrival_rates, service_type, simulation_time)

    events = start()
    fill_arrival_events(requests, events)
    event_creators[EventTypes.instantiate](-100, events)
    run(events)
    


