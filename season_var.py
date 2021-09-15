from PIL import Image
import matplotlib.cbook as cbook
import matplotlib.image as image


from time import strptime
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go

import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvas
import plotly.graph_objects as go
#from bokeh.resources import INLINE
import panel as pn
import numpy as np
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
    
pn.extension(loading_spinner='dots',loading_color='#00aa41',sizing_mode = 'stretch_width',css_files=css, js_files=js)
#template = 'bootstrap'



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


a = pd.read_excel('subdivision_data_1901-2019 _m1.xlsx',engine='openpyxl')
a = a.drop(['Column2','Column4','Column17','Column18','Column19','Column20','Column21'],axis = 1)

b = a.set_index(['Column3','Column22']).stack().reset_index()
#print(b)
b.columns = ['year','name','month','rain']
b.month = b.month.astype(int)



title = '## hello'
m5 = list(b['name'].unique())
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
s4 = pn.widgets.Select(name = 'subdivision',options =m5,width = 100)

k = s4.value
k1 = b[b.name == k]
m1 = int(k1.year.min())
m2 = int(k1.year.max())
m3 = list(range(m1,m2+1))
m4 = list(k1.month.unique())
s = pn.widgets.Select(name = 'start year',options =m3,width = 100)
s1 = pn.widgets.Select(name = 'end year',options =m3,width=100)
s2 = pn.widgets.Select(name = 'star month',options =m4,width = 100)
s3 = pn.widgets.Select(name = 'end month',options =m4,width = 100)

#s.jslink(s4,value='value')
#s1.jslink(s4,value='value')
#s2.jslink(s4,value='value')
#s3.jslink(s4,value='value')

#d = pn.widgets.DataFrame(b)  

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

d  = pn.widgets.DataFrame(width = 300,height = 400)  

table_with_export_buttons = pn.pane.HTML("<h1>hello</h1>",sizing_mode='stretch_width', margin=(10,5,25,5))

#file_download_csv = pn.widgets.FileDownload(filename="Statistical.csv", button_type="primary")   

file_download = pn.widgets.FileDownload(file='figure.png',button_type='success',label='Download',name='Click to download chart')

al = pn.pane.Alert("Hello")  

@pn.depends(s.param.value,s1.param.value,s2.param.value,s3.param.value,s4.param.value)
def p1(s,s1,s2,s3,s4):
 al.object='welcome to seasonal plot'
 al.alert_type = 'info'
 if(s > s1):
    al.object='## Alert\nEnd Year is smaller than Start Year!'
    al.alert_type = 'warning'
    table_with_export_buttons.object = ""   
    return al   
 pn.param.ParamMethod.loading_indicator = True
 c = b.copy()
 c = c[c.name == s4]
 c = c[c.rain >= 0]
 
 #c = c[(c.year >= s) & (c.year <= s1)]
 
 #c = c[(c.month >= s2) & (c.month <= s3)]
  
 l1 = pd.to_datetime(str(s) + '-' + str(s2) + '-01')   
 l2 = pd.to_datetime(str(s1) + '-' + str(s3) + '-01')

  
 c['dates'] = pd.to_datetime(c.year.astype(str) + '-' + c.month.astype(str) + '-01')

 c = c[(c.dates >= l1) & (c.dates <= l2)]
 diff = s3 - s2  
 if(diff == 0):
     c = c[c.month == s2]
     c = c.reset_index()
 elif(diff > 0):
     c = c[(c.month >= s2) & (c.month <= s3)]
     c = c.set_index('dates').resample('Y').sum()
     c.year  = c.index.year
     c = c.reset_index()
        
 elif(diff < 0):
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


 m1 = c['rain'].idxmax()
 x1 = c['year'][m1]
 y1 = round(c['rain'][m1],2)
 # = pn.widgets.DataFrame(c)   
 #print(c)
 f = Figure(figsize=(12,7),dpi = 200)
 #cw = os.getcwd()
 im1 = Image.open('static/imd_logo.png')
 sz = im1.size
 sz1 = (int(sz[0]/2), int(sz[1]/2))
 height = im1.size[1]
 width = im1.size[0]
 im1 = np.array(im1).astype(np.float) / 255
 #f.bbox.xmax-width
 plt.style.use('fivethirtyeight')   
 ax =f.subplots()
 print(height)      
 ax.figure.figimage(im1, f.bbox.xmax-width, f.bbox.ymax-height)      
 FigureCanvas(f)
 db1 = datetime.datetime.strptime(str(s2),"%m")
 m1 = db1.strftime("%b")
 db2 = datetime.datetime.strptime(str(s3),"%m")
 m2 = db2.strftime("%b")                                 
 f.suptitle('seasonal variation of '+ s4 + ' from ' + m1+ ' ' + str(s) + ' to ' + m2 + str(s1) , fontsize=20)
 ax.plot(c.year,c.rain,marker = 'o')
 ax.set_xlabel('year')
 ax.set_ylabel('rain')
 #ax.quiver(x1,y1,1,1,color='red')      
 ax.text(x1,y1,'max=' + str(y1) +'(' + str(x1) + ')',color='red',ha='right',va='bottom')   
 #c.plot.line('year','rain',ax = ax)
 #extent = ax.get_window_extent().transformed(f.dpi_scale_trans.inverted())
 #plt.savefig('figure.png',format='png',bbox_inches=extent)
 ax.figure.savefig('figure.png')
 ax.set_xlim(c.year.min()-1,c.year.max()+2)
 l1 = ['mean','50%','std','max']
 k3 = c["rain"].describe()
 df_2 = pd.DataFrame({'Values': k3})
 df_2    = df_2.reset_index()
 df_2.columns = ['Statistics','values']
 df_2['values'] = df_2['values'].round(2)     
 df_2 = df_2[df_2['Statistics'].isin(l1)]
 df_2['Statistics'] = df_2['Statistics'].replace({'50%':'Median','mean':'Mean','std':'Standard Deviation','max':'Maximum'})
 df_2.set_index('Statistics',inplace=True)
 print(df_2)
 d.value =  df_2
    
 html = df_2.to_html(classes=['example2', 'panel-df'])
 table_with_export_buttons.object = html+script
 def get_csv():
    return BytesIO(c.to_csv().encode())   
 
 #file_download_csv = pn.widgets.FileDownload(filename="data.csv", callback=kk, button_type="primary") 
 #file_download_csv =get_csv  
  


 pn.param.ParamMethod.loading_indicator = False   
 return f





