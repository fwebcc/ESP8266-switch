from simple import MQTTClient
import time,dht,machine
from machine import Pin,Timer
import network
import json
#接口定义
led=Pin(12,Pin.OUT, value=0)
Button = Pin(14,Pin.IN, value=0)
#网络定义
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#读取配置Json文件
f = open("Settings.json", encoding='utf-8')
setting = json.load(f)
#链接MQTT服务器参数
c = MQTTClient('ESP8266_'+setting['MQTT_Topic']+'', setting['MQTT'],setting['MQTT_PORT'],setting['MQTT_Topic'],setting['MQTT_PASS'])
#c.connect()
#上传MQTT数据——开关
def msg_up():
    if led.value()==1:
        c.publish(''+setting['MQTT_Topic']+'/I','ON')
    if led.value()==0:
        c.publish(''+setting['MQTT_Topic']+'/I','OFF')

#MQTT接收信息处理
def sub_cb(topic, msg):
    print(topic, msg)
    global Time_d
    if topic==b''+setting['MQTT_Topic']+'/C':
        if msg==b'OFF':
              led.off()
              UP_MQTT_MSG()
        if msg==b'ON':
              led.on()
              UP_MQTT_MSG()
#MQTT接收信息
def msg_connect():
           c.set_callback(sub_cb)
           c.connect()
           c.subscribe(b''+setting['MQTT_Topic']+'/C')
#msg_connect()
#检测按钮状态
Time_c =0
def Button_s():
   global Time_c
   if Button.value() == 1:
        if  Time_c == 0:
            if led.value()==0:
              led.on()
              UP_MQTT_MSG()
            else:
              led.off()
              UP_MQTT_MSG()
        else:
            if  Time_c > 250:
                 print('执行重启任务')
                 tim1.deinit()
                 tim2.deinit()
                 tim3.deinit()
                 machine.reset()
                 Time_c =0
        Time_c +=1
   else:
        Time_c =0
#判断有无网络
Time_d =0
def IF_NETWORK():
    global Time_d
    if setting['AP'] ==  'False':
      if not wlan.isconnected:
        Time_d =0
        print('网络已断开')
        wlan.config(dhcp_hostname=setting['MQTT_Topic'])
        wlan.connect(setting['ESSID'], setting['PASSWORD'])
        heartbeat()
        print('network config:', wlan.ifconfig())
    else:
      print('AP模式')
      tim2.deinit()
      tim3.deinit()
      wlan.active(False)
      ap_if = network.WLAN(network.AP_IF)
      ap_if.active(True)
      ap_if.config(essid='AP_'+setting['MQTT_Topic'],password=setting['AP_PASSWORD'])
      print('AP START MODE network...')
      print('network config:',ap_if.ifconfig())
#有无网络启动
def heartbeat():
   try:
       c.connect()
       msg_connect()
       msg_up()
       c.check_msg()
   except OSError:
       #IF_NETWORK()
       print('无网络_心跳传输')

heartbeat()
#定时执行接收信息
def UP_MQTT():
  if not wlan.isconnected():
        print('无网络_定时接收信息')
  else:
        try:
            c.check_msg()
            global Time_d
            print (Time_d)
            if  Time_d < 3:
                heartbeat()
                Time_d += 1
                print('链接检查网络信息')
            print('检查网络信息')
        except OSError:
            heartbeat()
#按钮信息反馈
def UP_MQTT_MSG():
    try:
       msg_up()
       print('在上传资料')
    except OSError:
       heartbeat()
#定时执行任务
tim = Timer(-1)
tim.init(period=500, mode=Timer.PERIODIC, callback=lambda t:Button_s())
tim2 = Timer(-1)
tim2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:UP_MQTT())
tim3 = Timer(-1)
tim3.init(period=30000, mode=Timer.PERIODIC, callback=lambda t:IF_NETWORK())
print('MQTT START')
