#!/bin/python3
import re
import csv

def get_interface_list(nedata):
    regex = ('\t+"admin-status": "(.*)",\n'
             '\t+"port-reference-mkey": \[\n'
             '.*\n'
             '\t+\],\n'
             '\t+"name": "(.*)",\n')
    result_list_all = {}
    with open(nedata) as a:
        match = re.finditer(regex, a.read())
        if match:
            for m in match:
                int = m.group(2).replace('"',"")
                state = m.group(1)
                result_list_all[int] = state

        return(result_list_all)

def get_id_list(nedata):
    regex = ('\t+"name": "(.*)",\n'
              '\t+"created-when": .*\n'
              '\t+"basetype": "port",\n'
              '\t+"model-name": ".*",\n'
              '\t+"id": "(.*)"\n')
    result_list_id = {}
    with open(nedata) as a:
        match = re.finditer(regex, a.read())
        if match:
            for m in match:
                int = m.group(1)
                id = m.group(2)
                result_list_id[int] = id

    return(result_list_id)

def get_interface_list_up(nedata):
    result_list = {}
    result_list_up = {}
    result_list_all = get_interface_list(nedata)
    result_list_id = get_id_list(nedata)
    for int, state in result_list_all.items():
        for int_id, id in result_list_id.items():
            if int == int_id[4:]:
                result_list[int] = state, id
                for k, v in result_list.items():
                    if v == "up" or "up" in v:
                        result_list_up[k] = v
                    else:
                        pass

    return(result_list_up)

def get_card_list(nedata):
    cards = {}
    with open (nedata) as a:
        for line in a:
            if "model-name" in line and "A99" in line:
                card = line.split()[1].replace(',', '').replace('"', '')
            if "Rack 0" in line and not "/" in line and not "name" in line:
                slot = line.strip()
                cards [slot] = card
        return(cards)
                
def get_result(nedata,result_data):
    with open (result_data, "w"):
        result_list_up = get_interface_list_up(nedata)
        cards = get_card_list(nedata)
        for k,v in result_list_up.items():
            [v0, v2] = v
            for k1,v1 in cards.items():
                slot_number = re.search("\w+(\d)/(\d).*",k).group(2)
                if "Line" in k1:
                    cards_number = re.search('".* (\d)"',k1).group(1)
                    if slot_number == cards_number:
                        with open (result_data, "a") as a:a.write(f'''{v1:<15} - {k1:<20} :
                                            {k}, {v0}, {v2}''' + '\n')

get_result(r"C:\Users\e_yarotskov\AppData\Local\Programs\Python\Python38\Scripts\conf_parse_cisco\cisco\ne-data.txt", r"C:\Users\e_yarotskov\AppData\Local\Programs\Python\Python38\Scripts\conf_parse_cisco\cisco\ne-data2.txt")
