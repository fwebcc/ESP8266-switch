# ESP8266-switch
基于micropython可以触控和MQTT控制的按钮开关

1.下载http://www.micropython.org/download#esp8266
刷入ESP8266
建议刷入http://www.micropython.org/resources/firmware/esp8266-20180511-v1.9.4.bin
高版本好像链接软件链接不了

2.使用http://fweb.cc/soft/PC/ESP8266.zip

3.把每个文件上传,并修改Settings.json中的"ESSID": "自己无线账号"，"PASSWORD": "自己无线密码"， "MQTT_Topic": "需要链接的主题"。MQTT服务器MQTT用户名密码等！

4.触控安装为点控高频输入接口为GPI14 开关控制按钮GPI12

5.测试版本有诸多不完善，请大家多修改

