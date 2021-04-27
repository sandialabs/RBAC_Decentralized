
import subprocess
import sys
import time
import schedule
netid = 1200


def start():
    global netid
    subprocess.call(['/opt/anaconda3/bin/python ./rbac_application.py ' + str(netid)], shell=True)
    subprocess.Popen(['/opt/anaconda3/bin/python ./app.py ' + str(netid)], shell=True)
    time.sleep(300)
    subprocess.Popen(['./client/vue_run.sh'], shell=True)
    print("Web Server is up and running...")


def end():
    global netid

    script1 = './app.py'
    script2 = './free_ports.sh'

    subprocess.check_call(['pkill','-9','-f', script1])
    time.sleep(30)

    subprocess.Popen([script2], shell = True)
    time.sleep(30)

    data_dir = '.ganache/data' + str(netid)
    subprocess.call(['./deleter.sh %s' %(data_dir)], shell = True)
    time.sleep(60)

    netid = netid + 1
    print(netid)


schedule.every().day.at("00:00").do(end)
schedule.every().day.at("00:10").do(start)

while True:
    schedule.run_pending()