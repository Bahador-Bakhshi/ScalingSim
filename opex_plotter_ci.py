import csv
import math
import matplotlib
import matplotlib.pyplot as plt
import sys


def load_trace(trace_file_name, outname):
    rate = []

    small_inst = []
    small_inst_ci = []
    small_sla = []
    small_sla_ci = []
    small_total = []
    small_total_ci = []

    big_inst = []
    big_inst_ci = []
    big_sla = []
    big_sla_ci = []
    big_total = []
    big_total_ci = []

    aiml_inst = []
    aiml_inst_ci = []
    aiml_sla = []
    aiml_sla_ci = []
    aiml_total = []
    aiml_total_ci = []

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
                small_inst_ci.append(float(row[2]) / 1000)
                small_sla.append(float(row[3]) / 1000)
                small_sla_ci.append(float(row[4]) / 1000) 
                small_total.append(float(row[5]) / 1000)
                small_total_ci.append(float(row[6]) / 1000)
                
                big_inst.append(float(row[7])  / 1000)
                big_inst_ci.append(float(row[8]) / 1000)
                big_sla.append(float(row[9])   / 1000)
                big_sla_ci.append(float(row[10]) / 1000)
                big_total.append(float(row[11]) / 1000)
                big_total_ci.append(float(row[12]) / 1000)

                aiml_inst.append(float(row[13])  / 1000)
                aiml_inst_ci.append(float(row[14])  / 1000)
                aiml_sla.append(float(row[15])  / 1000)
                aiml_sla_ci.append(float(row[16])  / 1000)
                aiml_total.append(float(row[17]) / 1000)
                aiml_total_ci.append(float(row[18])/ 1000)

            line_count += 1
  
    
    font = {
            'weight' : 'bold',
            'size'   : 10
        }

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

    ms = 3.5
    cs = 1.2 * ms
    
    lns1 = ax1.errorbar(rate, small_inst, yerr=small_inst_ci, label='L-INS-Prov', color='tab:orange', linestyle='--', marker="s", fillstyle='none', linewidth=1, markersize=ms, capsize=cs)
    lns2 = ax1.errorbar(rate, small_sla, yerr = small_sla_ci, label='L-INS-SLA', color='tab:orange', linestyle='-.', marker="o", fillstyle='none', linewidth=1, markersize=ms, capsize=cs)
    lns3 = ax1.errorbar(rate, small_total, yerr = small_total_ci, label='L-INS-OPEX', color='tab:orange', linestyle='solid', marker="+", fillstyle='none', linewidth=1, markersize=ms, capsize=cs)
    
    lns1 = ax1.errorbar(rate, big_inst, yerr = big_inst_ci, label='H-INS-Prov', color='tab:blue', linestyle='--', marker="s", fillstyle='none', linewidth=1, markersize=ms, capsize=cs)
    lns2 = ax1.errorbar(rate, big_sla, yerr = big_sla_ci, label='H-INS-SLA', color='tab:blue', linestyle='-.', marker="o", fillstyle='none', linewidth=1, markersize=ms, capsize=cs)
    lns3 = ax1.errorbar(rate, big_total, yerr = big_total_ci, label='H-INS-OPEX', color='tab:blue', linestyle='solid', marker="+", fillstyle='none', linewidth=1, markersize=ms, capsize=cs)
 
    lns1 = ax1.errorbar(rate, aiml_inst, yerr = aiml_inst_ci, label='ML-RS-Prov', color='tab:green', linestyle='--', marker="s", fillstyle='none', linewidth=1, markersize=ms, capsize=cs)
    lns2 = ax1.errorbar(rate, aiml_sla, yerr = aiml_sla_ci, label='ML-RS-SLA', color='tab:green', linestyle='-.', marker="o", fillstyle='none', linewidth=1, markersize=ms, capsize=cs)
    lns3 = ax1.errorbar(rate, aiml_total, yerr= aiml_total_ci, label='ML-RS-OPEX', color='tab:green', linestyle='solid', marker="+", fillstyle='none', linewidth=1, markersize=ms, capsize=cs)

    #plt.ylim(-5,100)
    ax1.tick_params(axis='y')



    leg = plt.legend(handlelength=1, ncol=3, handleheight=2.4, labelspacing=0.00)
    leg.get_frame().set_alpha(0.75)

    plt.savefig(outname+".pdf", bbox_inches='tight')


load_trace("bird_eye-2days-results.csv", "bird_eye-2days")
load_trace("Automative-results.csv", "Automative")
load_trace("bird_eye-results.csv", "bird_eye")










