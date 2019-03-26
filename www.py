from machine import Pin,Timer
import socket,sys,machine,gc,time,json
html= '''<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>SOME.CF</title>
</head>
<body>
<div style="width:400px; margin:0 auto">
<div style="background:#d9edf7; color:#31708f; border-radius:5px; padding: 5px"">
            <h5>开关状态：<a href="/LED=%s"><button style="background:%s">%s</button></a> </h5>
</div><br>
<div style="background:#dff0d8; color:#3c763d; border-radius:5px; padding: 10px"">
            <h3>WIFI</h3>
            <hr>
<form action="/" method="get">
            <h5>SSID：<input type="text" name="ESSID" value= %s /></h5>
            <h5>PASS：<input type="text" name="PASSWORD" value= %s /></h5>
            <h5>AP WIFI PASS：<input type="text" name="AP_PASSWORD" value= %s /> </h5>
            <p>主题: <input type="text" name="MQTT_Topic" value= %s /> </p>
            <p>OPEN AP:<input type="checkbox" name="AP" value="True" %s /></p>
            <input type="submit" value="保存" />
</form>

<h5>重启：<a href="/RESTART"><button >重启</button></a> </h5>
</div>
</div>
</body>
</html>
'''
import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('0.0.0.0',80))
s.listen(5)
print('listening on', addr)

#批量修改json文件
def json_writes(ini_p,ini_k):
     f =open(ini_p,'rb')
     data =json.load(f)
     text = json.loads(ini_k)
     for i in text:
            data[i[0]]=i[1]
            fs =open(ini_p,'w')
            fs.write(json.dumps(data))
            fs.close()
     f.close()
     return 'OK'


def www():
  while 1:
    f = open("Settings.json", encoding='utf-8')
    setting = json.load(f)
    cl, addr = s.accept()
    request = cl.recv(1024)
    request = request.decode()
    request = request.replace('GET', 'GET:').replace('HTTP/1.1', '').strip().split('\r\n')
    request = {x.split(':')[0].strip(): ("".join(x.split(':')[1:])).strip().replace('//', "://") for x in request}
    #开关按钮
    if request['GET']== "/LED=ON":
        led.on()
        UP_MQTT_MSG()
    elif request['GET']== "/LED=OFF":
        led.off()
        UP_MQTT_MSG()
    elif request['GET']== "/RESTART":
        machine.reset()
    elif request['GET'].find("ESSID") != -1:
        vurl0 = request['GET'].replace('/?ESSID', "ESSID").strip().split('&')
        vurl = {x.split('=')[0].strip(): ("".join(x.split('=')[1:])).strip().replace('//', "://") for x in vurl0}
        if request['GET'].find("AP=") != -1:
           APS= vurl['AP']
        else:
           APS= 'False'
        VAL='[["ESSID":"'+vurl['ESSID']+'"],["PASSWORD":"'+vurl['PASSWORD']+'"],["AP_PASSWORD":"'+vurl['AP_PASSWORD']+'"],["MQTT_Topic":"'+vurl['MQTT_Topic']+'"],["AP":"'+APS+'"]]'
        #print(VAL)
        json_writes("Settings.json",VAL)
    #开关按钮控制
    if led.value()== 1:
              LedState='OFF'
              textd='关'
              clou='green'
    else:
              LedState='ON'
              textd='开'
              clou=''
    #AP状态
    if setting['AP'] == 'False':
              check='check'
    else:
              check='checked="checked"'

    response =  html % (LedState, clou, textd, setting['ESSID'], setting['PASSWORD'], setting['AP_PASSWORD'], setting['MQTT_Topic'], check)
    cl.sendall(response)
    cl.close()
www()
