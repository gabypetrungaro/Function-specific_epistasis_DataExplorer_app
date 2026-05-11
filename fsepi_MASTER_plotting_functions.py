#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 18:59:47 2021

@author: gaby
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly
import os

# def asign_colors_to_strains(strains):
#     """ create a dictionary {strain:color} with one color per strain in strains """
#     colors = [plt.cm.rainbow(x) for x in np.linspace(0, 1, len(strains))]
#     # colors = [plt.cm.viridis(x) for x in np.linspace(0, 1, len(strains))]
#     strain_color = {strain:color for strain, color in zip(strains, colors)}
#     return strain_color
# def asign_strain_color_to_wells(plate_layout, strain_color):
#     """ create a dictionary {well:color} with one color per strain in the plate_layout dataframe -- receives dic strain_color={strain:color}"""
#     col_dic= {}
#     for strain in strain_color.keys():
#         all_wells = np.array(plate_layout.stack().index.map('{0[0]}{0[1]}'.format))
#         strain_wells = [w for w in all_wells if plate_layout.loc[w[0], w[1:]]==strain]
#         d = {well : strain_color[strain] for well in strain_wells}
#         col_dic.update(d)
#     well_color = col_dic.copy()
#     return well_color
# # =============================================================================
# # Plotting functions
# # =============================================================================
# def AB_vs_time(ax1, all_data_bg_sub, all_AB_dataframe, pl_wells, well_color, well_strain, xmin=0, xmax=600, ymin=10**-1, ymax=500):
#     done=[]
#     for well1 in pl_wells:
#         done=list(set(done))
#         ax1.step(all_AB_dataframe['time[h]'], all_AB_dataframe[well1],where='post', color=well_color[well1], label=well_strain[well1] if well_strain[well1] not in done else '')
#         ax1.semilogy(all_AB_dataframe['time[h]'], all_AB_dataframe[well1], 'o', markersize=3, color=well_color[well1])
#         done.append(well_strain[well1])    
#     ax1.set_xlim((xmin, xmax))
#     ax1.grid()
#     # ax1.set_ylim(10**-2,2*10**3)
#     ax1.set_ylim(ymin,ymax)
# def OD_AB_both_gr_vs_time(ax_list, all_data_bg_sub, all_AB_dataframe, pl_wells, well_color, well_strain, gr_rates_dic, antibiotic = 'antibiotic', timerange = (0,600),g0=0.02):
#     done=[]
#     for well1 in pl_wells:
#         done=list(set(done))
#         ax_list[0].semilogy(all_data_bg_sub['time[h]'], all_data_bg_sub[well1], color=well_color[well1], label=well_strain[well1] if well_strain[well1] not in done else '')
#         done.append(well_strain[well1])    
#         ax_list[1].step(all_AB_dataframe['time[h]'], all_AB_dataframe[well1],where='post', color=well_color[well1])
#         ax_list[1].semilogy(all_AB_dataframe['time[h]'], all_AB_dataframe[well1], 'o', markersize=3, color=well_color[well1], label='real [antibiotic]')
#         ax_list[2].plot(gr_rates_dic['time[h]'], np.array(gr_rates_dic[f'{well1}_gr_fit'])/g0,'-o',color=well_color[well1], markersize=3)
#         ax_list[3].plot(gr_rates_dic['time[h]'], np.array(gr_rates_dic[f'{well1}_gr_area'])/g0,'-o',color=well_color[well1], markersize=3)   
#     ax_list[0].set_xlim(timerange)
#     for i in range(len(ax_list)-1):
#         ax_list[i].set_xticks([])
#         ax_list[i].get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
#     ax_list[1].grid()
#     ax_list[1].set_xlim(timerange)
#     ax_list[1].set_ylim(10**-1,2*10**3)
#     # ax_list[2].set_xlim(timerange)
#     # ax_list[3].set_xlim((xmin, xmax))
#     ax_list[2].set_ylim((0,1) )
#     ax_list[3].set_ylim((0,1) )
#     # ax_list[2].hlines(0.5, xmin,xmax)
#     # ax_list[3].hlines(0.5, xmin,xmax)
#     ax_list[0].set_ylabel('OD', fontsize=14)
#     ax_list[1].set_ylabel(f'{antibiotic} [ug/ml]',fontsize=14)
#     ax_list[2].set_ylabel('Normalized growth rate\n (linear fit)', fontsize=14)
#     ax_list[3].set_ylabel('Normalized growth rate\n (Area estimation)', fontsize=14)
#     ax_list[3].set_xlabel('time[h]', fontsize=14)
#     ax_list[0].set_ylim((10**-3,1) )
#     #ax_list[0].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=10, mode="expand", borderaxespad=0., fontsize=16)
# def OD_AB_gr_fit_vs_time(ax_list, all_data_bg_sub, all_AB_dataframe, pl_wells, well_color, well_strain, gr_rates_dic, xmin=0, xmax=300, g0=0.02):
#     done=[]
#     for well1 in pl_wells:
#         done=list(set(done))
#         ax_list[0].semilogy(all_data_bg_sub['time[h]'], all_data_bg_sub[well1], '-o',markersize=3, color=well_color[well1], label=well_strain[well1] if well_strain[well1] not in done else '')
#         done.append(well_strain[well1])    
#         ax_list[1].step(all_AB_dataframe['time[h]'], all_AB_dataframe[well1],where='post', color=well_color[well1])
#         ax_list[1].semilogy(all_AB_dataframe['time[h]'], all_AB_dataframe[well1], 'o', markersize=3, color=well_color[well1], label='real [NIT]')
#         ax_list[2].plot(gr_rates_dic['time[h]'], np.array(gr_rates_dic[f'{well1}_gr_fit'])/g0,'-o', markersize=3,color=well_color[well1])
#     ax_list[0].set_xlim((xmin, xmax))
#     ax_list[1].grid()
#     ax_list[1].set_xlim((xmin, xmax))
#     ax_list[1].set_ylim(10**-3,2*10**3)
#     ax_list[2].set_xlim((xmin, xmax))
#     ax_list[2].set_ylim((0,1.2) )
#     ax_list[2].hlines(0.5, xmin,xmax)
#     ax_list[0].set_ylabel('OD', fontsize=14)
#     ax_list[1].set_ylabel('NIT [ug/ml]',fontsize=14)
#     ax_list[2].set_ylabel('Normalized growth rate\n (linear fit)', fontsize=14)
#     ax_list[0].set_ylim((10**-3,1) )
#     #ax_list[0].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=10, mode="expand", borderaxespad=0., fontsize=16)
# # =============================================================================
# # Revised
# # =============================================================================
def strain_to_plate_and_wells(strain_name, layouts, motherplates_dic, strainsdf):
    all_wells = [f'{i}{j}' for i in 'ABCDEFGH' for j in range(1,13)]
    strain_plate_wells_dic = {}
    if strain_name == 'lacA':
        strain = strain_name
        plates = layouts.keys()
    else:
        strain = strainsdf.loc[strain_name,:].values[0]
        plates = motherplates_dic[strainsdf.loc[strain_name,:].values[1]]
    for plate in plates:#list(layouts.keys())[:3]: #layouts.keys(): #---- change to include all plates!
        plate_layout = layouts[plate]
        well_strain = {w:plate_layout.loc[w[0],w[1:]] for w in all_wells}
        strain_wells=[w for w in all_wells if well_strain[w]==strain]#inoc_wells
        strain_plate_wells_dic[plate] = strain_wells
    return strain_plate_wells_dic
