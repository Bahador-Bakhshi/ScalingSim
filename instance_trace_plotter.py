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
    small_empty = []
    small_delay = []

    big_inst = []
    big_empty = []
    big_delay = []

    aiml_inst = []
    aiml_empty = []
    aiml_delay = []

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

                small_inst.append(int(row[4]))
                small_empty.append(int(row[5]))
                small_delay.append(float(row[6]))
                
                big_inst.append(int(row[9]))
                big_empty.append(int(row[10]))
                big_delay.append(float(row[11]))

                aiml_inst.append(int(row[14]))
                aiml_empty.append(int(row[15]))
                aiml_delay.append(float(row[16]))

            line_count += 1
  
    return h,m,s,small_inst,small_empty,small_delay,big_inst,big_empty,big_delay,aiml_inst,aiml_empty,aiml_delay


def per_alg_plotter(h,m,s,inst,empty,delay,alg_name, bot_y1_lim, top_y1_lim, bot_y2_lim, top_y2_lim):
    
    font = {
            'weight' : 'bold',
            'size'   : 10}

    matplotlib.rc('font', **font)
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["axes.labelsize"] = "12"

    x = [i for i in range(len(h))]
    ticks = [i for i in range(0,len(h),20)]
    labels=[]
    for t in ticks:
        conv = lambda x: str(x) if x > 9 else "0"+str(x)
        labels.append(conv(h[t])+":"+conv(m[t])+":"+conv(s[t]))
    
    fig, ax1 = plt.subplots()
    plt.grid(linestyle="--", linewidth=0.5)

    ax1.set_xlabel('Time')
    plt.xticks(ticks, labels, rotation="vertical")
    ax1.set_ylabel('#', color='tab:orange')
    ax1.set_ylim(bot_y1_lim, top_y1_lim)

    lns1 = ax1.plot(x, inst, label=alg_name+'-CI', color='darkorange', linestyle='solid', linewidth=1.2)
    lns2 = ax1.plot(x, empty, label=alg_name+'-EI', color='tab:orange', linestyle='-.', linewidth=1.2)
    ax1.tick_params(axis='y', labelcolor='tab:orange')
    

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel(r'Time ($10^{-4}$s)', color='tab:blue')  # we already handled the x-label with ax1
    ax2.set_ylim(bot_y2_lim, top_y2_lim)

    lns3 = ax2.plot(x, delay, label=alg_name+'-DL', color='tab:blue', linestyle='solid', linewidth=1.2)
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    
    # added these three lines
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc="best")

    plt.savefig(alg_name+"instance_trace.eps", bbox_inches='tight')


h,m,s,small_inst,small_empty,small_delay,big_inst,big_empty,big_delay,aiml_inst,aiml_empty,aiml_delay = load_trace("instance_trace.csv")

per_alg_plotter(h,m,s,small_inst,small_empty,small_delay,'S-VNFD',-0.5, 10, 25 * -0.5 / 10, 25)
per_alg_plotter(h,m,s,big_inst,big_empty,big_delay,'B-VNFD',-0.5, 8, -0.5, 8)
per_alg_plotter(h,m,s,aiml_inst,aiml_empty,aiml_delay,'ML-VRS',-0.5, 8, -0.5, 8)
