import streamlit as st
import CoolProp.CoolProp as CP
from CoolProp.CoolProp import PhaseSI, PropsSI, get_global_param_string
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy
import pandas
st.set_page_config(page_title='制冷工具', page_icon=(":four_leaf_clover:"), layout="centered", initial_sidebar_state="auto", menu_items=None)


# st.title('肥猫，这个库太厉害，太简单了')
st.header('冷媒查询')
st.subheader('饱和状态查询')
# st.text('文本')
# st.markdown('markdown is **_really_ cool**.')
ref = st.selectbox(
    '请选择冷媒',
    ('R11', 'R113', 'R114', 'R115', 'R12', 'R123', 'R1233zd(E)', 'R1234yf',
            'R1234ze(E)', 'R1234ze(Z)', 'R124', 'R125', 'R13', 'R134a', 'R13I1', 'R14', 'R141b', 'R142b', 'R143a',
            'R152A', 'R161', 'R21', 'R218', 'R22', 'R227EA', 'R23', 'R236EA', 'R236FA', 'R245ca', 'R245fa', 'R32',
            'R365MFC', 'R40', 'R404A', 'R407C', 'R41', 'R410A', 'R507A', 'RC318', 'SES36', 'SulfurDioxide',
            'Water', 'Xenon', 'R290', 'R744', 'CO2'))
# ref
st.write('你的选择:', ref)


ASHRAE = CP.get_fluid_param_string(ref, 'ASHRAE34')
st.write('安全类别：', ASHRAE)

GWP100 = CP.PropsSI(ref, 'GWP100')
GWP100 = int(GWP100)
st.write('GWP100：', GWP100)

 # 临界压力
pressure_at_critical_point = round(CP.PropsSI(ref, 'pcrit') / 1000000, 3)
st.write('临界压力：', pressure_at_critical_point, 'Mpa')
#  临界温度
temperature_at_critical_point = round(CP.PropsSI(ref, 'Tcrit') - 273.15, 3)
st.write('临界温度：', temperature_at_critical_point, '℃')

#  露点 泡点
stat = st.radio(
     "状态选择",
     ('露点', '泡点'))
if stat ==('露点'):
    stat = 1
else:
    stat = 0

st.success('通过压力查温度')
#  通过压力查温度
p2t = st.number_input('输入饱和压力(Mpa(g))', min_value=None, max_value=None,
                      value=1.000, step=0.1, format="%.3f", key=None, help=None, on_change=None,
                      args=None, kwargs=None, disabled=False)
# p2t
# st.text('饱和温度：')
try:
    p2tt = round((CP.PropsSI("T", "P", (p2t*1000000 + 101325), "Q", stat, ref) - 273.15), 3)
    # print(CP.PropsSI("T", "P", (p2t*1000000+101325), "Q", stat, ref))
    st.write('饱和温度：', p2tt, '℃')
except Exception as e:
    # print(e)
    p2tt = str(e)
    st.write('饱和温度：', p2tt, '℃')

st.success('通过温度查压力')
#  通过压力查温度
t2p = st.number_input('输入饱和温度(℃)', min_value=None, max_value=None,
                      value=20.000, step=1.000, format="%.3f", key=None, help=None, on_change=None,
                      args=None, kwargs=None, disabled=False)

try:
    t2pp = round((CP.PropsSI("P", "T", (t2p+273.15), "Q", stat, ref) - 101325)/ 1000000, 3)
    st.write('饱和压力：', t2pp, 'Mpa')
except Exception as e:
    # print(e)
    t2pp = str(e)
    st.write('饱和温度：', t2pp, '℃')