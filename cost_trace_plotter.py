import csv
import math
import matplotlib
import matplotlib.pyplot as plt
import sys


def load_trace(trace_file_name):
    h = []
    m = []
    s = []

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
                h.append(int(row[0]))
                m.append(int(row[1]))
                s.append(int(row[2]))

                small_inst.append(float(row[3]) / 1000)
                small_sla.append(float(row[4])  / 1000)
                small_total.append(float(row[5])/ 1000)
                
                big_inst.append(float(row[6])  / 1000)
                big_sla.append(float(row[7])   / 1000)
                big_total.append(float(row[8]) / 1000)

                aiml_inst.append(float(row[9])  / 1000)
                aiml_sla.append(float(row[10])  / 1000)
                aiml_total.append(float(row[11])/ 1000)

            line_count += 1
  
    return h,m,s,small_inst,small_sla,small_total,big_inst,big_sla,big_total,aiml_inst,aiml_sla,aiml_total


def per_alg_plotter(h,m,s,inst,sla,total,alg_name,y1_lim):
    
    font = {
            'weight' : 'bold',
            'size'   : 10}

    matplotlib.rc('font', **font)
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["axes.labelsize"] = "12"

    x = [i for i in range(len(h))]
    ticks = [i for i in range(0,len(h),15)]
    labels=[]
    for t in ticks:
        conv = lambda x: str(x) if x > 9 else "0"+str(x)
        labels.append(conv(h[t])+":"+conv(m[t])+":"+conv(s[t]))
    
    fig, ax1 = plt.subplots()
    plt.grid(linestyle="--", linewidth=0.5)

    ax1.set_xlabel('time')
    plt.xticks(ticks, labels, rotation="vertical")
    ax1.set_ylabel(r'cost ($10^3$)')
    #plt.ylim(0,y1_lim)

    lns1 = ax1.plot(x, inst, label=alg_name+'-Inst', color='r', linestyle='--', linewidth=1)
    lns2 = ax1.plot(x, sla, label=alg_name+'-SLA', color='g', linestyle='solid', linewidth=1)
    lns3 = ax1.plot(x, total, label=alg_name+'-OPEX', color='b', linestyle='solid', linewidth=1)
    ax1.tick_params(axis='y')


    # added these three lines
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="best")

    plt.savefig(alg_name+"cost_trace.eps", bbox_inches='tight')


h,m,s,small_inst,small_sla,small_total,big_inst,big_sla,big_total,aiml_inst,aiml_sla,aiml_total = load_trace("cost_trace.csv")

per_alg_plotter(h,m,s,small_inst,small_sla,small_total,'S-VNFD',10)
per_alg_plotter(h,m,s,big_inst,big_sla,big_total,'B-VNFD',8)
per_alg_plotter(h,m,s,aiml_inst,aiml_sla,aiml_total,'AIML',8)
