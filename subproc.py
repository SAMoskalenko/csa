import subprocess

for i in range(int(input('введите количество клиентов: '))):
    subprocess.Popen(['fab client:r'], shell=True)
c = subprocess.Popen(['fab client:w'], shell=True)
c.communicate()
