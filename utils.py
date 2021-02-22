import csv
import json
path = "C:/Users/95445/PycharmProjects/PredictCVSS/nvdcve-1.1-modified.json"


def get_vector_string_list():
    vector_string_list = []
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        cve_items = data['CVE_Items']
        for cve in cve_items:
            if cve['impact'].get('baseMetricV3'):
                # ID = cve['cve']['CVE_data_meta']['ID']
                vector_string = cve['impact']['baseMetricV3']['cvssV3']['vectorString']
                vector_string_list.append(vector_string)
    return vector_string_list


def convert_to_probability(vector_string):
    metrics_list = vector_string.split('/')
    AV = metrics_list[1].split(':')[1]
    AC = metrics_list[2].split(':')[1]
    PR = metrics_list[3].split(':')[1]
    UI = metrics_list[4].split(':')[1]
    S = metrics_list[5].split(':')[1]
    P_AV, P_AC, P_PR, P_UI= 0, 0, 0, 0
    if AV == 'N':
        P_AV = 0.85
    elif AV == 'A':
        P_AV = 0.62
    elif AV == 'L':
        P_AV = 0.55
    elif AV == 'P':
        P_AV = 0.2

    if AC == 'L':
        P_AC = 0.77
    elif AC == 'H':
        P_AC = 0.44

    if S == 'U':
        if PR == 'N':
            P_PR = 0.85
        elif PR == 'L':
            P_PR = 0.62
        elif PR == 'H':
            P_PR = 0.27
    elif S == 'C':
        if PR == 'N':
            P_PR = 0.85
        elif PR == 'L':
            P_PR = 0.68
        elif PR == 'H':
            P_PR = 0.50

    if UI == 'N':
        P_UI = 0.85
    elif UI == 'R':
        P_UI = 0.62

    # P = 2.11*P_AV*P_AC*P_PR*P_UI
    # return round(P, 2)
    return P_AV, P_AC, P_PR, P_UI

def get_probability_vector_list(vector_string_list):
    probability_vector_list = []
    for pv in vector_string_list:
        P_AV, P_AC, P_PR, P_UI = convert_to_probability(pv)
        P = round(2.11*P_AV*P_AC*P_PR*P_UI, 2)
        probability_vector_list.append([P_AV, P_AC, P_PR, P_UI, P])
    return probability_vector_list

vector_string_list = get_vector_string_list()
probability_vector_list = get_probability_vector_list(vector_string_list)
with open('C:/Users/95445/PycharmProjects/PredictCVSS/cve_vectors.csv', mode='w') as cve_vectors:
    writer = csv.writer(cve_vectors,lineterminator='\n')
    writer.writerows(probability_vector_list)