from PIL import Image
import matplotlib.cbook as cbook
import matplotlib.image as image
from matplotlib.dates import DateFormatter
import numba as nb
from time import strptime
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
import base64

#from diskcache import FanoutCache

import os
import asyncio

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvas
import plotly.graph_objects as go
#from bokeh.resources import INLINE
import panel as pn
import numpy as np
import codecs
import datetime
from io import BytesIO
from panel.widgets import SpeechToText, GrammarList
from panel.template import DarkTheme



css = ['https://cdn.datatables.net/1.10.24/css/jquery.dataTables.min.css',
       # Below: Needed for export buttons
       'https://cdn.datatables.net/buttons/1.7.0/css/buttons.dataTables.min.css'
]
js = {
    '$': 'https://code.jquery.com/jquery-3.5.1.js',
    'DataTable': 'https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js',
    # Below: Needed for export buttons
    'buttons': 'https://cdn.datatables.net/buttons/1.7.0/js/dataTables.buttons.min.js',
    'jszip': 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js',
    'pdfmake': 'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js',
    'vfsfonts': 'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js',
    'html5buttons': 'https://cdn.datatables.net/buttons/1.7.0/js/buttons.html5.min.js',
}
    
pn.extension('plotly' ,  'echarts', loading_spinner='dots',loading_color='#00aa41',sizing_mode = 'stretch_width',css_files=css, js_files=js)
#template = 'bootstrap'


#EXPIRE = 5 * 60  # 5 minutes
#CACHE_DIRECTORY = "cache"

#cache = FanoutCache(directory=CACHE_DIRECTORY)




script = """
<script>
function renderTable(){
  $('.example2').DataTable( {
    dom: 'Bfrtip',
    buttons: [
        'copyHtml5',
        'excelHtml5',
        'csvHtml5',
        'pdfHtml5'
    ]
} );
}

if (document.readyState === "complete") {
  renderTable()
} else {
  $(document).ready(renderTable);
}
</script>
"""

#@nb.jit()
def getdata():
 a = pd.read_excel('subdivision_data_1901-2019 _m1.xlsx',engine='openpyxl')
 a = a.drop(['Column2','Column4','Column17','Column18','Column19','Column20','Column21'],axis = 1)

 b = a.set_index(['Column3','Column22']).stack().reset_index()
#print(b)
 b.columns = ['year','name','month','rain']
 b.month = b.month.astype(int)
 return b

im1 = Image.open('static/imd_logo.png')
sz = im1.size
sz1 = (int(sz[0]/2), int(sz[1]/2))
height = im1.size[1]
width = im1.size[0]
im1 = np.array(im1).astype(np.float) / 255

'''
f = Figure(figsize=(12,9),dpi = 200)
#cw = os.getcwd()
#f.bbox.xmax-width
plt.style.use('fivethirtyeight')   
ax =f.subplots()
#print(height)      
ax.figure.figimage(im1, f.bbox.xmax-width, f.bbox.ymax-height)      
FigureCanvas(f)
'''


title = '## hello'

#m1 = int(b.year.min())
#m2 = int(b.year.max())
#m3 = list(range(m1,m2+1))



#print(b.dtypes)
#m4 = list(b.month.unique())

#bootstrap = pn.template.BootstrapTemplate(title='Seasonal variation')

bootstrap = pn.template.MaterialTemplate(title = 'Seasonal variation',theme = DarkTheme)

#s = pn.widgets.Select(name = 'Select',options =m3)
#s1 = pn.widgets.Select(name = 'Select1',options =m3)
#s2 = pn.widgets.Select(name = 'Select2',options =m4)
#s3 = pn.widgets.Select(name = 'Select3',options =m4)

b= getdata() 

m5 = list(b['name'].unique())
s4 = pn.widgets.Select(name = 'Subdivision',options =m5,width = 100)
k = s4.value
k1 = b[b.name == k]
m1 = int(k1.year.min())
m2 = int(k1.year.max())
m3 = list(range(m1,m2+1))
m4 = list(k1.month.unique())
m7 = list(range(0,12))
s = pn.widgets.Select(name = 'Start Year',width = 80,  options =m3 ,value = m1, precedence=1  )
s1 = pn.widgets.Select(name = 'End Year',width=80, options =m3 ,value = m2,  precedence=1 )
s2 = pn.widgets.Select(name = 'Start Month',width = 80, options =m4 ,value = 1 , precedence=1 )
s3 = pn.widgets.Select(name = 'No. of Months',width = 80, options =m7 ,value = 0, precedence=1  )

#s.jslink(s4,value='value')
#s1.jslink(s4,value='value')
#s2.jslink(s4,value='value')
#s3.jslink(s4,value='value')

#d = pn.widgets.DataFrame(b)  
'''
def load_data():
    if 'stocks' not in pn.state.cache:
        a = pd.read_excel('subdivision_data_1901-2019 _m1.xlsx',engine='openpyxl')
        a = a.drop(['Column2','Column4','Column17','Column18','Column19','Column20','Column21'],axis = 1)

        b = a.set_index(['Column3','Column22']).stack().reset_index()
        b.columns = ['year','name','month','rain']
        b.month = b.month.astype(int)
        pn.state.cache['stocks'] = b
    else:
        b = pn.state.cache['stocks']
    
    m5 = list(b['name'].unique()
    s4.options = m5
    k = m5[0]
    k1 = b[b.name == k]
    m1 = int(k1.year.min())
    m2 = int(k1.year.max())
    m3 = list(range(m1,m2+1))
    m4 = list(k1.month.unique())
    s.options = m3
    s1.options = m3
    s2.options = m4
    s3.options = m4
    
pn.state.onload(load_data)
'''