def OD_AB_gr_fit_vs_time_1strain_allreplicates(strain_name, ODdata, ABdata, full_gr_dic, layouts, motherplates_dic, strainsdf, g0=0.02, tmax=600, ABylabel = 'drug concentration', seq_results = {}):
    # colors = plotly.colors.DEFAULT_PLOTLY_COLORS
    # ref_strain_wells = strain_to_plate_and_wells('lacA',layouts)
    # strain_plate_and_well = strain_to_plate_and_wells(strain, layouts)
    # new_line = '<br>'
    ref_strain_wells = strain_to_plate_and_wells('lacA', layouts, motherplates_dic, strainsdf)
    strain_plate_and_well = strain_to_plate_and_wells(strain_name, layouts, motherplates_dic, strainsdf)
    colors = [matplotlib.colors.rgb2hex(plt.cm.rainbow(x)[:-1]) for x in np.linspace(0, 1, len(list(strain_plate_and_well.values())[0])*9+2)]
    #colors = [plt.cm.rainbow(x)[:-1] for x in np.linspace(0, 1, len(list(strain_plate_and_well.values())[0])*9+2)]
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing = 0.05)
    i=0
    j=0
    if strain_name !='lacA':
        for plate in ref_strain_wells.keys():
            df_OD = ODdata[plate]
            df_AB = ABdata[plate]
            gr_dic = full_gr_dic[plate]
            for well in ref_strain_wells[plate]:
                if j==0:
                    boolean = True
                else:
                    boolean = False
        #         i=i+1 #if I want to turn off the lacA replicates one by one
                fig.add_trace(go.Scatter( x=df_AB['time[h]'],y=df_AB[well],
    
                    legendgroup=f"group{i}",
                    name="lacA (all rep)",
                    mode="lines+markers",
                     line=dict(color='lightgrey', shape='hv'),
                     showlegend=boolean
                    ), row=2, col=1)
                j=j+1
    j=0
    for plate in strain_plate_and_well.keys():
        df_OD = ODdata[plate]
        df_AB = ABdata[plate]
        gr_dic = full_gr_dic[plate]
        # mut_info = ['no info']
        for well in strain_plate_and_well[plate]:
            # mut_info = [tup[1] for tup in seq_results[(strain_name, plate, well)]]
            i=i+1
            j=j+1
            fig.add_trace(go.Scatter( x=df_OD['time[h]'],y=df_OD[well],

                legendgroup=f"group{i}",
                # name=f"{plate,well},{new_line}{new_line.join(map(str, mut_info))}",
                name=f"{plate,well}",
                mode="lines+markers",
                 line=dict(color=colors[j]),
                ), row=1, col=1)
            fig.add_trace(go.Scatter( x=df_AB['time[h]'],y=df_AB[well],

                legendgroup=f"group{i}",
                name=f"{plate,well}",
                mode="lines+markers",
                 line=dict(color=colors[j], shape='hv'),
                showlegend=False
                ), row=2, col=1,)
            fig.add_trace(go.Scatter( x=gr_dic['time[h]'],y=np.array(gr_dic[f'{well}_gr_fit'])/g0,

                legendgroup=f"group{i}",
                name=f"{plate,well}",
                mode="lines+markers",
                 line=dict(color=colors[j]),
                showlegend=False
                ), row=3, col=1)
    fig.update_layout(title=f'{strain_name}', title_x=0.5,
        autosize=False,
        width=800,
        height=800,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ))
    fig.update_traces(marker_size=3)
    fig.update_yaxes(type="log", range=[-3,0], row=1,col=1, title = 'OD')
    fig.update_xaxes(title = 'time[h]', row=3, col=1)
    fig.update_yaxes(type="log", range=[np.log10(0.01),np.log10(3000)],showexponent = 'all',
            exponentformat = 'power', title=f'{ABylabel}[ug/ml]', row=2,col=1)
    fig.update_yaxes(title='normalized growth rate ', range=[0,1.1], row=3,col=1)
    # fig.update_xaxes(title = 'time[h]', row=2, col=1)
    fig.update_xaxes(range=[0,tmax])
    return fig
