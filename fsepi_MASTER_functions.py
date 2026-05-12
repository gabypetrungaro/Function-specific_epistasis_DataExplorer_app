#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 11:48:23 2021

@author: gaby
"""
import numpy as np
import os
import pandas as pd
import pickle
from datetime import datetime
import re
import glob
# =============================================================================
# Functions used only for analysis that start from the really RAW data (as it comes from the robot)
# usually run only once for each experiment, at the beggining -- I copied them here on 7.2.2025 from 
# the latest versions of my_py_functions_morbidostat_analysis_10122020 or from my_gral_functions
# def dataframeto1row(dataframe):
#     df_out = dataframe.stack()
#     df_out.index = df_out.index.map('{0[0]}{0[1]}'.format)
#     data_onerow = df_out.to_frame().T
#     return data_onerow
# def gettime_fromfilename(file):
#     match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}', file)
#     date_time = datetime.strptime(match.group(), '%Y-%m-%d %H-%M-%S')
#     return date_time
# def load_multiple_OD_read_files_into_dataframe(OD_csv_files_to_merge):
#     dataframes_to_concat = []
#     for file1 in OD_csv_files_to_merge:
#         one_row_dataframe = dataframeto1row(pd.read_csv(file1, header=1, nrows=13, usecols=range(1,13), sep = '\t'))
#         one_row_dataframe['date_time'] = gettime_fromfilename(file1)
#         folder, filename1 = os.path.split(file1)
#         one_row_dataframe['original_ODfile'] = filename1
#         dataframes_to_concat.append(one_row_dataframe)
#     new_dataframe = pd.concat(dataframes_to_concat, ignore_index=True).sort_values(by=['date_time'])
# #    add_relevant_timecols(new_dataframe, 'date_time') ##---> comented here, not in original
#     return new_dataframe.reset_index(drop=True)
# def gettime_fromfilename_yearlast(file):
#     match = re.search(r'\d{2}-\d{2}-\d{4} \d{2}-\d{2}-\d{2}', file)
#     date_time = datetime.strptime(match.group(), '%d-%m-%Y %H-%M-%S')
#     return date_time
# def load_multiple_ABconc_files_into_dataframe(AB_csv_files_to_merge):
#     dataframes_to_concat = []
#     for file1 in AB_csv_files_to_merge:
#         one_row_dataframe = dataframeto1row(pd.read_csv(file1, header=0, nrows=13, usecols=range(0,13), index_col = 0, sep =','))
#         one_row_dataframe['date_time'] = gettime_fromfilename_yearlast(file1)
#         folder, filename1 = os.path.split(file1)
#         one_row_dataframe['original_file'] = filename1
#         dataframes_to_concat.append(one_row_dataframe)
#     new_dataframe = pd.concat(dataframes_to_concat, ignore_index=True).sort_values(by=['date_time'])
#     return new_dataframe.reset_index(drop=True)
# def import_all_raw_data(exp_folder, exp_info, plate):
#     data_folder = f'{exp_folder}/data/'
#     OD_files_folder = f'{data_folder}{exp_info["exp_ini_date"]}_Plate_{plate}'
#     current_AB_folder = os.path.join(data_folder,'current_AB')
#     print('importing OD data from ', OD_files_folder)
#     all_OD_files = glob.glob(OD_files_folder+'/*.csv')
#     all_OD_files.sort(key=os.path.getmtime)
#     all_data = load_multiple_OD_read_files_into_dataframe(all_OD_files)
#     print('imported data')
#     print('importing concentrations data from ', current_AB_folder)
#     AB_conc_files = glob.glob(os.path.join(current_AB_folder,f'c_target_real*_{plate}_*.csv'))
#     all_AB_dataframe = load_multiple_ABconc_files_into_dataframe(AB_conc_files)
#     print('imported antibiotic update data')
#     return all_data, all_AB_dataframe
# # =============================================================================
# # My functions for adaptive background substraction
# def strain_wells_list(plate_layout, strain):
#     """ I give you the strain you tell me the wells that contain that strain"""
#     all_wellss = [f'{i}{j}' for i in 'ABCDEFGH' for j in range(1,13)]
#     return [w for w in all_wellss if plate_layout.loc[w[0], w[1:]]==strain]
# def well_strain(plate_layout, well): ##added on 12.04.2025
#     """ I tell you the well, you tell me what strain is there"""
#     return dataframeto1row(plate_layout).loc[0,:].to_dict()[well]
# def calculate_bg_from_LBwells(LB_dataframe_dil, pars_bg=0.046, min_OD=0.03, max_OD=0.05):
# #     print(LB_dataframe_dil[LB_dataframe_dil.columns[:-1]])
#     sums = (LB_dataframe_dil[LB_dataframe_dil.columns[:-1]]>max_OD).sum()
#     LB_keep = LB_dataframe_dil[LB_dataframe_dil.columns[:-1]][sums[sums<2].keys()]
#     if np.size(LB_keep) <1:
#         bkg = pars_bg
#     else:
#         bkg = np.round(LB_keep.values.mean(),4)
#     if bkg>max_OD or bkg<min_OD or np.isnan(bkg):
#         bkg = pars_bg
#     return np.repeat(bkg, len(LB_dataframe_dil))
# def data_slice_prev_to_dilution(all_data_bg_sub, dilutions, dil_num):
#     data_slice = all_data_bg_sub.copy()
#     data_slice = data_slice[(data_slice['date_time']>=dilutions[dil_num - 1]) & (data_slice['date_time']<dilutions[dil_num])]
#     return data_slice
# def create_bgs_list(layout,ODdata, dilutions):
#     empty_wells = set(strain_wells_list(layout,'LB'))#set([])
#     columns = list(empty_wells)
#     columns.append('date_time')
#     LB_dataframe = ODdata.copy().loc[:,columns ]
#     bgs_list = []
#     for dil_num in list(dilutions.index[1:]):
#         LBdata_1dil = data_slice_prev_to_dilution(LB_dataframe, dilutions, dil_num)
#         bg=calculate_bg_from_LBwells(LBdata_1dil)
#         #print('bg =',bg)
#         bgs_list.append(bg)
#     if len(LB_dataframe[LB_dataframe['date_time']>dilutions.iloc[-1]])>0:
#         LBdata_lastdil=LB_dataframe[LB_dataframe['date_time']>dilutions.iloc[-1]]
#         bgs_list.append(calculate_bg_from_LBwells(LBdata_lastdil))
#     return bgs_list
# def substract_bg(ODdata,bgs_list):
#     bgs=np.hstack(bgs_list)
#     #bg subtraction
#     ODdata_bgsub = ODdata.copy()
#     ODdata_bgsub.iloc[:,:96] = ODdata_bgsub.iloc[:,:96].subtract(bgs, axis="rows")
#     ODdata_bgsub.iloc[:,:96] = ODdata_bgsub.iloc[:,:96][ODdata_bgsub.iloc[:,:96]>0]
#     print('substracted background, from list of bgs')
#     return ODdata_bgsub
# # =============================================================================
# #checked functions
# def read_params(path_params_file):
#     f = open(path_params_file,'r')
#     lines = f.readlines()
#     params_dic = {}
#     for line in lines:
#         if line[0:3]=='num':
#             (key, val) = line.split()
#             params_dic[key] = int(val)
#         if line[0:2]=='CM' or line[0:2]=='c0' or line[0:6]=='factor' or line[0:6]=='OD_thr' or line[0:9]=='steepness' or line[0:6]=='OD_max' or line[0:3]=='bkg':
#             (key, val) = line.split()
#             params_dic[key] = float(val)
#         if line[0:5]=='units' or line[0:4]=='date'or line[0:4]=='anti':
#             (key, val) = line.split()
#             params_dic[key] = val
#     return params_dic
def read_plates_layout(data_folder, exp_ini_date, names='yes'):
    plates_info_file = f'{data_folder}/CurrentExperiment_info/Plates_info_{exp_ini_date}.txt'
    plates_info = pd.read_csv(plates_info_file, header=0, sep=' ', dtype=str)
    layouts = {}
    for plate_name in plates_info.loc[:,'Plate']:
        plate_layout_number = plates_info.loc[plates_info['Plate'] == plate_name, 'PlateLayoutFile'].iloc[0]
        plate_layout_number = plate_layout_number[plate_layout_number.index('plate')+len('plate'):plate_layout_number.index('_')]
        #Adaptation to be able to read plate layouts from both raw data experiment folder and Resuls_... folder
        #(I have copied the plates layout to the results folder to have them there for the analysis and do not touch EXPERIMENTS folder anymore after first analysis)
        if 'Results' in data_folder:
            if names=='yes':
                plate_layout_file = os.path.join(f'{data_folder}/TF_plate_layouts_strain_names','plate'+plate_layout_number+'_'+plate_name+'_layout_'+exp_ini_date+'.csv')
            else:
                plate_layout_file = os.path.join(f'{data_folder}/plate_layouts','plate'+plate_layout_number+'_'+plate_name+'_layout_'+exp_ini_date+'.csv')
        else:
            plate_layout_file = os.path.join(f'{data_folder}/data/current_AB','plate'+plate_layout_number+'_'+plate_name+'_layout_'+exp_ini_date+'.csv')
        plate_layout = pd.read_csv(plate_layout_file, header=0, index_col=0, nrows=13, usecols=range(0,13))
        layouts[plate_name] = plate_layout
    return plates_info, layouts
# def read_antibiotic_layout(plates_info, current_AB_folder, exp_ini_date):
#     layouts = {}
#     for i, plate_name in enumerate(np.sort(plates_info)):
#         plate_layout_file = os.path.join(current_AB_folder,f'antibiotics_plate{i+1}_{plate_name}_layout_{exp_ini_date}.csv')
#         plate_layout = pd.read_csv(plate_layout_file, header=0, index_col=0, nrows=13, usecols=range(0,13))
#         layouts[plate_name] = plate_layout
#     return layouts
# # =============================================================================
def load_data_one_plate(exp_folder, plate, min_OD_exp, max_OD_exp):
    filename = f'ODdata_bg_sub_with_exptime_plate{plate}.csv'
    ODdata = pd.read_csv(f'{exp_folder}/data/'+filename, sep='\t', index_col=0)
    filename = f'ABconc_with_exptime_plate{plate}.csv'
    ABdata = pd.read_csv(f'{exp_folder}/data/'+filename, sep='\t', index_col=0)
    filename = f'growth_rates_minODexpfit{min_OD_exp}_maxODexpfit_{max_OD_exp}_NOTnorm_plate{plate}.csv'
    full_gr_df = pd.read_csv(f'{exp_folder}/data/'+filename, sep=',', index_col=0)
    return plate, ODdata, ABdata, full_gr_df
# def substract_ini_time(df):
#     df['date_time'] = pd.to_datetime(df['date_time'])
#     df_ini_date = df.loc[df.index[0], 'date_time'] 
#     df['exp_time'] = df.loc[:,['date_time'] ].apply(lambda row: row-df_ini_date) # == global time and local time bc only one block
#     df['time[h]'] = df['exp_time'].apply(lambda row: row.total_seconds()/3600) #add redundant columns with times in hours and minutes that are useful to plot
#     df['time[mins]'] = df['exp_time'].apply(lambda row: row.total_seconds()/60) #add redundant columns with times in hours and minutes that are useful to plot
#     print('substracted ini_time')
#     return df
# # --- used in update function ---
# def x_y_transformed_1well(data_as_dataframe_positiveOD_bgsub_ODmax, well):
#     y = np.array(np.log(data_as_dataframe_positiveOD_bgsub_ODmax[well]))
#     x = np.array(data_as_dataframe_positiveOD_bgsub_ODmax['time[mins]'])
#     ypos = y - min(y)
#     #print(ypos)
#     if any(ypos<0):
#         print('obs, ypos has negative values!')
#     return x, ypos
# def Ac_gc_1well(x, ypos):
#     Ac = np.trapz(ypos, x) ###AREA under positive curve
#     estimated_gc = 2*Ac / (x[-1]-x[0])**2
#     return Ac, estimated_gc
# def factor_gc_1well(well, gc, n): ## this is the one for TMP experiment, see cuaderno 12.02.2025
#     g0 = 0.02
#     if gc >= g0 :
#         factor = 1.5 ## if it is growing too much, increase the concentration by 1.5 (update with doseresponse would be negative or inf) #0 #later I say the ones that are zero concentration set to basal c0
#     else:
#         factor = (gc/(g0-gc))**(1/n)
#     if factor > 5:
#         factor = 5 #maximum increase is to multiply by 5
#     return well, factor
# def update_func_results_1well_1dil(before_dil_data, well, max_OD, n):
#     """encapsulate in function -- mimic of update function that actually was used in the TMP experiment"""
#     aux_dataframe = before_dil_data.copy()
#     aux_dataframe = aux_dataframe[aux_dataframe[well]>0]
#     aux_dataframe = aux_dataframe[aux_dataframe[well]<max_OD]
#     try:    
#         if aux_dataframe.loc[aux_dataframe.index[0],well]>= aux_dataframe.loc[aux_dataframe.index[1],well]:
#             print(f'well {well}: removed first point')
#             aux_dataframe[well] = aux_dataframe[well][aux_dataframe.index>aux_dataframe.index[0]]
#         aux_dataframe = aux_dataframe[aux_dataframe[well].notna()]
#         #
#         xx, yy = x_y_transformed_1well(aux_dataframe, well)    
#         if len(xx)<3:
#             xx = aux_dataframe['time[h]']
#             yy = np.zeros(len(xx))
#             Ac = 0
#             gc = 0
#             factor = 1
#             print('not enough OD values')
#         else:
#             Ac, gc = Ac_gc_1well(xx, yy)
#             well, factor = factor_gc_1well(well, gc, n)
#     #     #mtx_factors[np.int(well[1:])][well[0]] = factor
#     except IndexError:
#         factor=1
#         xx = aux_dataframe['time[h]']
#         yy = np.zeros(len(xx))
#         Ac = 0
#         gc = 0
#         print('IndexError for well '+str(well)+' not enough OD values -- cells no-growth or have died?')
#     except ValueError:
#         factor=1
#         xx = aux_dataframe['time[h]']
#         yy = np.zeros(len(xx))
#         Ac = 0
#         gc = 0
#         print('ValueError for well '+str(well)+' Probably empty, no positive values of OD because cells have died?')
#     data_used_in_update_func = aux_dataframe
#     return data_used_in_update_func,xx,yy,Ac, gc,factor
# def Ac_gc_only_from_update_func_1well_1dil(before_dil_data, well, max_OD):#, n): #do not calculate factor
#     """encapsulate in function -- mimic of update function that actually was used in the TMP experiment"""
#     aux_dataframe = before_dil_data.copy()
#     aux_dataframe = aux_dataframe[aux_dataframe[well]>0]
#     aux_dataframe = aux_dataframe[aux_dataframe[well]<max_OD]
#     try:    
#         if aux_dataframe.loc[aux_dataframe.index[0],well]>= aux_dataframe.loc[aux_dataframe.index[1],well]:
#             print(f'well {well}: removed first point')
#             aux_dataframe[well] = aux_dataframe[well][aux_dataframe.index>aux_dataframe.index[0]]
#         aux_dataframe = aux_dataframe[aux_dataframe[well].notna()]
#         #
#         xx, yy = x_y_transformed_1well(aux_dataframe, well)    
#         if len(xx)<3:
#             xx = aux_dataframe['time[h]']
#             yy = np.zeros(len(xx))
#             Ac = 0
#             gc = 0
#             # factor = 1
#             print('not enough OD values')
#         else:
#             Ac, gc = Ac_gc_1well(xx, yy)
#             # well, factor = factor_gc_1well(well, gc, n)
#     #     #mtx_factors[np.int(well[1:])][well[0]] = factor
#     except IndexError:
#         # factor=1
#         xx = aux_dataframe['time[h]']
#         yy = np.zeros(len(xx))
#         Ac = 0
#         gc = 0
#         print('IndexError for well '+str(well)+' not enough OD values -- cells no-growth or have died?')
#     except ValueError:
#         # factor=1
#         xx = aux_dataframe['time[h]']
#         yy = np.zeros(len(xx))
#         Ac = 0
#         gc = 0
#         print('ValueError for well '+str(well)+' Probably empty, no positive values of OD because cells have died?')
#     data_used_in_update_func = aux_dataframe
#     return data_used_in_update_func,xx,yy,Ac, gc#,factor
# # -------------------------------
# def fit_gc_1well_ODrange(data_slice,well,min_OD_exp,max_OD_exp):
#     to_fit_data = data_slice.copy()
#     to_fit_data[well] = data_slice[well][(data_slice[well]>min_OD_exp) & (data_slice[well]<max_OD_exp)]
#     if to_fit_data.loc[to_fit_data.index[0],well]>= to_fit_data.loc[to_fit_data.index[1],well]:
#         print(f'well {well}: removed first point')
#         to_fit_data[well] = to_fit_data[well][to_fit_data.index>to_fit_data.index[0]]
#     to_fit_data = to_fit_data[to_fit_data[well].notna()]
#     if len(to_fit_data)<3:
#         print(f'well {well} not enough OD values in range to fit')
#         slope = 0
#         ordn = 0
#         r_squared = 0 #added 11.02.2025
#     else:
#         y=np.log(to_fit_data[well])
#         x=to_fit_data['time[h]']
#         slope, ordn = np.polyfit(x,y,1 )
#         y_pred = np.polyval([slope,ordn], x) #added 11.02.2025
#         # Calculate R-squared
#         ss_res = np.sum((y - y_pred) ** 2)  # Residual sum of squares
#         ss_tot = np.sum((y - np.mean(y)) ** 2)  # Total sum of squares
#         r_squared = 1 - (ss_res / ss_tot)
#     return to_fit_data, slope, ordn, r_squared
# def calculate_growth_rates(all_data_bg_sub, empty_wells, dilutions, min_OD, max_OD):#, steepness):
#     """" returns dic --- obs: grates are not normalized"""
#     all_wells = set([f'{i}{j}' for i in 'ABCDEFGH' for j in range(1,13)])
#     inoc_wells = all_wells - empty_wells
#     gr_rates_dic = {f'{w}_gr_fit': [] for w in all_wells}
#     gr_rates_dic.update({f'{w}_ord_fit': [] for w in all_wells})
#     gr_rates_dic.update({f'{w}_R2_fit': [] for w in all_wells})
#     gr_rates_dic.update({f'{w}_gr_area': [] for w in all_wells})
#     gr_rates_dic.update({f'{w}_Area': [] for w in all_wells})
#     gr_rates_dic.update({'time[h]':[]})
#     gr_rates_dic.update({'dilution_number':[]})
#     for dil_num in list(dilutions.index[1:]):
#         data_slice = data_slice_prev_to_dilution(all_data_bg_sub,dilutions,dil_num)
#         tm = data_slice.loc[data_slice.index[-1], 'time[h]']#max(xx)/60 #time to which I will assign the growth rate, in hours
#         gr_rates_dic['time[h]'].append(tm)
#         gr_rates_dic['dilution_number'].append(dil_num)
#         for well in inoc_wells:
#             # data_used_in_update_func, xx,yy, Ac, gc, factor = update_func_results_1well_1dil(data_slice, well, max_OD, steepness)
#             data_used_in_update_func, xx,yy, Ac, gc = Ac_gc_only_from_update_func_1well_1dil(data_slice, well, max_OD)
#             to_fit_data, g_fit, ordn, r_squared = fit_gc_1well_ODrange(data_slice,well,min_OD,max_OD)
#             gr_rates_dic[f'{well}_gr_fit'].append(g_fit/60 )
#             gr_rates_dic[f'{well}_ord_fit'].append(ordn)
#             gr_rates_dic[f'{well}_R2_fit'].append(r_squared) #added 11.02.2025
#             gr_rates_dic[f'{well}_gr_area'].append(gc)
#             gr_rates_dic[f'{well}_Area'].append(Ac)
#     return gr_rates_dic   
def import_strain_names_as_dataframe(data_dir, motherplates):
    df = pd.DataFrame()
    for mother_plate in motherplates:
        df_toap = pd.read_csv(f'{data_dir}/fsepi_data/strain_names_plate_{mother_plate}.csv', usecols = [0,1])
        df_toap['mother_plate'] = mother_plate
        df = df._append(df_toap)
    df = df.set_index('gene-deletion')
    return df
# def strain_num_and_motherplate_to_name(strainsdf, str_num, motherplate):
#     return strainsdf['gene-deletion'][(strainsdf['strain']==str_num) & strainsdf['mother_plate']==motherplate]