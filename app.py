import pandas as pd
import streamlit as st
# from st_aggrid import AgGrid, GridOptionsBuilder
import CoolProp.CoolProp as CP
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PhaseSI, PropsSI, get_global_param_string, get_fluid_param_string

# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy

st.set_page_config(page_title='制冷工具', page_icon=(":four_leaf_clover:"), layout="centered",
                   initial_sidebar_state="expanded", menu_items=None)

# st.title('肥猫，这个库太厉害，太简单了')
st.sidebar.title('冷媒查询工具')
st.sidebar.header('')
tool_type = st.sidebar.radio(
    '选择查询类别',
    ('冷媒信息', '饱和状态查询', '非饱和状态查询', '理论COP计算', '压焓图'))
st.sidebar.header('')

ref_list = ['R11', 'R113', 'R114', 'R115', 'R12', 'R123', 'R1233zd(E)', 'R1234yf',
         'R1234ze(E)', 'R1234ze(Z)', 'R124', 'R125', 'R13', 'R134a', 'R13I1', 'R14', 'R141b', 'R142b', 'R143a',
         'R152A', 'R161', 'R21', 'R218', 'R22', 'R227EA', 'R23', 'R236EA', 'R236FA', 'R245ca', 'R245fa', 'R32',
         'R365MFC', 'R40', 'R404A', 'R407C', 'R41', 'R410A', 'R507A', 'RC318', 'SES36', 'SulfurDioxide',
         'Water', 'Xenon', 'R290', 'R744', 'CO2']
# 冷媒信息
if tool_type == "冷媒信息":
    st.header('冷媒信息')
    # st.header('')
    ref = st.selectbox(
        '选择冷媒',
        ref_list, 30)

    ref2 = st.selectbox(
        '选择对比冷媒',
        ref_list, 36)
# st.text('文本')
# st.markdown('markdown is **_really_ cool**.')

    # st.title('')
    st.markdown('**对比表格**')
    pd.set_option('display.unicode.east_asian_width', True)
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_colwidth', 400)
    # pd.set_option('expand_frame_repr', False)

    info_ASHRAE = CP.get_fluid_param_string(ref, 'ASHRAE34')
    # st.write('安全类别：', info_ASHRAE)

    info_GWP100 = CP.PropsSI(ref, 'GWP100')
    GWP100 = int(info_GWP100)
    # st.write('GWP100：', GWP100)
    # info_ODP = CP.get_fluid_param_string(ref, 'ODP')
    # ODP = int(info_ODP)

     # 临界压力
    pressure_at_critical_point = round(CP.PropsSI(ref, 'pcrit') / 1000000, 3)
    # st.write('临界压力：', pressure_at_critical_point, 'Mpa')
    #  临界温度
    temperature_at_critical_point = round(CP.PropsSI(ref, 'Tcrit') - 273.15, 3)
    # st.write('临界温度：', temperature_at_critical_point, '℃')

    # st.title('')
    # st.write('对比冷媒:', ref2)

    info_ASHRAE2 = CP.get_fluid_param_string(ref2, 'ASHRAE34')
    # st.write('安全类别：', info_ASHRAE2)

    info_GWP1002 = CP.PropsSI(ref2, 'GWP100')
    GWP1002 = int(info_GWP1002)
    # st.write('GWP100：', GWP1002)

     # 临界压力
    pressure_at_critical_point2 = round(CP.PropsSI(ref2, 'pcrit') / 1000000, 3)
    # st.write('临界压力：', pressure_at_critical_point2, 'Mpa')
    #  临界温度
    temperature_at_critical_point2 = round(CP.PropsSI(ref2, 'Tcrit') - 273.15, 3)
    # st.write('临界温度：', temperature_at_critical_point2, '℃')

    dic = {"冷媒1": {"冷媒名称": str(ref), "安全类别": str(info_ASHRAE),
                   "GWP100": str(GWP100),
                   "临界压力(Mpa(G))": str(pressure_at_critical_point), "临界温度(℃)": str(temperature_at_critical_point)},
           "冷媒2": {"冷媒名称": str(ref2), "安全类别": str(info_ASHRAE2),
                   "GWP100": str(GWP1002), "临界压力(Mpa(G))": str(pressure_at_critical_point2), "临界温度(℃)": str(temperature_at_critical_point2)}
           }

    df = pd.DataFrame(dic)
    # print(df)
    st.table(df)

    # bg = GridOptionsBuilder.from_dataframe(df)
    # grid_return = AgGrid(df)