'''
@pn.depends(s4.param.value,watch = True)
def p2(s4):
 k = s4
 k1 = b[b.name == k]
 m1 = int(k1.year.min())
 m2 = int(k1.year.max())
 m3 = list(range(m1,m2+1))
 m4 = list(k1.month.unique())
 s.options = m3
 s1.options = m3
 s2.options = m4
 s3.options = m4
 #s.value = m3[0]
 #s1.value = m3[0]
 #s2.value = m4[0]
 #s3.value = m4[0]
'''
d  = pn.widgets.DataFrame(width = 300,height = 400)  

table_with_export_buttons = pn.pane.HTML("<h1>hello</h1>", margin=(10,5,25,5))  #sizing_mode='stretch_width'

#file_download_csv = pn.widgets.FileDownload(filename="Statistical.csv", button_type="primary")   

file_download = pn.widgets.FileDownload(file='figure.png',button_type='success',label='Download',name='Click to download chart')

al = pn.pane.Alert("Hello")  

ld = pn.indicators.LoadingSpinner(width=100,height=100,color='primary',bgcolor='dark')

plotly_pane7 = pn.pane.Plotly()
plotly_pane8 = pn.pane.Plotly()


plotly_pane5 = pn.pane.Plotly()
plotly_pane6 = pn.pane.HTML()

matpl = pn.pane.Plotly()

radio_group = pn.widgets.RadioButtonGroup(
    name='Radio Button Group', options=['Seasonal','Yearly',  'Monthly', 'Month-Month'], button_type='success',value='Seasonal')


months_choices = []
dd={}
for i in range(1,13):
    db1 = datetime.datetime.strptime(str(i),"%m")
    m1 = db1.strftime("%B")
    months_choices.append(m1)
    dd[m1]= i


#s5= pn.widgets.Select(name = 'Month',width = 80, options = months_choices ,value = months_choices[0]   , precedence= -1  )
gau= pn.indicators.Gauge(name='Selected Month', value=1, bounds=(0, 12),  format='{value}'  , num_splits=2  )

s5 = pn.widgets.DiscreteSlider(name='Month', options= months_choices , value= months_choices[0],  precedence= -1   )

@pn.depends(radio_group.param.value,s4.param.value,  watch = True)
def p5(radio_group,s4):
 '''      
 if(radio_group == 'Monthly') :
   s2.visible=False
   s3.visible=False
   s5.visible=True
   gau.visible=True
 

 if(radio_group == 'Yearly') :
   s2.visible=False
   s3.visible=False
   s5.visible=False
   gau.visible=False

 if(radio_group == 'Seasonal') :
   s2.visible=True
   s3.visible=True
   s5.visible=False
   gau.visible=False

 if(radio_group == 'Month-Month') :
   s2.visible=True
   s3.visible=True
   s5.visible=False
   gau.visible=False
 '''
 b= getdata()
 k = s4
 k1 = b[b.name == k]
 m1 = int(k1.year.min())
 m2 = int(k1.year.max())
 m3 = list(range(m1,m2+1))
 m4 = list(k1.month.unique())
 m7 = list(range(0,12))
 s.options = m3
 s1.options = m3
 s2.options = m4
 s3.options = m7
 s.value = m3[0]
 s1.value = m3[-1]
 s2.value = m4[0]
 s3.value = m7[0]


