import numpy as np
import logging
import sys

import debug
from debug import verbose

class ServiceType:
    def __init__(self, mu, delay_threshold):
        self.service_rate = mu
        self.delay_threshold = delay_threshold
    
class ServiceType1(ServiceType):
    def __init__(self, mu, delay_threshold):
        super().__init__(mu, delay_threshold)

    def sla_penalty(self, time):
        return max(0, (time - self.delay_threshold) * 1000)

class Requst:
    def __init__(self, arrival_time, holding_time, service_type):
        self.arrival_time = arrival_time
        self.holding_time = holding_time
        self.service_type = service_type

    def __str__(self):
        return "t = "+str(self.arrival_time)+", type = "+ str(self.service_type)

def generate_requests_per_interval(start_time, end_time, rate, service_type):
    if verbose:
        print("start_time = ", start_time, ", end_time = ", end_time, ", rate = ", rate)
    
    res = []
    t = start_time
    while t <= end_time:
        t += np.random.exponential(1.0 / rate)
        holding_time = np.random.exponential(1.0 / service_type.service_rate)
        request = Requst(t, holding_time, service_type)
        if t <= end_time:
            res.append(request)

    return res

class ArrivalRateDynamics:
    def __init__(self, portion, rate):
        self.portion = portion
        self.rate = rate

def generate_requests_per_type(arrival_rates, service_type, simulation_time):
    total_portion = 0
    for rate_dynamcis in arrival_rates:
        total_portion += rate_dynamcis.portion
    if total_portion > 1.0:
        logging.error("total_portion > 1.0")
        sys.exit(-1)

    result = []
    t = 0
    for rate_dynamcis in arrival_rates:
        start_time = t
        end_time = t + simulation_time * rate_dynamcis.portion

        result += generate_requests_per_interval(start_time, end_time, rate_dynamcis.rate, service_type)

        t = end_time

    logging.debug("per_type requests:")
    for req in result:
        logging.debug("t = %f, type.mu = %f", req.arrival_time, req.service_type.service_rate)

    return result


if __name__ == "__main__":

    arrival_rates = [ArrivalRateDynamics(0.9, 1), ArrivalRateDynamics(0.1, 10)]
    service_type = ServiceType(1)
    simulation_time = 10

    generate_requests_per_type(arrival_rates, service_type, simulation_time)