# def OD_AB_gr_fit_vs_time_1well(ax_list, all_data_bg_sub, all_AB_dataframe, well1, gr_rates_dic,timerange=(0,300), g0=0.02, antibiotic = 'antibiotic'):
#     ax_list[0].semilogy(all_data_bg_sub['time[h]'], all_data_bg_sub[well1], '-o',markersize=3)
#     ax_list[1].step(all_AB_dataframe['time[h]'], all_AB_dataframe[well1],where='post')
#     ax_list[1].semilogy(all_AB_dataframe['time[h]'], all_AB_dataframe[well1], 'o', markersize=3)
#     ax_list[2].plot(gr_rates_dic['time[h]'], np.array(gr_rates_dic[f'{well1}_gr_fit'])/g0,'-o', markersize=3)
#     ax_list[0].set_xlim(timerange)
#     ax_list[0].grid()
#     ax_list[1].grid()
#     ax_list[2].grid()
#     # ax_list[1].set_xlim((xmin, xmax))
#     ax_list[1].set_ylim(10**-3,2*10**3)
#     # ax_list[2].set_xlim((xmin, xmax))
#     ax_list[2].set_ylim((0,1.2) )
#     ax_list[2].hlines(0.5, timerange[0], timerange[1],'k')
#     ax_list[0].set_ylabel('OD', fontsize=14)
#     ax_list[1].set_ylabel(f'{antibiotic}[ug/ml]',fontsize=14)
#     ax_list[2].set_ylabel('Normalized growth rate\n (linear fit)', fontsize=14)
#     ax_list[0].set_ylim((10**-3,1) )
#     #ax_list[0].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=10, mode="expand", borderaxespad=0., fontsize=16)
def plate_overwiew_2ys(y1, y1_name, ABdata, layouts, plate, platenum_to_motherplate, strainsdf, g0=0.02, y1_lines=True, ABres_lines=False, cm1end =0, cm2end=0, ABylims=(10**-3,2000), xmin=0, xmax=600, ABylabel = '[antibiotic]'):
    y1_1plate = y1[plate]
    ABdata_1plate = ABdata[plate]
    all_wells = [f'{i}{j}' for i in 'ABCDEFGH' for j in range(1,13)]
    if y1_name == 'OD':
        scale = 'log'
        dic_key = ''
        normalization = 1
        y1lims = (5*10**-3,1)
        yticks = [10**-2, 10**-1,1]
        lin1 = 0.01
        lin2 = 0.15
        lin3 = 1
    elif y1_name[:2] == 'gr':
        scale = 'linear'
        dic_key = f'_{y1_name}'
        normalization = g0
        y1lims = (0,1.1)
        yticks = [0,0.5,1]
        lin1 = 0.3
        lin2 = 0.7
        lin3 = 0.5
    else:
        print('wtf do you want to plot?')
        return None
    for i in range(8):
        for j, well in zip(range(12), list(all_wells)[i*12:i*12+12]):
            ax= plt.subplot2grid((8,12),(i,j))
            ax.plot(y1_1plate['time[h]'], np.array(y1_1plate[f'{well}{dic_key}'])/normalization,'-o', markersize=3)
            if y1_lines == True:
                ax.hlines(lin3, xmin,xmax,'r')
                ax.hlines(lin1, xmin,xmax,'r', linestyle='dashed')
                ax.hlines(lin2, xmin,xmax,'r', linestyle='dashed')
            ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
            ax2.step(ABdata_1plate['time[h]'], ABdata_1plate[well],where='post',color='orange')
            ax2.set_yscale('log')
            ax2.set_yticks([])
            ax2.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
            ax.set_yscale(scale)
            ax.set_yticks([])
            ax.set_xticks([])
            ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
            if j==11:
                ax2.set_yticks([10**-3,1,10**3])
                ax2.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
                ax2.set_ylabel(f'{ABylabel}[ug/ml]', color='orange', fontsize=16)
            if i==7:
                ax.set_xticks([xmin,xmax/2,xmax])
                ax.set_xlabel('time[h]')
            if j==0:
                ax.set_yticks(yticks)
                ax.set_ylabel(y1_name, color='C0', fontsize=16)
            str_num = layouts[plate].loc[well[0],well[1:]]
            if str_num!='lacA' and str_num!='LB':
                motherplate = platenum_to_motherplate[plate]
                title = strainsdf[(strainsdf['mother_plate']==motherplate)&(strainsdf['strain']==str_num)].index.values[0]
            else:
                title = layouts[plate].loc[well[0],well[1:]]
            ax.set_title(title)
    #         plt.title(well)
            ax.set_ylim(y1lims)
            ax2.set_ylim(ABylims)
            ax.set_xlim((xmin,xmax))
            if ABres_lines == True:
                ax2.hlines(cm1end,xmin,xmax,'k')
                ax2.hlines(cm2end,xmin,xmax,'k')
    # plt.suptitle(motherplate)
