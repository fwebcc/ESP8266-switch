import network
import json
#读取配置Json文件
f = open("Settings.json", encoding='utf-8')
setting = json.load(f)
#MAC地址
#wlan = network.WLAN(network.STA_IF)
#s = wlan.config('mac')
#mymac = ('%02x-%02x-%02x-%02x-%02x-%02x') %(s[0],s[1],s[2],s[3],s[4],s[5])
#开启WIFI链接
def GO_wifi():
       wlan = network.WLAN(network.STA_IF)
       if not wlan.isconnected():
          wlan.active(False)
          wlan.active(True)
          wlan.config(dhcp_hostname=setting['MQTT_Topic'])
          wlan.connect(setting['ESSID'], setting['PASSWORD'])
          print('链接失败无网络', wlan.ifconfig())
       else:
          print('链接成功', wlan.ifconfig())

#判断网络链接没开启开启AP
def AP_START():
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(True)
        ap_if.config(essid='AP_'+setting['MQTT_Topic'],password=setting['AP_PASSWORD'])
        print('AP START MODE network...')
        print('network config:',ap_if.ifconfig())
        exec(open('./mqtt.py').read(),globals())
#判断网络链接是否开启
def DO_WIFI():
    if setting['AP'] ==  'False':
        GO_wifi()
        print('WIFI_START')
    else:
        AP_START()
        print('AP_START')
DO_WIFI()
