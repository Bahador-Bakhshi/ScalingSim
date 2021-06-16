import numpy as np
import logging
import sys
import heapq
import queue

from enum import IntEnum

import request_generator

requests_queue = queue.Queue()
number_of_empty_instances = 0
number_of_instances = 0
sla_penalty_cost = []
instances = []

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
    sla_penalty_cost.append(penalty)
    event_creators[EventTypes.dequeue](current_time, events)
    
def finish_event_creator(current_time, request, events):
    logging.debug("finish_event_creator")
    time = current_time + request.holding_time
    event = Event(time, EventTypes.finish, finish_event_processor, request)
    add_event(events, event)

class InstanceLifeTime:
    def __init__(self):
        self.instantiation_time = None
        self.terminatation_time = None


INSTANTIATION_TIME = 10
def get_instantiation_time():
    return INSTANTIATION_TIME

def instantiate_event_processor(current_time, dummy, events):
    logging.debug("instantiate_event_processor: time = %s", current_time)
    slt = InstanceLifeTime()
    slt.instantiation_time = max(current_time, 0)
    instances.append(slt)

    global number_of_empty_instances
    number_of_empty_instances += 1
    global number_of_instances
    number_of_instances += 1

def instantiate_event_creator(current_time, events):
    logging.debug("instantiate_event_creator: time = %s", current_time)
    time = current_time + get_instantiation_time()
    event = Event(time, EventTypes.instantiate, instantiate_event_processor, None)
    add_event(events, event)


def termination_event_processor(current_time, dummy, events):
    logging.debug("termination_event_processor: time = %s", current_time)

    for slt in instances:
        if slt.terminatation_time == None:
            slt.terminatation_time = current_time
            
            global number_of_empty_instances
            number_of_empty_instances -= 1
            global number_of_instances
            number_of_instances -= 1

            return

    logging.error("termination_event_processor: cannot find an instance to terminate")
    sys.exit(-1)

def termination_event_creator(current_time, events):
    logging.debug("termination_event_creator: time = %s", current_time)
    event = Event(current_time, EventTypes.terminate, termination_event_processor, None)
    add_event(events, event)


event_creators={}
event_creators[EventTypes.arrival] = arrival_event_creator
event_creators[EventTypes.dequeue] = dequeue_event_creator
event_creators[EventTypes.finish]  = finish_event_creator
event_creators[EventTypes.instantiate] = instantiate_event_creator
event_creators[EventTypes.terminate] = termination_event_creator


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
    last_time = 0
    while len(events) > 0:
        event = heapq.heappop(events)
        last_time = event.time
        event.processor(event.time, event.data, events)
        logging.debug("number_of_empty_instances = %s", number_of_empty_instances)
    
    return last_time

INSTANTIATION_COST = 30000
def instantiation_cost():
    return INSTANTIATION_COST

INSTANTCE_USAGE_PER_TIMER = 10
def instance_usage_cost(ht):
    return ht * INSTANTIATION_TIME

def instances_costs():
    total_cost = 0
    for slt in instances:
        ht = slt.terminatation_time - slt.instantiation_time
        logging.debug("instances_costs: st = %s, et = %s", slt.instantiation_time, slt.terminatation_time)
        total_cost += instantiation_cost() + instance_usage_cost(ht)

    return total_cost

def sla_cost():
    return sum(sla_penalty_cost)

if __name__ == "__main__":
    
    arrival_rates = [request_generator.ArrivalRateDynamics(0.25, 5), request_generator.ArrivalRateDynamics(0.5, 20), request_generator.ArrivalRateDynamics(0.25, 10)]
    service_type = request_generator.ServiceType1(4.0, 5 * 1.0 / 4.0)
    simulation_time = 10
    iterations = 1
    max_instance_num = 2

    for instance_num in range(1,max_instance_num):
        inst_costs_arr = []
        sla_costs_arr  = []

        for _ in range(iterations):
            requests = request_generator.generate_requests_per_type(arrival_rates, service_type, simulation_time)

            requests_queue = queue.Queue()
            number_of_empty_instances = 0
            number_of_instances = 0
            sla_penalty_cost = []
            instances = []

            events = start()
            fill_arrival_events(requests, events)
            for _ in range(instance_num):
                event_creators[EventTypes.instantiate](-100, events)

            last_time = run(events)

            for _ in range(instance_num):
                event_creators[EventTypes.terminate](last_time, events)
            run(events)

            inst_costs = instances_costs()
            inst_costs_arr.append(inst_costs)
            sla_costs  = sla_cost()
            sla_costs_arr.append(sla_costs)
            logging.debug("instances_costs = %s, sla_cost = %s", inst_costs, sla_costs)
    
        print("Result for max_instance_num = ", instance_num," instances_costs = ", sum(inst_costs_arr) / iterations, " sla_costs = ", sum(sla_costs_arr) / iterations, flush=True)

