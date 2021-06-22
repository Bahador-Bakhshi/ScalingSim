import csv
import math
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
    plt.grid(linestyle="--", linewidth=0.5)

    ax1.set_xlabel('Load Scale')
    ticks = rate.copy()
    labels = rate.copy()
    plt.xticks(ticks, labels)

    ax1.set_ylabel(r'cost ($10^3$)')

    lns1 = ax1.plot(rate, small_inst, label='S-VNFD-Inst', color='r', linestyle='--', marker="s", fillstyle='none', linewidth=1)
    lns2 = ax1.plot(rate, small_sla, label='S-VNFD-SLA', color='r', linestyle='-.', marker="o", fillstyle='none', linewidth=1)
    lns3 = ax1.plot(rate, small_total, label='S-VNFD-OPEX', color='r', linestyle='solid', marker="+", fillstyle='none', linewidth=1)
    
    lns1 = ax1.plot(rate, big_inst, label='B-VNFD-Inst', color='g', linestyle='--', marker="s", fillstyle='none', linewidth=1)
    lns2 = ax1.plot(rate, big_sla, label='B-VNFD-SLA', color='g', linestyle='-.', marker="o", fillstyle='none', linewidth=1)
    lns3 = ax1.plot(rate, big_total, label='B-VNFD-OPEX', color='g', linestyle='solid', marker="+", fillstyle='none', linewidth=1)
 
    lns1 = ax1.plot(rate, aiml_inst, label='aiml-VNFD-Inst', color='b', linestyle='--', marker="s", fillstyle='none', linewidth=1)
    lns2 = ax1.plot(rate, aiml_sla, label='aiml-VNFD-SLA', color='b', linestyle='-.', marker="o", fillstyle='none', linewidth=1)
    lns3 = ax1.plot(rate, aiml_total, label='aiml-VNFD-OPEX', color='b', linestyle='solid', marker="+", fillstyle='none', linewidth=1)
 
    #plt.ylim(-5,100)
    ax1.tick_params(axis='y')



    plt.legend(handlelength=1, ncol=2, handleheight=2.4, labelspacing=0.00)

    plt.savefig("Bird_eye-2days.eps", bbox_inches='tight')


load_trace("bird_eye-2days-results.csv")








