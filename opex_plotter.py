import csv
import math
import matplotlib
import matplotlib.pyplot as plt
import sys


def load_trace(trace_file_name, outname):
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

    ax1.set_xlabel(r'$\ell$')
    ticks = rate.copy()
    labels = rate.copy()
    plt.xticks(ticks, labels)

    ax1.set_ylabel(r'Cost ($10^3$)')

    lns1 = ax1.plot(rate, small_inst, label='S-NSD-Prov', color='tab:orange', linestyle='--', marker="s", fillstyle='none', linewidth=1)
    lns2 = ax1.plot(rate, small_sla, label='S-NSD-SLA', color='tab:orange', linestyle='-.', marker="o", fillstyle='none', linewidth=1)
    lns3 = ax1.plot(rate, small_total, label='S-NSD-OPEX', color='tab:orange', linestyle='solid', marker="+", fillstyle='none', linewidth=1)
    
    lns1 = ax1.plot(rate, big_inst, label='B-NSD-Prov', color='tab:blue', linestyle='--', marker="s", fillstyle='none', linewidth=1)
    lns2 = ax1.plot(rate, big_sla, label='B-NSD-SLA', color='tab:blue', linestyle='-.', marker="o", fillstyle='none', linewidth=1)
    lns3 = ax1.plot(rate, big_total, label='B-NSD-OPEX', color='tab:blue', linestyle='solid', marker="+", fillstyle='none', linewidth=1)
 
    lns1 = ax1.plot(rate, aiml_inst, label='ML-RS-Prov', color='tab:green', linestyle='--', marker="s", fillstyle='none', linewidth=1)
    lns2 = ax1.plot(rate, aiml_sla, label='ML-RS-SLA', color='tab:green', linestyle='-.', marker="o", fillstyle='none', linewidth=1)
    lns3 = ax1.plot(rate, aiml_total, label='ML-RS-OPEX', color='tab:green', linestyle='solid', marker="+", fillstyle='none', linewidth=1)
 
    #plt.ylim(-5,100)
    ax1.tick_params(axis='y')



    leg = plt.legend(handlelength=1, ncol=2, handleheight=2.4, labelspacing=0.00)
    leg.get_frame().set_alpha(0.05)

    plt.savefig(outname+".eps", bbox_inches='tight')


load_trace("bird_eye-2days-results.csv", "bird_eye-2days")
load_trace("Automative-results.csv", "Automative")
load_trace("bird_eye-results.csv", "bird_eye")