@pn.depends(s.param.value,s1.param.value,s2.param.value,s3.param.value,s4.param.value, s5.param.value ,radio_group.param.value,watch=True )
#@asyncio.coroutine
def p1(s,s1,s2,s3,s4,s5,radio_group):
 s3 = s2+s3      
 #await asyncio.sleep(2)
 al.object='welcome to seasonal plot'
 al.alert_type = 'info'
 if(s > s1):
    al.object='## Alert\nEnd Year is smaller than Start Year !'
    al.alert_type = 'warning'
    table_with_export_buttons.object = ""   
    return al
 elif((s == s1) &  (s2 > s3)):
    al.object='## Alert\nEnd Month is smaller than Start Month !'
    al.alert_type = 'warning'
    table_with_export_buttons.object = ""   
    return al
 #pn.param.ParamMethod.loading_indicator = True
 #ld.value=True
 '''
 a = pd.read_excel('subdivision_data_1901-2019 _m1.xlsx',engine='openpyxl')
 a = a.drop(['Column2','Column4','Column17','Column18','Column19','Column20','Column21'],axis = 1)
 b = a.set_index(['Column3','Column22']).stack().reset_index()
 b.columns = ['year','name','month','rain']
 b.month = b.month.astype(int)
 
 if 'stocks' not in pn.state.cache:
        return pn.indicators.LoadingSpinner(value=True)
        time.sleep(0.5)
 
 '''
 c =    getdata()  #      b.copy()
 c = c[c.name == s4]
 c = c[c.rain >= 0]
 
 #c = c[(c.year >= s) & (c.year <= s1)]
 
 #c = c[(c.month >= s2) & (c.month <= s3)]
  
 l1 = pd.to_datetime(str(s) + '-' + str(s2) + '-01')   
 l2 = pd.to_datetime(str(s1) + '-' + str(s3) + '-01')

  
 c['dates'] = pd.to_datetime(c.year.astype(str) + '-' + c.month.astype(str) + '-01')

 db1 = datetime.datetime.strptime(str(s2),"%m")
 m1 = db1.strftime("%b")
 db2 = datetime.datetime.strptime(str(s3),"%m")
 m2 = db2.strftime("%b")
 #db3 = datetime.datetime.strptime(str(s5),"%m")
 #m3 = db3.strftime("%b")
 title= 'Seasonal variation (' + str(m1) + '-' + str(m2) +   ') of Rainfall over '+ s4 + '<br> for the period ' + str(s) + '-'  + str(s1)
 
 c = c[(c.dates >= l1) & (c.dates <= l2)]
 diff = s3 - s2  
 if((diff == 0)):
     mm =  s3 #dd[s5]
     db1 = datetime.datetime.strptime(str(s3),"%m")
     m1 = db1.strftime("%B")
     gau.value= mm
     c = c[c.month == mm]
     title= 'Monthly variation (' + str(m1)  +   ') of Rainfall over '+ s4 + '<br> for the period ' + str(s) + '-'  + str(s1)
     #s2.value = s2
     #s3.value = s2
     #s2.param.precedence=-1
     #s3.param.precedence=-1
     c = c.reset_index()
 '''
 elif((diff == 'Month-Month')):
     #c = c[(c.month >= s2) & (c.month <= s3)]
     #c = c.set_index('dates').resample('Y').sum()
     #c.year  = c.index.year
     #c = c.replace(0,np.nan)
     title= 'Month to Month variation (' + str(m1) + '-' + str(m2) +   ') of Rainfall over '+ s4 + '<br> for the period ' + str(s) + '-'  + str(s1)
     c = c.reset_index()
 '''    
 elif((diff == 11)):
     c = c[(c.month >= 1) & (c.month <= 12)]
     c = c.set_index('dates').resample('Y').sum()
     c.year  = c.index.year
     c = c.replace(0,np.nan)
     title= 'Yearly variation ' +   ' of Rainfall over '+ s4 + '<br> for the period ' + str(s) + '-'  + str(s1)
     c = c.reset_index()
 elif((diff > 0))# & (radio_group == 'Seasonal')):
     c = c[(c.month >= s2) & (c.month <= s3)]
     c = c.set_index('dates').resample('Y').sum()
     c.year  = c.index.year
     c = c.replace(0,np.nan)
     title= 'Seasonal variation (' + str(m1) + '-' + str(m2) +   ') of Rainfall over '+ s4 + '<br> for the period ' + str(s) + '-'  + str(s1)
     c = c.reset_index()
        
 elif((diff < 0))# & (radio_group == 'Seasonal')):
     title= 'Seasonal variation (' + str(m1) + '-' + str(m2) +   ') of Rainfall over '+ s4 + '<br> for the period ' + str(s) + '-'  + str(s1)
     j1 = s2
     j2 = s3 +12
     j3 = list(range(j1,j2+1))
     j4 = [x%12 if x != 12 else x for x in j3]
     j4.sort()
     c['season'] = pd.Series(0,c.index)
     c = c[c.month.isin(j4)]
     n = len(j4)   
     ls = [c[i:i+n] for i in range(0,c.shape[0],n)]
     for y in  ls:
        y['s'] = pd.Series(y['year'].iloc[0],index = y.index)
     c = pd.concat(ls,axis = 0)
    

     #c['year'] = c.index.year
     #for i in range(len(c)):
     #   if(c.month.iloc[i] in j4):
     #    c['season'].iloc[i] = j3[j4.index(c.month.iloc[i])]


     #c = c[(c['season'] >= j3[0]) &  (c['season'] <= j3[-1])]
     #c = c.groupby('season').sum()   

     c = c.set_index('dates')#.resample('Y').sum()
     c = c.groupby('s').sum()
     #c = c.reset_index()
     #c['year'] =  c.index.year   
     c = c.reset_index()
     c.year = c['s']

 #c['year'] = c['year'].astype(str
 #c['year']  = pd.to_datetime(c['year'], format='%Y')
 m1 = c['rain'].idxmax()
 x1 = c['year'][m1]
 y1 = round(c['rain'][m1],2)
 # = pn.widgets.DataFrame(c)   
 #print(c)
 '''
 f = Figure(figsize=(12,9),dpi = 200)
 #cw = os.getcwd()
 
 #f.bbox.xmax-width
 plt.style.use('fivethirtyeight')   
 ax =f.subplots()
 FigureCanvas(f)
 #print(height)      
 ax.figure.figimage(im1, f.bbox.xmax-width, f.bbox.ymax-height)      
 
 
 db1 = datetime.datetime.strptime(str(s2),"%m")
 m1 = db1.strftime("%b")
 db2 = datetime.datetime.strptime(str(s3),"%m")
 m2 = db2.strftime("%b") 
 #Title: Seasonal variation (Jan-Mar) of rainfall over Bihar for the period 1901-2020
 f.suptitle('Seasonal variation (' + str(m1) + '-' + str(m2) +   ') of Rainfall over '+ s4 + '\n for the period ' + str(s) + '-'  + str(s1) , fontsize=20)
 
 #c.plot.line('year', 'rain', ax=ax)
 ax.plot(c.year,c.rain,marker = 'o')
 ax.set_xlabel('year')
 ax.set_ylabel('rainfall(mm)')
 #ax.quiver(x1,y1,1,1,color='red')      
 ax.text(x1,y1,'*max-->' + str(y1) +'(' + str(x1) + ')',color='red',ha='right',va='bottom')
 #date_form = DateFormatter("%Y")
 #ax.xaxis.set_major_formatter(date_form)  
   
 #ax.xaxis.set_ticks(np.arange(c.year.min()-1, c.year.max()+2, 10))
 #ax.set_xticklabels(ax.get_xticks(), rotation = 45)

 #c.plot.line('year','rain',ax = ax)
 #extent = ax.get_window_extent().transformed(f.dpi_scale_trans.inverted())
 #plt.savefig('figure.png',format='png',bbox_inches=extent)
 ax.set_xlim(c.year.min()-1,c.year.max()+2)
 ax.figure.savefig('figure.png')
 #ax.set_xlim(c.year.min()-1,c.year.max()+2)
 '''
       
 if((radio_group == 'Month-Month')):
  import calendar
  c['Month'] = c['month'].apply(lambda x: calendar.month_abbr[x])
  c['ym']= c['year'].astype(str) + '-' +  c['Month']
  f= px.line(c, x="year", y="rain", color='Month')#, symbol="Month")
  f.update_layout(xaxis_type='category')
 else:
  f=   go.Figure(go.Scatter(x=c['year'], y=c['rain'] ,mode='lines+markers' ))           
 im = Image.open(r"static/imd_logo.png")  
 f.layout.images = [dict(
        source=im,
        xref="paper", yref="paper",
        x=1.05, y=1.0,
        sizex=0.2, sizey=0.2,
        xanchor="center", yanchor="bottom"
      )]


 #db1 = datetime.datetime.strptime(str(s2),"%m")
 #m1 = db1.strftime("%b")
 #db2 = datetime.datetime.strptime(str(s3),"%m")
 #m2 = db2.strftime("%b")
 #title= 'Seasonal variation (' + str(m1) + '-' + str(m2) +   ') of Rainfall over '+ s4 + '<br> for the period ' + str(s) + '-'  + str(s1)
 f.update_layout(title= '<b>'+ title + '</b>',title_x=0.5,
                   xaxis_title='Year',
                   yaxis_title='Rainfall (mm)')

 #test_base64 = base64.b64encode(open('assets/imd_logo.png' , 'rb').read()).decode('ascii')

 
 f.add_annotation(
        x=x1,
        y=y1,
        xref="x",
        yref="y",
        text="max="+ str(y1) ,
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
        )


 '''
 f.add_annotation(x=x1, y=y1,
            text="*highest value",
            showarrow=True,
            arrowhead=1)

 '''
 