#  饱和状态查询
if tool_type == "饱和状态查询":
    st.subheader('饱和状态查询')
    st.title('')

    ref = st.selectbox(
        '选择冷媒',
        ref_list, 30)

    ref2 = st.selectbox(
        '选择对比冷媒',
        ref_list, 36)

    st.title('')

    tool_type1 = st.radio(
        '查询',
        ('饱和压力', '饱和温度')
    )

    stat = st.radio(
        "状态选择",
        ('露点', '泡点'))
    if stat == '露点':
        stat = 1
    else:
        stat = 0

    if tool_type1 == '饱和温度':

    #  st.success('通过压力查温度')
    #  通过压力查温度
        p2t = st.number_input('输入饱和压力(Mpa(g))', min_value=None, max_value=None,
                              value=1.000, step=0.1, format="%.3f", key=None, help=None, on_change=None,
                              args=None, kwargs=None, disabled=False)
        # p2t
    # st.text('饱和温度：')
        try:
            p2tt = round((CP.PropsSI("T", "P", (p2t * 1000000 + 101325), "Q", stat, ref) - 273.15), 3)
            p2tt2 = round((CP.PropsSI("T", "P", (p2t * 1000000 + 101325), "Q", stat, ref2) - 273.15), 3)
            # print(CP.PropsSI("T", "P", (p2t*1000000+101325), "Q", stat, ref))
            # st.write('饱和温度：', p2tt, '℃')
        except Exception as e:
            # print(e)
            p2tt = str(e)
            p2tt2 = str(e)
            # st.write('饱和温度：', p2tt, '℃')
     # 临界压力
        pressure_at_critical_point = round(CP.PropsSI(ref, 'pcrit') / 1000000, 3)
        pressure_at_critical_point2 = round(CP.PropsSI(ref2, 'pcrit') / 1000000, 3)
        # st.write('临界压力：', pressure_at_critical_point, 'Mpa')
        #  临界温度
        temperature_at_critical_point = round(CP.PropsSI(ref, 'Tcrit') - 273.15, 3)
        temperature_at_critical_point2 = round(CP.PropsSI(ref2, 'Tcrit') - 273.15, 3)
        # st.write('临界温度：', temperature_at_critical_point, '℃')
        dic = {"冷媒1": {"冷媒名称": str(ref),
                       "临界压力(Mpa(G))": str(pressure_at_critical_point), "临界温度(℃)": str(temperature_at_critical_point),
                       "饱和温度(℃)": str(p2tt), "饱和压力(℃)": str(p2t)},
               "冷媒2": {"冷媒名称": str(ref2),
                       "临界压力(Mpa(G))": str(pressure_at_critical_point2), "临界温度(℃)": str(temperature_at_critical_point2),
                       "饱和温度(℃)": str(p2tt2), "饱和压力(℃)": str(p2t)}
               }

        df = pd.DataFrame(dic)
    # print(df)
        st.table(df)

    if tool_type1 == '饱和压力':

        # st.success('通过温度查压力')
        #  通过压力查温度
        t2p = st.number_input('输入饱和温度(℃)', min_value=None, max_value=None,
                              value=20.000, step=1.000, format="%.3f", key=666, help=None, on_change=None,
                              args=None, kwargs=None, disabled=False)

        try:
            t2pp = round((CP.PropsSI("P", "T", (t2p + 273.15), "Q", stat, ref) - 101325) / 1000000, 3)
            t2pp2 = round((CP.PropsSI("P", "T", (t2p + 273.15), "Q", stat, ref2) - 101325) / 1000000, 3)
            # st.write('饱和压力：', t2pp, 'Mpa')
        except Exception as e:
            # print(e)
            t2pp = str(e)
            t2pp2 = str(e)
            # st.write('饱和温度：', t2pp, '℃')

     # 临界压力
        pressure_at_critical_point = round(CP.PropsSI(ref, 'pcrit') / 1000000, 3)
        pressure_at_critical_point2 = round(CP.PropsSI(ref2, 'pcrit') / 1000000, 3)
        # st.write('临界压力：', pressure_at_critical_point, 'Mpa')
        #  临界温度
        temperature_at_critical_point = round(CP.PropsSI(ref, 'Tcrit') - 273.15, 3)
        temperature_at_critical_point2 = round(CP.PropsSI(ref2, 'Tcrit') - 273.15, 3)
        # st.write('临界温度：', temperature_at_critical_point, '℃')
        dic = {"冷媒1": {"冷媒名称": str(ref),
                       "临界压力(Mpa(G))": str(pressure_at_critical_point), "临界温度(℃)": str(temperature_at_critical_point),
                       "饱和温度(℃)": str(t2p), "饱和压力(℃)": str(t2pp)},
               "冷媒2": {"冷媒名称": str(ref2),
                       "临界压力(Mpa(G))": str(pressure_at_critical_point2), "临界温度(℃)": str(temperature_at_critical_point2),
                       "饱和温度(℃)": str(t2p), "饱和压力(℃)": str(t2pp2)}
               }

        df = pd.DataFrame(dic)
    # print(df)
        st.table(df)

