import csv
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys


def load_trace(trace_file_name):
    rate = []

    small_inst = []
    small_sla = []
    small_total = []

    big_inst = []
    big_sla = []
    big_total = []

    aiml_inst = []
    aiml_sla = []
    aiml_total = []

    with open(trace_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                pass
            elif len(row) > 0:
                rate.append(float(row[0]))

                small_inst.append(float(row[1]) / 1000)
                small_sla.append(float(row[2])  / 1000)
                small_total.append(float(row[3])/ 1000)
                
                big_inst.append(float(row[4])  / 1000)
                big_sla.append(float(row[5])   / 1000)
                big_total.append(float(row[6]) / 1000)

                aiml_inst.append(float(row[7])  / 1000)
                aiml_sla.append(float(row[8])  / 1000)
                aiml_total.append(float(row[9])/ 1000)

            line_count += 1
  
    
    font = {
            'weight' : 'bold',
            'size'   : 10}

    matplotlib.rc('font', **font)
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["axes.labelsize"] = "12"

    fig, ax1 = plt.subplots()
    plt.grid(axis="y", linestyle="--", linewidth=0.5)

    ax1.set_xlabel('Load Scale')
    ticks = rate.copy()
    labels = rate.copy()
    plt.xticks(ticks, labels)

    ax1.set_ylabel(r'OPEX ($10^3$)')
    width = 0.025

    rate_small = [x - width for x in rate]
    rate_aiml  = rate.copy()
    rate_big   = [x + width for x in rate]
    
    plt.bar(rate_small, small_inst, width, label='S-VNFD-Inst', color='darkgreen')
    plt.bar(rate_aiml, aiml_inst, width, label='AIML-Inst', color='aqua')
    plt.bar(rate_big, big_inst, width, label='B-VNFD-Inst', color='blue')

    plt.bar(rate_small, small_sla, width, label='S-VNFD-SLA', bottom=small_inst, color='red')
    plt.bar(rate_aiml, aiml_sla, width, label='AIML-SLA', bottom=aiml_inst, color='orange')
    plt.bar(rate_big, big_sla, width, label='B-VNFD-SLA', bottom=big_inst, color='darkred')

    #plt.ylim(-5,100)
    ax1.tick_params(axis='y')

    plt.legend(handlelength=1, ncol=2, handleheight=2.4, labelspacing=0.00)

    plt.savefig("Automative-bar.eps", bbox_inches='tight')


load_trace("Automative-results.csv")








