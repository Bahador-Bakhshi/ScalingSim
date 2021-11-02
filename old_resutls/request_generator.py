import numpy as np
import logging
import sys

import debug
from debug import verbose

class ServiceType:
    def __init__(self, mu, delay_threshold1, delay_threshold2):
        self.service_rate = mu
        self.delay_threshold1 = delay_threshold1
        self.delay_threshold2 = delay_threshold2

#Automative
class ServiceType1(ServiceType):
    SLA_PENALTY_PER_TIME_1 = 1
    SLA_PENALTY_PER_TIME_2 = 2
    
    def __init__(self, mu, delay_threshold1, delay_threshold2):
        super().__init__(mu, delay_threshold1, delay_threshold2)

    def sla_penalty(self, time):
        logging.debug("sla_penalty: processing_time = %f", time)
        if time < self.delay_threshold1:
            return 0
        elif time < self.delay_threshold2:
            return (time - self.delay_threshold1) * self.SLA_PENALTY_PER_TIME_1
        else:
            return (time - self.delay_threshold2) * self.SLA_PENALTY_PER_TIME_2

    def __str__(self):
        return "mu = "+str(self.service_rate)+", threshold1 = "+str(self.delay_threshold1)+", threshold2 = "+str(self.delay_threshold2)

#Bird Eye
class ServiceType2(ServiceType):
    SLA_PENALTY_PER_TIME_1 = 0.75
    SLA_PENALTY_PER_TIME_2 = 1.25
    
    def __init__(self, mu, delay_threshold1, delay_threshold2):
        super().__init__(mu, delay_threshold1, delay_threshold2)

    def sla_penalty(self, time):
        logging.debug("sla_penalty: processing_time = %f", time)
        if time < self.delay_threshold1:
            return 0
        elif time < self.delay_threshold2:
            return (time - self.delay_threshold1) * self.SLA_PENALTY_PER_TIME_1
        else:
            return (time - self.delay_threshold2) * self.SLA_PENALTY_PER_TIME_2

    def __str__(self):
        return "mu = "+str(self.service_rate)+", threshold1 = "+str(self.delay_threshold1)+", threshold2 = "+str(self.delay_threshold2)


class Requst:
    def __init__(self, arrival_time, holding_time, service_type):
        self.arrival_time = arrival_time
        self.holding_time = holding_time
        self.service_type = service_type

    def __str__(self):
        return "t = "+str(self.arrival_time)+", ht ="+str(self.holding_time)+", type = "+ str(self.service_type)

def generate_requests_per_interval(start_time, end_time, rate, service_type):
    logging.debug("start_time = %s, end_time = %s, rate = %s", start_time, end_time, rate)
    
    res = []
    t = start_time
    while t <= end_time:
        t += np.random.exponential(1.0 / rate)
        holding_time = min(np.random.exponential(1.0 / service_type.service_rate), service_type.delay_threshold1)
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
        logging.debug("req = %s", req)

    return result


if __name__ == "__main__":
    '''
    arrival_rates = [ArrivalRateDynamics(0.9, 1), ArrivalRateDynamics(0.1, 10)]
    service_type = ServiceType(1)
    simulation_time = 10

    generate_requests_per_type(arrival_rates, service_type, simulation_time)
    '''

    service_type = ServiceType1(1, 2, 10)
    for i in range(20):
        print(service_type.sla_penalty(i))