if tool_type == "非饱和状态查询":
    st.subheader('非饱和状态查询')
    st.title('')

    ref = st.selectbox(
        '选择冷媒',
        ref_list, 30)

    ref2 = st.selectbox(
        '选择对比冷媒',
        ref_list, 36)

    st.title('')

    parameter_list = ('A',
                      'ACENTRIC',
                      'ALPHA0',
                        'ALPHAR',
                        'BVIRIAL',
                        'Bvirial',
                        'C',
                        'CONDUCTIVITY',
                        'CP0MASS',
                        'CP0MOLAR',
                        'CPMASS',
                        'CPMOLAR',
                        'CVIRIAL',
                        'CVMASS',
                        'CVMOLAR',
                        'Cp0mass',
                        'Cp0molar',
                        'Cpmass',
                        'Cpmolar',
                        'Cvirial',
                        'Cvmass',
                        'Cvmolar',
                        'D',
                        'DALPHA0_DDELTA_CONSTTAU',
                        'DALPHA0_DTAU_CONSTDELTA',
                        'DALPHAR_DDELTA_CONSTTAU',
                        'DALPHAR_DTAU_CONSTDELTA',
                        'DBVIRIAL_DT',
                        'DCVIRIAL_DT',
                        'DELTA',
                        'DIPOLE_MOMENT',
                        'DMASS',
                        'DMOLAR',
                        'Delta',
                        'Dmass',
                        'Dmolar',
                        'FH',
                        'FRACTION_MAX',
                        'FRACTION_MIN',
                        'FUNDAMENTAL_DERIVATIVE_OF_GAS_DYNAMICS',
                        'G',
                        'GAS_CONSTANT',
                        'GMASS',
                        'GMOLAR',
                        'GWP100',
                        'GWP20',
                        'GWP500',
                        'Gmass',
                        'Gmolar',
                        'H',
                        'HH',
                        'HMASS',
                        'HMOLAR',
                        'Hmass',
                        'Hmolar',
                        'I',
                        'ISOBARIC_EXPANSION_COEFFICIENT',
                        'ISOTHERMAL_COMPRESSIBILITY',
                        'L',
                        'M',
                        'MOLARMASS',
                        'MOLAR_MASS',
                        'MOLEMASS',
                        'O',
                        'ODP',
                        'P',
                        'PCRIT',
                        'PH',
                        'PHASE',
                        'PIP',
                        'PMAX',
                        'PMIN',
                        'PRANDTL',
                        'PTRIPLE',
                        'P_CRITICAL',
                        'P_MAX',
                        'P_MIN',
                        'P_REDUCING',
                        'P_TRIPLE',
                        'P_max',
                        'P_min',
                        'Pcrit',
                        'Phase',
                        'Prandtl',
                        'Q',
                        'RHOCRIT',
                        'RHOMASS_CRITICAL',
                        'RHOMASS_REDUCING',
                        'RHOMOLAR_CRITICAL',
                        'RHOMOLAR_REDUCING',
                        'S',
                        'SMASS',
                        'SMOLAR',
                        'SMOLAR_RESIDUAL',
                        'SPEED_OF_SOUND',
                        'SURFACE_TENSION',
                        'Smass',
                        'Smolar',
                        'Smolar_residual',
                        'T',
                        'TAU',
                        'TCRIT',
                        'TMAX',
                        'TMIN',
                        'TTRIPLE',
                        'T_CRITICAL',
                        'T_FREEZE',
                        'T_MAX',
                        'T_MIN',
                        'T_REDUCING',
                        'T_TRIPLE',
                        'T_critical',
                        'T_freeze',
                        'T_max',
                        'T_min',
                        'T_reducing',
                        'T_triple',
                        'Tau',
                        'Tcrit',
                        'Tmax',
                        'Tmin',
                        'Ttriple',
                        'U',
                        'UMASS',
                        'UMOLAR',
                        'Umass',
                        'Umolar',
                        'V',
                        'VISCOSITY',
                        'Z',
                        'acentric',
                        'alpha0',
                        'alphar',
                        'conductivity',
                        'dBvirial_dT',
                        'dCvirial_dT',
                        'dalpha0_ddelta_consttau',
                        'dalpha0_dtau_constdelta',
                        'dalphar_ddelta_consttau',
                        'dalphar_dtau_constdelta',
                        'dipole_moment',
                        'fraction_max',
                        'fraction_min',
                        'fundamental_derivative_of_gas_dynamics',
                        'gas_constant',
                        'isobaric_expansion_coefficient',
                        'isothermal_compressibility',
                        'molar_mass',
                        'molarmass',
                        'molemass',
                        'p_critical',
                        'p_reducing',
                        'p_triple',
                        'pcrit',
                        'pmax',
                        'pmin',
                        'ptriple',
                        'rhocrit',
                        'rhomass_critical',
                        'rhomass_reducing',
                        'rhomolar_critical',
                        'rhomolar_reducing',
                        'speed_of_sound',
                        'surface_tension',
                        'viscosity')

    in_put = st.selectbox(
        '已知参数1',
        parameter_list, 20)
    in_put_data = st.number_input('参数值')

    in_put2 = st.selectbox(
        '已知参数2',
        parameter_list, 30)
    in_put_data2 = st.number_input('参数2值')

    out_put = st.selectbox(
        '选择查询参数',
        parameter_list, 36)
    out_put_data = CP.PropsSI(out_put, in_put, in_put_data, in_put2, in_put_data2, ref)
    st.write(out_put_data)
    out_put_data2 = CP.PropsSI(out_put, in_put, in_put_data, in_put2, in_put_data2, ref2)