#f.add_layout_image(
#    dict(
#        source="static/imd_logo.png",
#        x=1, y=1.05,
#        #sizex=0.2, sizey=0.2,
#        xanchor="right", yanchor="bottom"
#    )
#)


 f.layout.autosize = True
 #f = pn.pane.Plotly(f,config={'responsive': True, 'displaylogo': False }) 
       
 plotly_pane7.object = f
 plotly_pane7.config={'responsive': True, 'displaylogo': False }
 l1 = ['mean','50%','std','max']
 k3 = c["rain"].describe()
 df_2 = pd.DataFrame({'Values': k3})
 df_2    = df_2.reset_index()
 df_2.columns = ['Statistics','values(mm)']
 df_2['values(mm)'] = df_2['values(mm)'].round(2)     
 df_2 = df_2[df_2['Statistics'].isin(l1)]
 df_2['Statistics'] = df_2['Statistics'].replace({'50%':'Median','mean':'Mean','std':'Standard Deviation','max':'Maximum Value'})
 df_2.loc[len(df_2.index)] = ['Year(Max Value)', c.loc[c['rain'].idxmax(), 'year']]
 df_2.set_index('Statistics',inplace=True)
 #print(df_2)
 d.value =  df_2
    
 html = df_2.to_html(classes=['example2', 'panel-df'])
 table_with_export_buttons.object = html+script
 #p2(s2,s3,s4)
 #p3(s4)
 #p4(s4)

 #def get_csv():
 #  return BytesIO(c.to_csv().encode())   
 
 #file_download_csv = pn.widgets.FileDownload(filename="data.csv", callback=kk, button_type="primary") 
 #file_download_csv =get_csv  
  


 #pn.param.ParamMethod.loading_indicator = False
 #ld.value=False         
 #return f#pn.pane.Matplotlib(f)
 c= getdata()
 import calendar
 c= c[c.name == s4]
 c['Month'] = c['month'].apply(lambda x: calendar.month_abbr[x])
 #c = c[c.rain >= 0]
 #c['year'] = c['year'].astype(int)
 c= c.replace(-99.9,np.nan)
 c['year-month']= c['year'].astype(str) + '-' +  c['Month']
 c = c.reset_index()
 idx = list(range(c.year.min(),c.year.max()+1))
 idx = [str(x) for x in idx]
 g = len(idx)
 idx1 =list(c['Month'].unique())   #   list(range(1,13))
 h = len(idx1)
 idx = idx*h
 idx1 = idx1*g
 idx.sort()
 res = [i +'-' +  j for i, j in zip(idx, idx1)]
 c = c.set_index('year-month')
 c = c.reindex(res, fill_value=np.nan)
 c = c.reset_index()
 c['month1'] = pd.to_datetime(c['year-month'], format='%Y-%b').dt.month
 c['year1'] = pd.to_datetime(c['year-month'], format='%Y-%b').dt.year
 c = c.sort_values(['year1','month1'])

 fig= px.line(c, x="year-month", y="rain",title='Available Monthly  data of '+ s4)#, color='Month')#, symbol="Month")
 fig.update_layout(xaxis_type='category',title_x=0.5)      
 #fig = px.bar(c, x="ym", y="rain", color="Month", title='monthly dataset of '+ s4) 
 fig.layout.autosize = True
 matpl.object = fig
 matpl.config={'responsive': True, 'displaylogo': False }
 





