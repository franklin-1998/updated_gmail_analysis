import numpy as np
product_new = ['SO', 'MO', 'SO', 'CG', 'OG', 'SO', 'SO', 'SO', 'TS', 'CG', 'CG', 'SO', 'SO', 'PB', 'MO', 'BR', 'MO', 'SO', 'SO', 'MO', 'CG', 'CG', 'TS', 'CN', 'MO', 'MO', 'PB', 'CG', 'SO', 'RBO', 'CG', 'C&B', 'CSO', 'SO', 'CN', 'DS', 'CSO', 'CB', 'MO', 'CG', 'SO', 'C&B', 'MDN', 'C&B', 'SO', 'CN', 'CSO', 'C&B', 'C&B', 'SO', 'CG', 'MO', 'RBO', 'CG', 'D&LCB', 'SO', 'PP', 'SO', 'C&B', 'C&B', 'MO', 'SO', 'OG', 'PC', 'PB', 'SC', 'PB', 'BO', 'CN', 'AB', 'CG', 'MO', 'PB', 'PB', 'BO', 'PB', 'CSO', 'PB', 'CG', 'RBO', 'SO', 'SO', 'RBO', 'BR', 'MC', 'MO', 'OSO', 'CB', 'BR', 'CN', 'CG', 'SO', 'C&B', 'MC', 'CFC', 'PC', 'C&B', 'RM', 'CN', 'CN', 'MC', 'SO', 'RC', 'PN', 'CB', 'MC', 'BB', 'RBO', 'RM', 'MC', 'PB', 'IS', 'DW', 'SO', 'RBO', 'MO', 'GO', 'GO', 'CG',
'C&B', 'CN', 'RTCM', 'PB', 'MC', 'C&B', 'C&B', 'BB', 'CN', 'MS', 'CN', 'GO', 'BG', 'SO', 'BS', 'PC', 'BR', 'MC', 'MC', 'SO', 'CCDF', 'PN', 'CG', 'MP', 'CG', 'CW', 'CG', 'PO', 'RBO', 'CG', 'RM', 'DC', 'PC', 'C&B', 'PN', 'GM', 'BR', 'BR', 'BR', 'SO', 'SO', 'CG', 'MO', 'DS', 'BR', 'CG', 'MC', 'SO', 'PN', 'RC', 'BR', 'CN', 'MN', 'CN', 'PN', 'CN', 'SO', 'FS', 'RBO', 'CN', 'J(', 'C&P', 'GO', 'GO', 'SO', 'D&LCB', 'MS', 'H&ERM', 'GM', 'AC', 'SO', 'SO', 'PO', 'PB', 'C&B', 'DC', 'POO', 'CB', 'BG', 'MO', 'MR', 'CS', 'CF', 'M&FM', 'CN', 'SS', 'PB', 'GO', 'RM', 'BR', 'RC', 'MO', 'AB', 'AB', 'SS', 'AC', 'SO', 'PB', 'PB', 'MO', 'CN', 'RM', 'OG', 'DC', 'D&LCB', 'CSO', 'SO', 'RO', 'CS', 'RBO', 'RS', 'CB', 'PN', 'CG', 'MF', 'FJ', 'PN', 'TS', 'RN',
'CN', 'POO', 'AB', 'C&B', 'C&B', 'KMP', 'MN', 'BG', 'POO', 'MN', 'SC', 'DS', 'RN', 'AB', 'DC', 'PB', 'C&P', 'SO', 'POO', 'PP', 'FS', 'VO', 'GO', 'AC', 'SC', 'EVOO', 'CF', 'CF', 'PN', 'BS', 'CN', 'MO', 'RTCM', 'BR', 'VCO', 'PS', 'SO', 'CF', 'CG', 'GO', 'CG', 'H&ERM', 'TS', 'EVOO', 'PO', 'WF', 'PB', 'TS', 'FJ', 'DC', 'C&B', 'C&B', 'RS', 'DC', 'MO', 'CB', 'POO', 'PB', 'SC', 'BR', 'POO', 'DS', 'SO', 'PN', 'SC', 'MC', 'RC']


def unique(list1): 
  
    # intilize a null list 
    unique_list = [] 
      
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    print(unique_list)

unique(product_new)