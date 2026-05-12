#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 12:01:27 2021

@author: gaby
"""
import zipfile
import requests
from pathlib import Path
from io import BytesIO
import sys
import fsepi_MASTER_functions as mymf
import fsepi_MASTER_plotting_functions as mypf
import pickle
from plotly.subplots import make_subplots

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def histogram_for_barplot(xis, nbins):
    binss=np.linspace(min(xis), max(xis),nbins)
    hist, bins=np.histogram(xis, bins=binss)
    return hist, binss

# ──────────────────────────────────────────────
# Zenodo-related CONFIGURATION — edit these two values
# ──────────────────────────────────────────────
ZENODO_RECORD_ID = "20082951"          # Zenodo record ID
ZIP_FILENAME      = "fsepi_data.zip"  # your ZIP filename on Zenodo

@st.cache_resource(show_spinner="Downloading data from Zenodo...")
def load_data_from_zenodo():
    """
    Downloads and extracts the ZIP from Zenodo.
    Cached so it only runs once per app session.
    Uses an API token if available (for restricted/embargoed data).
    Returns a Path to the extracted data directory.
    """
    url = f"https://zenodo.org/api/records/{ZENODO_RECORD_ID}/files/{ZIP_FILENAME}/content"

    # Use token if available (for restricted data), otherwise download without
    headers = {}
    try:
        token = st.secrets["ZENODO_TOKEN"]
        headers["Authorization"] = f"Bearer {token}"
    except (KeyError, FileNotFoundError):
        pass  # No token — data must be public

    response = requests.get(url, headers=headers, timeout=120)
    response.raise_for_status()

    extract_dir = Path("data")
    extract_dir.mkdir(exist_ok=True)

    with zipfile.ZipFile(BytesIO(response.content)) as zf:
        zf.extractall(extract_dir)

    return extract_dir
# ──────────────────────────────────────────────
# Load the data (this line triggers the download)
# ──────────────────────────────────────────────
DATA_DIR = load_data_from_zenodo()
# ──────────────────────────────────────────────
# YOUR APP CODE BELOW
# ──────────────────────────────────────────────
# Use DATA_DIR to reference your files, for example:
#
#   import pandas as pd
#   df = pd.read_csv(DATA_DIR / "subfolder" / "my_file.csv")
#
# The directory structure inside the ZIP is preserved,
# so use the same relative paths as on your local machine.
# ──────────────────────────────────────────────
# st.write(f"Data loaded from: {DATA_DIR}")
# st.write("Files available:")
# for f in sorted(DATA_DIR.rglob("*")):
#     if f.is_file():
#         st.write(f"  📄 {f.relative_to(DATA_DIR)}")
# =============================================================================
# -- Set page config
apptitle = 'Petrungaro_et_al_NatComm_EvoExperiments_explorer'
st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

# Title the app
st.title('Evolution experiments data explorer and visualization')
# st.subtitle('hola')
st.markdown("""
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
""")

st.sidebar.markdown("## Select data")

#-- Choose experiment
antibioticlist = ['Trimethoprim (TMP)',' Nitrofurantoin (NIT)', 'Mecillinam (MEC)']
antibiotic = st.sidebar.selectbox('Select experiment by antibiotic name',
                                    antibioticlist)
antibiotic_label = antibiotic[antibiotic.index('(')+1:antibiotic.index(')')]
# =============================================================================
if antibiotic_label == 'TMP':
    exp_ini_date = '12082021'
    tmax = 600
    first_plate = '11641'
    motherplates_dic = {'GPm1bkpcorrected':[f'1164{i}' for i in range(1,4)], 'GPm2':[f'1164{i}' for i in range(4,7)], 'GPm3':[f'1164{i}' for i in range(7,10)]}
    platenum_to_motherplate = {}
    for i in range(1,4):
        platenum_to_motherplate[f'1164{i}'] = 'GPm1bkpcorrected'
    for i in range(4,7):
        platenum_to_motherplate[f'1164{i}'] = 'GPm2'
    for i in range(7,10):
        platenum_to_motherplate[f'1164{i}'] = 'GPm3'
elif antibiotic_label == 'MEC':
    exp_ini_date = '20052022'
    tmax = 500
    first_plate = '17221'
    motherplates_dic = {'GPm1bkpcorrected':[f'1722{i}' for i in range(1,4)], 'GPm2':[f'1722{i}' for i in range(4,7)], 'GPm3':[f'1722{i}' for i in range(7,10)]}
    platenum_to_motherplate = {}
    for i in range(1,4):
        platenum_to_motherplate[f'1164{i}'] = 'GPm1bkpcorrected'
    for i in range(4,7):
        platenum_to_motherplate[f'1164{i}'] = 'GPm2'
    for i in range(7,10):
        platenum_to_motherplate[f'1164{i}'] = 'GPm3'
else:
    exp_ini_date = '21062021'
    tmax=270#450
    first_plate = '8961'
    motherplates_dic = {'GPm1bkpcorrected':[f'896{i}' for i in range(1,4)], 'GPm2':[f'896{i}' for i in range(4,7)], 'GPm3':[f'896{i}' for i in range(7,10)]}
    platenum_to_motherplate = {}
    for i in range(1,4):
        platenum_to_motherplate[f'896{i}'] = 'GPm1bkpcorrected'
    for i in range(4,7):
        platenum_to_motherplate[f'896{i}'] = 'GPm2'
    for i in range(7,10):
        platenum_to_motherplate[f'896{i}'] = 'GPm3'
exp_info = {'exp_ini_date': exp_ini_date, 'antibiotic': antibiotic_label, 'number_of_plates':  9}
exp_folder = f'{DATA_DIR}/fsepi_data/Results_{exp_info["antibiotic"]}_{exp_info["number_of_plates"]}plates_{exp_info["exp_ini_date"]}'
#-------------------------------------------------------
plates_info, layouts = mymf.read_plates_layout(exp_folder, exp_info['exp_ini_date'], names='no')
plates = plates_info.loc[:,'Plate'].values
print('plates:', plates)
#---------------------------------------------------
ODdata = {}
ABdata = {}
full_gr_dic = {}
min_OD_exp = 0.01
max_OD_exp = 0.15
# g0 =0.02
for pl in plates:
    _, ODdata[pl], ABdata[pl], full_gr_dic[pl] = mymf.load_data_one_plate(exp_folder, pl, min_OD_exp, max_OD_exp)
strainsdf = mymf.import_strain_names_as_dataframe(motherplates_dic.keys())
#
# seq_results = pickle.load(open(f'{exp_folder}/mutated_genes_in_evolved_strains_{exp_info["antibiotic"]}.p', 'rb'))
# =============================================================================
#%%
all_wells = [f'{i}{j}' for i in 'ABCDEFGH' for j in range(1,13)]
grs_lacA_nodrug = []
for plate in plates_info.loc[:,'Plate']:
    # print('plate ', plate)
    lacA_wells = [w for w in all_wells if layouts[plate].loc[w[0], w[1:]]=='lacA']
    grs_lacA_nodrug=grs_lacA_nodrug+[full_gr_dic[plate][f'{well}_gr_fit'][1] for well in lacA_wells]
print(grs_lacA_nodrug)
g0=0.02#np.mean(grs_lacA_nodrug)
#%%
# import matplotlib as mpl
# mpl.use("agg")

# ##############################################################################
# # Workaround for the limited multi-threading support in matplotlib.
# # Per the docs, we will avoid using `matplotlib.pyplot` for figures:
# # https://matplotlib.org/3.3.2/faq/howto_faq.html#how-to-use-matplotlib-in-a-web-application-server.
# # Moreover, we will guard all operations on the figure instances by the
# # class-level lock in the Agg backend.
# ##############################################################################
# from matplotlib.backends.backend_agg import RendererAgg
# _lock = RendererAgg.lock



#-- Set time by GPS or event
select_event = st.sidebar.selectbox('How do you want to find data?',
                                    ['By strain (all replicates)', 'By plate and well',"I'd like to see an overview of one plate"])


if select_event == 'By strain (all replicates)':
    # -- Give a gene name, selected strain has that gene-deletion:        
    strain = st.sidebar.text_input('Strain name', 'tolC')    # -- GW150914
    
    # t0 = strain#float(str_t0)

    st.sidebar.markdown("""
    Example gene-deletions in experiment:
    * lacA (reference strain)
    * tolC
    * mutT
    * dnaK
    """)
    #uncomment to include mutations quick and dirty.
    # strains = [strain, 'lacA']
    # strain_plates_reps = [int(k[1]) for k in seq_results.keys() if k[0]==strain]
    # strain_plates_reps.sort()
    # d_strain = {k[1]:[tup[1] for tup in seq_results[k]] for k in seq_results.keys() if k[0]==strain}
    # for k in d_strain:
    #     d_strain[k].sort()
    # mut_string = ''.join(['<br>'+str(i)+':'+str(d_strain[str(i)]) for i in strain_plates_reps])
    # fig = mypf.OD_AB_gr_fit_vs_time_1strain_allreplicates(strain, ODdata, ABdata, full_gr_dic, layouts, motherplates_dic, strainsdf, g0=0.02, tmax=tmax, ABylabel = antibiotic_label, seq_results = seq_results)
    # fig.update_layout(title=f'\u0394{strain} -- mutations:{mut_string}', title_x=0.5,
    #
    fig = mypf.OD_AB_gr_fit_vs_time_1strain_allreplicates(strain, ODdata, ABdata, full_gr_dic, layouts, motherplates_dic, strainsdf, g0=0.02, tmax=tmax, ABylabel = antibiotic_label)
    fig.update_layout(title=f'\u0394{strain}', title_x=0.5,
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
    st.plotly_chart(fig, width=800, height=800)
### Multiple strains together -- replicates from multiple plates
# strains = ['lacA','s45']#,'tolC']
# strain_color = asign_colors_to_strains(strains)
    # strains = [strain, 'lacA']    
    # strain_color = {'lacA':'gray', strains[0]:'C0'}
    # fig, axs = plt.subplots(4)
    # fig.set_figheight(20)
    # fig.set_figwidth(15)
    # tit = []
    # for plate in plates_info.loc[0:2,'Plate']:
    #     tit.append(plate)
    #     plate_layout = layouts[plate]
    #     well_strain = {w:plate_layout.loc[w[0],w[1:]] for w in all_wells}
    #     well_color = mypf.asign_strain_color_to_wells(plate_layout, strain_color)
    #     pl_wells=[w for w in all_wells if well_strain[w] in strains]#inoc_wells
    #     #-------------------
    # #     AB_and_gr_vs_time([ax1,ax2], ODdata[plate], ABdata[plate], pl_wells, well_color, well_strain, full_gr_dic[plate], xmax=310)                             
    #     mypf.OD_AB_both_gr_vs_time(axs, ODdata[plate], ABdata[plate], pl_wells, well_color, well_strain, full_gr_dic[plate], g0=0.02)#, xmax=400)
    # #remove repeated labels
    # labels=[p.get_label() for i, p in enumerate(axs[0].get_lines())]
    # for i, p in enumerate(axs[0].get_lines()):
    #     if p.get_label() in labels[:i]:    # check for Name already exists
    #          idx = labels.index(p.get_label())       # find ist index
    # #         #p.set_c(ax.get_lines()[idx].get_c())   # set color
    #          p.set_label('_' + p.get_label())       # hide label in auto-legend
    # lgnd=axs[0].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=4, mode="expand", borderaxespad=0., fontsize=11)
    # plt.suptitle(tit)
    # st.pyplot(fig)

















elif select_event == 'By plate and well':
    plate = st.sidebar.text_input('plate', first_plate)
    well = st.sidebar.text_input('well', 'A4')
    st.sidebar.markdown("""
    Change last number to get data from following plates. Obs:
    * NIT plate numbers 896$i
    * TMP plate numbers 1164$i
    """)
    timerange = st.sidebar.slider('Time range [hours]', min_value=0, max_value=600, value=(0,tmax))
    #
    xis_lacA = np.array(grs_lacA_nodrug)/g0
    xis = np.array(full_gr_dic[plate][f'{well}_gr_fit'])/g0
    
    st.subheader('Relevant plots')
    fig, axs = plt.subplots(3, sharex=True)
    fig.set_figheight(10)
    fig.set_figwidth(15)
    # ax.semilogy(ODdata[plate]['time[h]'], ODdata[plate][well], markersize=3)
    mypf.OD_AB_gr_fit_vs_time_1well(axs, ODdata[plate], ABdata[plate], well, full_gr_dic[plate], g0=g0, timerange=timerange, antibiotic=antibiotic_label)
    st.pyplot(fig)
    # fig = mypf.OD_AB_gr_fit_vs_time_1well(plate, well, ODdata, ABdata, full_gr_dic, layouts, g0=0.02)
    # st.plotly_chart(fig)
    
    
    # xis = np.array(full_gr_dic[plate]['A4_gr_fit'])[(np.array(full_gr_dic[plate]['time[h]'])>timerange[0]) & (np.array(full_gr_dic[plate]['time[h]'])<timerange[1])]/g0 ##### distribution also in time range
    st.subheader('Distribution of growth rates all times')
    fig2, ax2 = plt.subplots()
    fig2.set_figheight(5)
    fig2.set_figwidth(15)
    hist, binss = histogram_for_barplot(xis, 50)
    hist2, binss2 = histogram_for_barplot(xis_lacA, 50)
    width=(binss[1]-binss[0])
    width2=(binss2[1]-binss2[0])
    ax2.bar(binss[:-1], hist, width=width, label = f'plate {plate} well {well}')
    ax2.bar(binss2[:-1], hist2, width=width2,fill=False, label = 'lacA reference strain\nin no drug (all ref wells)')
    ax2.vlines(0.5, 0,16, label='50% inhibition', color='k', linestyle='dashed')
    median = np.median(xis)
    ax2.vlines(median, 0,16, 'k', label=f'median = {np.round(median,2)}')
    ax2.set_xlim(-0.02, 1.2)
    ax2.set_ylim(0, 16)
    ax2.legend()
    st.pyplot(fig2)

else:
    plate = st.sidebar.text_input('plate', first_plate)
    y2 = st.sidebar.selectbox('Antibiotic concentration together with:',
                                    ['normalized growth rate', 'OD data'])
    fig = plt.figure(figsize=(30,20))
    dic = {'normalized growth rate': (full_gr_dic, 'gr_fit'), 'OD data':(ODdata, 'OD')}
    mypf.plate_overwiew_2ys(dic[y2][0], dic[y2][1], ABdata, layouts, plate, platenum_to_motherplate, strainsdf, xmax=tmax, g0 = g0, ABylabel = antibiotic_label)
    st.pyplot(fig)
    
    