@pn.depends(s.param.value,s1.param.value,s2.param.value,s3.param.value,s4.param.value)
def p2(s,s1,s2,s3,s4):
        if(s > s1):
           return          
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
        un = 'rain'

  
        l1 = pd.to_datetime(str(s) + '-' + str(s2) + '-01')   
        l2 = pd.to_datetime(str(s1) + '-' + str(s3) + '-01')

  
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
        
        
        if(diff == 0):
          #df = df[(df.year >= int(startdate)) & (df.year <= int(enddate))] 
          df2 = df2[df2.month ==  mm2]
          df2 = df2.dropna()
          df2 = df2.reset_index()
          df2.set_index('dates', inplace=True)
          df2 = df2[pm]
           
        elif(diff > 0):
           #df = df[(df.year >= int(startdate)) & (df.year <= int(enddate))] 
           df2 = df2[(df2.month >= mm1) & (df2.month <= mm2)]
           df2 = df2.set_index('dates').resample('Ys').sum()
           df2 = df2.reset_index()
           df2['year'] = df2.dates.dt.year
           df2.set_index('dates', inplace=True)
           df2 = df2[pm]
           
         #r = list(range(int(start_month),int(end_month)))
        elif(diff < 0):
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
           
           df2 = df2.groupby(['s'])['Monthly_rain'].agg('sum') #.sum()
          
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
        df3.sort_values(un,inplace=True)

        config={
            "displaylogo": False
        }
        #f = px.bar(df3, x="status" ,y=un,color='status',orientation='v',title=title + un,barmode = 'stack', hover_data=['Year'],template='plotly_white')#,pattern_shape=un)
        df3 = df3.reset_index()
        f =px.sunburst(df3,path=['status', 'rank'], values=un,hover_data=['Year'],template='simple_white',color = un)
        f.update_layout(title='<b>'+title + un+'</b>',title_x=0.5)
        f.update_layout(modebar_remove=['toImageButtonOptions','zoom', 'pan','select', 'zoomIn', 'zoomOut','lasso2d','sendDataToCloud','toImage']
         )
        f.update_yaxes(showgrid= False,visible= False)#range=[min(df3[un])-2,max(df3[un])+2])
        f.update_xaxes(showgrid= False)#range=[min(df3[un])-2,max(df3[un])+2])
        
        plotly_pane = pn.pane.Plotly(f)
        return plotly_pane

     

















 #k = plt.plot(c.year,c.rain)
 #return pn.pane.Matplotlib(k,width = 400,height =400)
 #return f #plt.gcf()
 #k = go.Scatter(x=c.year,y=c.rain)
 #return pn.pane.Plotly(k,width = 400,height =400)
#f1 = p1(s,s1,s2,s3,s4)
#k1 = pn.pane.Plotly(p1)
value = "welcome to the data visualization of Seasonal Variation  of Subdivision  . Select start year , start mnth,end year ,end month from the dropdown given above "
bb = pn.widgets.TextToSpeech(name = "Speech Synthesis",value = value,auto_speak = False)
text = pn.Param(bb.param.value)

text1 = pn.Row(bb.controls(jslink=False), bb, width=600,height = 100)







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


#https://panel.holoviz.org/_static/logo_horizontal.png
pn.template.FastListTemplate(header=pn.panel('static/imd_logo.png',height=40),   title="Seasonal Variation", 
                            sidebar = [al,s4,s,s1,s2,s3,text1],
                            main = [pn.Card(pn.Column(pn.Card(file_download,p1,sizing_mode = 'stretch_both',title='Seasonal Variation'),pn.Row(pn.Card(table_with_export_buttons,title='Statistical Table'),p2)))]).servable();

#pn.serve(bootstrap,websocket_origin = "season-var.herokuapp.com",address="0.0.0.0")#,port = 8085)#.save('test.html')#,embed=True,embed_json=True,max_states= 3)





#ppn.pane.panel(k)
#p.save('test.html',embed=True,resources=INLINE)#,embed_json=False)
