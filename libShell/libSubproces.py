import subprocess

# a = subprocess.run(["dir", '.'])
a1 = subprocess.Popen(["ipconfig"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
a2 = subprocess.run(["ipconfig"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

pass