if tool_type == "理论COP计算":
    st.subheader('理论COP计算')
    st.title('')
    ref = st.selectbox(
        '选择冷媒',
        ref_list, 30)

    ref2 = st.selectbox(
        '选择对比冷媒',
        ref_list, 36)

if tool_type == "压焓图":
    st.subheader('压焓图')
    st.title('')
    ref = st.selectbox(
        '选择冷媒',
        ref_list, 30)

    ref2 = st.selectbox(
        '选择对比冷媒',
        ref_list, 36)

    # ref1临界压力
    pressure_at_critical_point1 = CP.PropsSI(ref, 'pcrit') / 1000000
    # print(pressure_at_critical_point1)
    pressure_at_critical_point1_g = pressure_at_critical_point1 - 1.01325
    # print(pressure_at_critical_point1_g)
    h_at_critical_point1 = CP.PropsSI("H", "P", pressure_at_critical_point1 * 1000000, "Q", 1, ref) / 1000

    p_list = []
    h_v_list = []
    h_l_list = []
    # p_list = [pressure_at_critical_point1_g]
    # print(p_list)
    # h_v_list = [h_at_critical_point1]
    # h_l_list = [h_at_critical_point1]
    i = pressure_at_critical_point1_g
    while i > 0.01:
        i = i - 0.01
        # print(i)
        p_list.append(i)
        h_v = CP.PropsSI("H", "P", (i * 1000000 + 101325), "Q", 1, ref) / 1000
        h_l = CP.PropsSI("H", "P", (i * 1000000 + 101325), "Q", 0, ref) / 1000
        h_v_list.append(h_v)
        h_l_list.append(h_l)
    # print(p_list)
    # print(h_l_list)
    # p_list.append(pressure_at_critical_point1_g)
    # h_l_list.append(h_at_critical_point1)
    # h_v_list.append(h_at_critical_point1)
    # print(p_list)
    # print(h_l_list)
    # print(h_v_list)

    # ref2临界压力
    pressure_at_critical_point2 = CP.PropsSI(ref2, 'pcrit') / 1000000
    # print(pressure_at_critical_point1)
    pressure_at_critical_point2_g = pressure_at_critical_point2 - 1.01325
    # print(pressure_at_critical_point2_g)
    h_at_critical_point2 = CP.PropsSI("H", "P", pressure_at_critical_point2 * 1000000, "Q", 1, ref2) / 1000

    p_list2 = []
    h_v_list2 = []
    h_l_list2 = []
    # p_list = [pressure_at_critical_point1_g]
    # print(p_list)
    # h_v_list = [h_at_critical_point1]
    # h_l_list = [h_at_critical_point1]
    i2 = pressure_at_critical_point2_g
    while i2 > 0.01:
        i2 = i2 - 0.01
        # print(i2)
        p_list2.append(i2)
        h_v2 = CP.PropsSI("H", "P", (i2 * 1000000 + 101325), "Q", 1, ref2) / 1000
        h_l2 = CP.PropsSI("H", "P", (i2 * 1000000 + 101325), "Q", 0, ref2) / 1000
        h_v_list2.append(h_v2)
        h_l_list2.append(h_l2)
    # print(p_list2)
    # print(h_l_list)
    # p_list.append(pressure_at_critical_point1_g)
    # h_l_list.append(h_at_critical_point1)
    # h_v_list.append(h_at_critical_point1)
    # print(p_list)
    # print(h_l_list2)
    # print(h_v_list2)
    # pd.set_option('display.unicode.east_asian_width', True)
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_colwidth', 400)
    # pd.set_option('expand_frame_repr', False)
    # dic={"焓蒸汽":h_v_list,"焓液体":h_l_list}
    #      "冷媒2":{"安全类别":str(info_ASHRAE2),"GWP100":str(GWP1002),"临界压力":str(temperature_at_critical_point2)}}

    # df=pd.DataFrame(dic,index=p_list)
    # df2=pd.DataFrame(p_list,h_l_list)
    # print(df)
    # st.table(df)

    #fname = 'h'  # 文件名，也可为.csv，当为csv时，读取代码要改为pd.read_csv,其他不变
    #isheader = 0  # fname里的数据是否有标题，有标题isheader置为0，表示第一行当标题，无标题改为isheader = None
    #xlabel = 'h Enthalpy [kJ/kg]'  # 横坐标标题
    #ylabel = 'Pressure [Mpa(g)]'  # 纵坐标标题
    #title = 'Ph'  # 总标题

    #fig = plt.figure()  # 初始化一张图
    #plt.plot(h_l_list, p_list, label=ref + '(liquid)', color='dodgerblue', linestyle='--')  # 连线图,若要散点图将此句改为：plt.scatter(x,y) #散点图
    #plt.plot(h_v_list, p_list, label=ref + '(vapor)', color='salmon',linestyle='--')
    #plt.plot(h_l_list2, p_list2, label=ref2 + '(liquid)', color='dodgerblue')
    #plt.plot(h_v_list2, p_list2, label=ref2 + '(vapor)', color='salmon')

    ## plt.grid(alpha=0.5,linestyle='-.') #网格线，更好看
    #plt.title(title, fontsize=14)  # 画总标题 fontsize为字体，下同
    #plt.xlabel(xlabel, fontsize=14)  # 画横坐标
    #plt.ylabel(ylabel, fontsize=14)  # 画纵坐标
    #fig.legend(loc=1)
    ## plt.savefig(title+'.jpg', dpi=300) #可以存到本地，高清大图。路径默认为当前路径，dpi可理解为清晰度
    ## plt.show()
    #st.pyplot(fig)
