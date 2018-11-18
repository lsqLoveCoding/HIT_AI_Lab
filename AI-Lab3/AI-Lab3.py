import networkx as nx


def find_pre_count(var):
    count = 0
    for ab in G.predecessors(var):
        count += 1
    return(count)


def find_pre_counts(var):
    count = []
    for ab in G.predecessors(var):
        count.append(ab)
    return(count)


def calc_prob(tof, parent_list, pros):
    count = 0
    for i in range(1, len(parent_list)):
        bit = len(parent_list) - i - 1
        count += tof[i] * (2 ** bit)
    pr = 0
    if tof[0] == 1:
        pr += pros[count][0]
    else:
        pr += pros[count][1]
    return pr


def detect_value(values):
    detected = []
    for key in values.keys():
        if values[key] == -1:
            detected.append(key)
    return detected


def get_value(values, list_value):
    calc_value = []
    length = len(list_value)
    for i in range(2 ** length):
        ints = []
        count = 0
        for j in range(length):
            if j is 0:
                ints.append(i%2)
                count += i%2
            else:
                ints.append(((i-count)%(2**(j+1)))>>j)
                count = (i-count)%(2**(j+1))
        vals = dict(values)
        for j in range(length):
            vals[list_value[j]] = ints[j]
        calc_value.append(vals)
    return calc_value


def calc_overall(var_dict, values1):
    list_value = detect_value(values1)
    calc_values = get_value(values1, list_value)
    probability = []
    probabi = 0
    for values in calc_values:
        probs = []
        for key in values.keys():
            if find_pre_count(key) == 0:
                if values[key] == 1:
                    probs.append(var_dict[key][0][0])
                else:
                    probs.append(var_dict[key][0][1])
            else:
                parents = find_pre_counts(key)
                pro = []
                pro.append(values[key])
                for i in range(len(parents)):
                    if parents[i] in values:
                        pro.append(values[parents[i]])
                parents.insert(0, key)
                probs.append(calc_prob(pro, parents, var_dict[key]))
        count = 1
        for i in range(len(probs)):
            count *= probs[i]
        probability.append(count)
    for nums in probability:
        probabi += nums
    return probabi


f = open('burglarnetwork.txt', 'r')
line_count = 0
try:
    list1 = f.read().splitlines()
finally:
    f.close()
num = int(list1[0])
line_count += num + 4
variable = list1[2].split(" ")
G = nx.DiGraph()
for var in variable:
    G.add_node(var)
for i in range(num):
    a = list1[i+4].split(" ")
    for j in range(num):
        if a[j] is "1":
            G.add_edge(variable[i], variable[j])
line_count += 1
var_pro_dict = {}
for var in variable:
    count = find_pre_count(var)
    lin = 2 ** count
    list2 = []
    for i in range(line_count, line_count + lin):
        list3 = list1[i].split(" ")
        list4 = []
        for j in list3:
            list4.append(float(j))
        list2.append(list4)
    line_count += 1
    line_count += lin
    var_pro_dict[var] = list2
f = open('burglarqueries.txt', 'r')
try:
    list_query = f.read().splitlines()
finally:
    f.close()
list_queries = []
for i in range(len(list_query)):
    if list_query[i] is not "\n" and len(list_query[i])>1:
        list_queries.append(list_query[i].strip()[2:len(list_query[i].strip())-1])
outcomes = []
for query in list_queries:
    valus = {}
    for vars in variable:
        valus[vars] = -1
    valus[query.split(" | ")[0]] = 1
    names = query.split(" | ")[1].split(", ")
    for name in names:
        if name.split("=")[1] == "true":
            valus[name.split("=")[0]] = 1
        if name.split("=")[1] == "false":
            valus[name.split("=")[0]] = 0
    num1 = calc_overall(var_pro_dict, valus)
    valus[query.split(" | ")[0]] = 0
    num2 = calc_overall(var_pro_dict, valus)
    a1 = num1 / (num1 + num2)
    a2 = num2 / (num1 + num2)
    print(round(a1, 5), round(a2, 5))
    outcomes.append(str(round(a1, 5))+" "+str(round(a2, 5)))
with open("my_outcome.txt", 'w', encoding='utf-8') as file_object:
    for i in range(len(outcomes)):
        file_object.write("P("+list_queries[i]+")\n")
        file_object.write(outcomes[i])
        file_object.write('\n')