@pn.depends(s2.param.value,s3.param.value,s4.param.value,s5.param.value,  radio_group.param.value, watch=True)#,s3.param.value,s4.param.value, watch=True)
def p2(s2,s3,s4,s5, radio_group):#,s3,s4):
       # await asyncio.sleep(2)
        #if(s > s1):
         #  return
       # elif((s == s1) &  (s2 > s3)):
         #  return
        mm1 = s2  #strptime(st_mon,'%b').tm_mon
        mm2 = s3 #strptime(et_mon,'%b').tm_mon
        a = pd.read_excel('subdivision_data_1901-2019 _m1.xlsx',engine='openpyxl')
        a = a.drop(['Column2','Column4','Column17','Column18','Column19','Column20','Column21'],axis = 1)

        b = a.set_index(['Column3','Column22']).stack().reset_index()
       # print(b)
        b.columns = ['year','name','month','rain']
        b.month = b.month.astype(int)
        df2 = b.copy()
        df2 = df2[df2.name == s4]
        df2 = df2[df2.rain >= 0]
        pm = 'rain'
        un = 'rain(mm)'

  
        #l1 = pd.to_datetime(str(s) + '-' + str(s2) + '-01')   
        #l2 = pd.to_datetime(str(s1) + '-' + str(s3) + '-01')

  
        #df2['dates'] = pd.to_datetime(df2.year.astype(str) + '-' + df2.month.astype(str) + '-01')
        
        
        #df2 = data.copy() #df.copy()
        #df2 = df2.replace(-99.9,0)
        #df2 = df2[df2['Monthly_rain'] >= 0]
        df2['dates'] = pd.to_datetime(df2.year.astype(str) +'-'+ df2.month.astype(str))
        
        #a = pd.to_datetime(str(int(startdate)) + '-' +str(int(mm1))+'-01')
        #b = pd.to_datetime(str(int(enddate)) + '-'+ str(int(mm2)) + '-01')
        #cur_date = a.month
        #end =b.month
        
        
 
        
        #df2['season'] = pd.Series('1',df2.index)
        #for i in range(start_month,end_month,1):
        
        diff =  mm2 - mm1
        r = [1]
        
        df2 = df2.reset_index()
        
        
        if((radio_group == 'Monthly')):
           mm = dd[s5]
          #df = df[(df.year >= int(startdate)) & (df.year <= int(enddate))] 
           df2 = df2[df2.month ==  mm]
           df2 = df2.dropna()
           df2 = df2.reset_index()
           df2.set_index('dates', inplace=True)
           df2 = df2[pm]
        elif((radio_group == 'Month-Month')):
           df2 = df2.reset_index()
           df2.set_index('dates', inplace=True)
           df2 = df2[pm] 
        elif((radio_group == 'Yearly')):
           df2 = df2[(df2.month >= 1) & (df2.month <= 12)]
           df2 = df2.set_index('dates').resample('Ys').sum()
           df2 = df2.reset_index()
           df2['year'] = df2.dates.dt.year
           df2.set_index('dates', inplace=True)
           df2 = df2[pm]
        elif((diff > 0)): # & (radio_group == 'Seasonal')):
           #df = df[(df.year >= int(startdate)) & (df.year <= int(enddate))] 
           df2 = df2[(df2.month >= mm1) & (df2.month <= mm2)]
           df2 = df2.set_index('dates').resample('Ys').sum()
           df2 = df2.reset_index()
           df2['year'] = df2.dates.dt.year
           df2.set_index('dates', inplace=True)
           df2 = df2[pm]
           
         #r = list(range(int(start_month),int(end_month)))
        elif((diff <= 0)):# & (radio_group == 'Seasonal')):
           st1 = df2.year.max()
           st2 = df2.year.min()
           st3 = df2.month.max()
           st4 = df2.month.min()
           a = pd.to_datetime(str(int(st2)) + '-' +str(int(mm1))+'-01')
           b = pd.to_datetime(str(int(st1)) + '-'+ str(int(mm2)) + '-01')
           
           df2 = df2[(df2.dates >= a) & (df2.dates <= b)]
          
           
           #print(df2)
           df2 = df2.reset_index()
           #gg = []
           #sum = 0
           #df['sum1'] = pd.Series(0.0,df.index)
           #df['sum2'] = pd.Series('gg',df.index)
           
           t1 =  int(mm1)
           t2 =  int(mm2)+ 12
           r = list(range(t1,t2+1))
           r = [x%12 if x != 12 else x for x in r]
           r.sort()
           #df2['season'] = pd.Series(0,df2.index)
           df2 = df2[df2.month.isin(r)]
           
           n = len(r)   
           ls = [df2[i:i+n] for i in range(0,df2.shape[0],n)]
          
           for y in  ls:
            y['s'] = pd.Series(y['year'].iloc[0],index = y.index)
           df2 = pd.concat(ls,axis = 0)
          
           #df2 = df2.set_index('dates')#.resample('Y').sum()
           
           df2 = df2.groupby(['s'])['rain'].agg('sum') #.sum()
          
           df2= df2.reset_index()
           df2.year = df2['s']
           df2['dates'] = pd.to_datetime(df2.year.astype(str) +'-'+ '01')
           df2.set_index('dates', inplace=True)
           df2 = df2[pm]

        large5 = df2.nlargest(5)
        small5 = df2.nsmallest(5)

        small5= small5.reset_index()
        large5= large5.reset_index()

        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

        large5['status'] = "5 highest values"
        large5['rank'] = [ordinal(n) for n in range(1,6)]#range(1,6)
        large5['rank']  = large5['rank'].sort_values(ascending=False)
        small5['status'] = "5 lowest values"
        small5['rank'] = [ordinal(n) for n in range(1,6)]#range(1,6)
        small5['rank']  = small5['rank'].sort_values(ascending=False)

        df3 = large5

        title='5 highest ever recorded '
        df3 = df3.reset_index()
        for i in range(len(df3)):
         df3.dates[i] = df3.dates[i].year#.strftime("%Y")

        df3['Extreme_Values'] = 'Extreme'
        df3[pm] = df3[pm].round(2)

        df3.rename(columns={'dates': 'Year', pm: un}, inplace=True)
        df3.sort_values([un], ascending=False, inplace=True)
        #df3=df3.sort_values(by=[un], ascending=False)

        config={
            "displaylogo": False
        }
        #f = px.bar(df3, x="status" ,y=un,color='status',orientation='v',title=title + un,barmode = 'stack', hover_data=['Year'],template='plotly_white')#,pattern_shape=un)
        df3 = df3.reset_index()
        x1= list(df3[un].values)
        y1= list(df3['Year'].values)
        #x1.sort(reverse=True)
        #y1.sort(reverse=True)
        #data= dict(rain= x1, year=y1)
        #res = list(map(lambda(i, j): str(i) + '('+ str(j)+')', zip(x1, y1)))
        res = [str(i) + '('+ str(j) + ')'  for i, j in zip(x1, y1)]
        #f = go.Figure(go.Funnelarea(
        #text = res,
        #values = y1
        #))

        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen', 'white']
        stt= list(df3['rank'].values) 
        res1 = [str(i) + '('+ str(j) + ')'  for i, j in zip(stt, y1)]
        #f= go.Figure(data=[go.Pie(labels=res1,
        #                     values=x1)])
        #f.update_traces(hoverinfo='label', textinfo='value', textfont_size=20,
        #          marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        #f.update_layout(legend_title="Rank(Year)") 




        #f = go.Figure(go.Funnel(
        #y = y1, #["Website visit", "Downloads", "Potential customers", "Requested price", "Finalized"],
        #x = x1, #[39, 27.4, 20.6, 11, 2],
        #textposition = "inside",
        #textinfo = "value",
        #opacity = 0.65, marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
        #"line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
        #connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}})
        #)

        percentile_list = pd.DataFrame(
        {'year': y1,
        'rain': x1
        })
        col_one_list1 = df3[un].tolist()
        #col_one_list1.sort(reverse=True)
        col_one_list2 = df3['Year'].tolist()
        col_one_list2= [str(x) for x in col_one_list2]
        res2 = [str(i) + '('+ str(j) + ')'  for i, j in zip(col_one_list1,  col_one_list2)]
        df3['Year']=df3['Year'].astype(str)
        f= px.funnel(df3, x=un, y='Year') #, color='rank')
        #f = go.Figure(go.Funnel(name = '5 highest values',
        #y =   col_one_list2 ,
        #x = col_one_list1,
        #textinfo = "value",
        #opacity = 0.65, marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
        #"line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
        #connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}} )) 
        #f = go.Figure()

        #f.add_trace(go.Funnel(
        #orientation = "h",
        #y = list(df3['Year']),
        # x = list(df3[un]),
        #textposition = "inside",
        #))
        #f = px.bar(df3, x=un ,y='Year',color='status',orientation='h',title=title + un,barmode = 'stack', hover_data=['Year'],template='plotly_white')#,pattern_shape=un)
        #f= px.funnel(df3, x=un, y='Year', color='status')
        #f = px.funnel(percentile_list,x='rain', y='year')
        #f = go.Figure(go.Funnel(x=df3[un], y=df3['Year']) ) 
        #f =px.sunburst(df3,path=['status', 'rank'], values=un,hover_data=['Year'],template='simple_white',color = un)
        f.update_layout(title='<b>'+title + un+'</b>',title_x=0.5)
        f.update_layout(modebar_remove=['toImageButtonOptions','zoom', 'pan','select', 'zoomIn', 'zoomOut','lasso2d','sendDataToCloud','toImage']
         )
        f.update_yaxes(showgrid= False,visible= False)#range=[min(df3[un])-2,max(df3[un])+2])
        f.update_xaxes(showgrid= False)#range=[min(df3[un])-2,max(df3[un])+2])
        
        f.layout.autosize = True
        #plotly_pane = pn.pane.Plotly(f,config={'responsive': True, 'displaylogo': False }) 
       
        plotly_pane8.object = f
        plotly_pane8.config={'responsive': True, 'displaylogo': False }

        #plotly_pane = pn.pane.Plotly(f) 
       
        #return plotly_pane
        '''
        c= getdata()
        c= c[c.name == s4]
        c= c.replace(-99.9,0)
        c['ym']= c['year'].astype(str) + '-' +  c['month'].astype(str)
  
        m1 = c['rain'].idxmax()
        x1 = c['year'][m1]
        y1 = round(c['rain'][m1],2)
        f = Figure(figsize=(9,7),dpi = 200)

        plt.style.use('fivethirtyeight')   
        ax =f.subplots()
        FigureCanvas(f)
       
        ax.figure.figimage(im1, f.bbox.xmax-width, f.bbox.ymax-height)      
 
 
       
        f.suptitle('monthly dataset of '+ s4, fontsize=20)
 
        ax.plot(c.ym,c.rain,marker = 'o')
        ax.set_xlabel('year')
        ax.set_ylabel('rainfall(mm)')
       
        #ax.text(x1,y1,'*max-->' + str(y1) +'(' + str(x1) + ')',color='red',ha='right',va='bottom')
        #ax.set_xlim(c.year.min()-1,c.year.max()+2)
        #ax.figure.savefig('figure.png')
        matpl.object = f
        matpl.dpi=200
        '''
        

     




