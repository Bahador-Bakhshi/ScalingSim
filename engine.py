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
must_be_terminated = 0
sla_penalty_cost = []
instances = []

class EventTypes(IntEnum):
    arrival     = 0 # new demand arrival, it will be enqueued
    dequeue     = 1 # a server dequeues a request
    finish      = 2 # processing the service is finished
    instantiate = 3 # processing the service is finished
    terminate   = 4 # processing the service is finished
    monitor     = 5

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
    
    if number_of_instances == 0:
        instantiate_event_processor(current_time, None, events)
    elif number_of_empty_instances > 0:
        dequeue_event_creator(current_time, events)

def arrival_event_creator(request, events):
    event = Event(request.arrival_time, EventTypes.arrival, arrival_event_processor, request)
    add_event(events, event)

def dequeue_event_processor(current_time, dummy, events):

    if requests_queue.empty():
        logging.debug("Queue is empty")
    else:
        global number_of_empty_instances
        number_of_empty_instances -= 1
 
        request = requests_queue.get()
        logging.debug("dequeue_event_processor: time = %f, req = %s", current_time, request)
    
        finish_event_creator(current_time, request, events)

def dequeue_event_creator(time, events):
    logging.debug("dequeue_event_creator, time = %s", time)
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

    global number_of_empty_instances
    number_of_empty_instances += 1
 
    dequeue_event_creator(current_time, events)

    global must_be_terminated
    if must_be_terminated > 0:
        termination_event_processor(current_time, None, events)

    
def finish_event_creator(current_time, request, events):
    logging.debug("finish_event_creator: time = %s", current_time)
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

    dequeue_event_creator(current_time, events)

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
            global must_be_terminated
            must_be_terminated -= 1
            
            return

    logging.error("termination_event_processor: cannot find an instance to terminate")
    sys.exit(-1)

def termination_event_creator(current_time, events):
    logging.debug("termination_event_creator: time = %s", current_time)
    event = Event(current_time, EventTypes.terminate, termination_event_processor, None)
    add_event(events, event)


class MonitoringDataQLen:
    def __init__(self,  queue_len):
        self.queue_len = queue_len

QLEN_HIGH_THRESHOLD = 5
QLEN_LOW_THRESHOLD = 3
def monitor_event_processor(current_time, interval, events):
    monitoring_data = MonitoringDataQLen(requests_queue.qsize())
    logging.debug("monitor_event_processor: time = %s, len = %d", current_time, monitoring_data.queue_len)
    if monitoring_data.queue_len > QLEN_HIGH_THRESHOLD:
        instantiate_event_creator(current_time, events)
    elif monitoring_data.queue_len < QLEN_LOW_THRESHOLD:
        if number_of_instances > 1: # FIXME or monitoring_data.queue_len == 0:
            global must_be_terminated
            must_be_terminated += 1

    if len(events) > 0:
        monitor_event_creator(current_time, interval, events)

def monitor_event_creator(current_time, interval, events):
    logging.debug("monitor_event_creator: time = %s", current_time)
    monitoring_time = current_time + interval
    event = Event(monitoring_time, EventTypes.monitor, monitor_event_processor, interval)
    add_event(events, event)

def fill_arrival_events(requests, events):
    for req in requests:
        arrival_event_creator(req, events)

def fill_monitoring_events(interval, simulation_time, events):
    '''
    time = interval
    while time < simulation_time:
        monitor_event_creator(time, events)
        time += interval
    '''
    monitor_event_creator(0, interval, events)

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

        logging.debug("number_of_instances = %s, number_of_empty_instances = %s, Q len = %s", number_of_instances, number_of_empty_instances, requests_queue.qsize())
    
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
    
    arrival_rates = [request_generator.ArrivalRateDynamics(0.25, 1.0), request_generator.ArrivalRateDynamics(0.5, 2.0), request_generator.ArrivalRateDynamics(0.25, 0.5)]
    service_type = request_generator.ServiceType1(0.030, 5 * 1.0 / 4.0)
    simulation_time = 20
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
            fill_monitoring_events(INSTANTIATION_TIME * 1.5, simulation_time, events)
            #for _ in range(instance_num):
            #    instantiate_event_creator(-100, events)

            last_time = run(events)

            for _ in range(number_of_instances):
                termination_event_creator(last_time, events)
            run(events)

            inst_costs = instances_costs()
            inst_costs_arr.append(inst_costs)
            sla_costs  = sla_cost()
            sla_costs_arr.append(sla_costs)
            logging.debug("instances_costs = %s, sla_cost = %s", inst_costs, sla_costs)
    
        print("Result for max_instance_num = ", instance_num," instances_costs = ", sum(inst_costs_arr) / iterations, " sla_costs = ", sum(sla_costs_arr) / iterations, flush=True)