@pn.depends(s4.param.value)#,s1.param.value,s2.param.value,s3.param.value,s4.param.value)
def p3(s4): #,s1,s2,s3,s4):
      # await asyncio.sleep(2)
       a = pd.read_excel('subdivision_data_1901-2019 _m1.xlsx',engine='openpyxl')

       a = a[['Column3','Column22','Column18','Column19','Column20','Column21']]
       a.columns = ['year','name','JF','MAM','JJAS','OND']

       #a = a.drop(['Column2','Column4','Column17','Column18','Column19','Column20','Column21'],axis = 1)

       b = a.set_index(['year','name']).stack().reset_index()
       #print(b)
       b.columns = ['year','name','seasons','rainfall(mm)']
       b = b[b.name == s4]
       b = b.replace(-99.9,0)
       #b.month = b.month.astype(int)
       #b['color'] = np.where(b.seasons =='JS','red',np.where(b.seasons =='JJAS','blue',np.where(b.seasons =='MM','green','white')))
       f = px.bar(b,x='year',y='rainfall(mm)',color='seasons',color_discrete_sequence=['red','blue','green','goldenrod'])#,barmode='group')

       f.update_layout(title='<b>Seasons('+s4+ ')</b>',title_x=0.5)
       #f.update_layout(xaxis = dict(rangeslider = dict(visible=True),type='date'),template='plotly_white')
       f.update_layout(modebar_remove=['toImageButtonOptions','zoom', 'pan','select', 'zoomIn', 'zoomOut','lasso2d','sendDataToCloud','toImage'])
       #f.update_yaxes(showgrid= False,visible= False)#range=[min(df3[un])-2,max(df3[un])+2])
       #f.update_xaxes(showgrid= False)#range=[min(df3[un])-2,max(df3[un])+2])
        
       f.layout.autosize = True

       plotly_pane5.object = f
       plotly_pane5.config={'responsive': True, 'displaylogo': False }


       #plotly_pane1 = pn.pane.Plotly(f,config={'responsive': True, 'displaylogo': False }) 
       
       
       #return plotly_pane1





@pn.depends(s4.param.value)#,s1.param.value,s2.param.value,s3.param.value,s4.param.value)
def p4(s4):#,s1,s2,s3,s4):
    #   await asyncio.sleep(2)
       a = pd.read_excel('subdivision_data_1901-2019 _m1.xlsx',engine='openpyxl')

       a = a[['Column3','Column22','Column18','Column19','Column20','Column21']]
       a.columns = ['year','name','JF','MAM','JJAS','OND']

       #a = a.drop(['Column2','Column4','Column17','Column18','Column19','Column20','Column21'],axis = 1)

       b = a.set_index(['year','name']).stack().reset_index()
       #print(b)
       b.columns = ['year','name','seasons','rainfall(mm)']
       b = b[b.name == s4]
       b = b.replace(-99.9,0)
       #b.month = b.month.astype(int)
       #b['color'] = np.where(b.seasons =='JS','red',np.where(b.seasons =='JJAS','blue',np.where(b.seasons =='MM','green','white')))
     

       

     
       
       s1 = b['rainfall(mm)'].min()
       s2 = b['rainfall(mm)'].max() + 10
       f1=px.bar(b, x='seasons',y = 'rainfall(mm)', hover_name = "year", color='seasons',
            animation_frame= 'year', barmode='group',range_y=[s1,s2])
       f1.update_layout(title='<b>Seasons('+s4+ ')</b>',title_x=0.5)
       #f.update_layout(xaxis = dict(rangeslider = dict(visible=True),type='date'),template='plotly_white')
       f1.update_layout(modebar_remove=['toImageButtonOptions','zoom', 'pan','select', 'zoomIn', 'zoomOut','lasso2d','sendDataToCloud','toImage'])
       plotly_pane2 = pn.pane.Plotly(f1) 
       f1.layout.autosize = True
       plot(f1, filename= 'season_anime.html' , show_link=False,include_plotlyjs='cdn', 
       config=dict(displaylogo=False,
                 modeBarButtonsToRemove=['sendDataToCloud']))
       #f1.write_html('season_anime.html',include_plotlyjs='cdn')
    
       
       #plotly_pane2 = pn.pane.Plotly(f1,config={'responsive': True, 'displaylogo': False }) 
   


       f2=codecs.open("season_anime.html", 'r')
       plotly_pane6.object = f2.read()

       




      # html_pane = pn.pane.HTML(f2.read())
       
      # return html_pane








 #k = plt.plot(c.year,c.rain)
 #return pn.pane.Matplotlib(k,width = 400,height =400)
 #return f #plt.gcf()
 #k = go.Scatter(x=c.year,y=c.rain)
 #return pn.pane.Plotly(k,width = 400,height =400)
#f1 = p1(s,s1,s2,s3,s4)
#k1 = pn.pane.Plotly(p1)
value1 = "Dear user!  Welcome to the data visualization of Seasonal Variation of rainfall of Subdivision  . Select start year , start month, end year , end month from the dropdown given below "
value2 = "Monthly series of rainfall for 36 subdivisions of India are used for this analysis. More details regarding the data set is available at https://imdpune.gov.in/Clim_Pred_LRF_New/Reports.html"

value = value1# + value2
bb = pn.widgets.TextToSpeech(name = "Speech Synthesis",value = value,auto_speak = False)
text = pn.Param(bb.param.value)

text1 = pn.Row(bb.controls(jslink=False), bb, width=600,height = 100)


def btt(event):
    #bb.voice= bb.voices[2]    
    bb.speak = True
    bb.volume = 1
    bb.pitch = 1
    bb.rate = 1
    bb.lang = 'en-US'
    

video = pn.pane.Video('https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_640_3MG.mp4', loop=True)


button = pn.widgets.Button(name='Click me for Audio Instructions', button_type='primary')
button.on_click(btt)
box2 = pn.WidgetBox('# Instructions', button,bb, video)


def btt1(event):
    #bb.voice= bb.voices[2]    
    bb1.speak = True
    bb1.volume = 1
    bb1.pitch = 1
    bb1.rate = 1
    bb1.lang = 'en-US'


value4= 'Dynamic charts given below visualizes variation of rainfall of subdivision with seasons in selected period . Here JF, MAM, JJAS, OND corresponds to different seasons in a year'
bb1 = pn.widgets.TextToSpeech(name = "Speech Synthesis",value = value4,auto_speak = False)
button1 = pn.widgets.Button(name='Instructions', button_type='success')
button1.on_click(btt1)
box3 = pn.WidgetBox('# Description', button1,bb1)



'''
bootstrap.sidebar.append(s4)
bootstrap.sidebar.append(s)
bootstrap.sidebar.append(s1)
bootstrap.sidebar.append(s2)
bootstrap.sidebar.append(s3)
#bootstrap.sidebar.append(file_download_csv)
bootstrap.sidebar.append(text1)
bootstrap.main.append(pn.Column(file_download,pn.Card(p1,width = 100),pn.Row(pn.Card(table_with_export_buttons),p2)))
#bootstrap.servable()
#websocket_origin = "192.168.0.103:8080",
#k = pn.Row(pn.Column(title,s4,s,s1,s2,s3,d),p1)#.controls(jslink=True),p1)
#k#.servable()

#bootstrap.servable(title="Seasonal Variation");

#strr = p3(s,s1,s2,s3,s4)
gif_pane = pn.pane.GIF('coil.gif')
box = pn.WidgetBox('# Select Box', al, s4,s,s1,s2,s3,text1)

d6 = pn.Column(pn.Card(file_download,pn.panel(p1,loading_indicator=True),title='Visualization',sizing_mode = 'stretch_width'))
a6 = pn.Row(d6,pn.Card(gif_pane,title='Gowing Visualization of seasonal variation of rainfall'))
b6 = pn.Row(pn.Card(table_with_export_buttons,title='Statistical Table',collapsible =False,background='WhiteSmoke',header_background='success'), pn.Card(p2,title='Highest 5 ever recorded rain'))
c6 = pn.Column(a6,b6,sizing_mode='stretch_both')                                                                                                                                        

kks = pn.Card(pn.Row(table_with_export_buttons,p2),title='Statistical Table for selected period',collapsible =False,background='WhiteSmoke',header_background='success',sizing_mode = 'stretch_width')
kks1 = pn.Card(pn.Row(p3,p4),sizing_mode = 'stretch_width')
box1 = pn.FlexBox(*[pn.Column(file_download,pn.panel(p1,loading_indicator=True)),kks1,kks])
column_box = box1.clone(flex_direction='column')

gsp = pn.GridSpec(sizing_mode='stretch_both')
gsp[0,0:1] = pn.Column(file_download,pn.panel(p1,loading_indicator=True))
gsp[0,2:3] =  gif_pane
gsp[1,0:1] = table_with_export_buttons
gsp[1,2:3] = p2

'''
#p6=asyncio.get_event_loop().run_until_complete(p1(s, s1, s2, s3, s4)) 

#w1 = pn.Column(pn.Card(file_download, plotly_pane7,  pn.panel(p1,loading_indicator=False)))
z1=  pn.Card(matpl)
w1 = pn.Card(plotly_pane7)

w2 = pn.Card(pn.Row(  plotly_pane5,plotly_pane6 ),sizing_mode = 'stretch_width')
w3 =  pn.Card(pn.Row(table_with_export_buttons, plotly_pane8),title='Statistical Table for selected period',collapsible =False,background='WhiteSmoke',header_background='success',sizing_mode = 'stretch_width')
w4 = pn.Column(z1,w1,  box3, w2,w3,p2,p1,p3, p4, p5)



pn.template.FastListTemplate(title="O/o Climate Research and Services,IMD Pune",  header=pn.panel('static/imd_logo.png',height=50),
                            sidebar = [box2,s4,s,s1,s2,s3],  
                            main =[w4]).servable();




#pn.template.FastListTemplate(header=pn.panel('static/imd_logo.png',height=40),   title="Seasonal Variation", 
#                            sidebar = [al,s4,s,s1,s2,s3,text1],  
#                            main = [pn.Card(pn.Column(file_download,pn.Card(pn.panel(p1,loading_indicator=True),title='Visualization',sizing_mode = 'stretch_width'
#),gif_pane,pn.Row(pn.Card(table_with_export_buttons,title='Statistical Table',collapsible =False,background='WhiteSmoke',header_background='success'),
#                                                                                                                                         pn.Card(p2,title='Highest 5 ever recorded rain')  )))]).servable();

#pn.serve(bootstrap,websocket_origin = "season-var.herokuapp.com",address="0.0.0.0")#,port = 8085)#.save('test.html')#,embed=True,embed_json=True,max_states= 3)
#sizing_mode = 'stretch_both'


#ppn.pane.panel(k)
#p.save('test.html',embed=True,resources=INLINE)#,embed_json=False)
#https://panel.holoviz.org/_static/logo_horizontal.png
