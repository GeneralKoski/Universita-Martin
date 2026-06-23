import math 
import optparse
import time
import socket

host=  socket.gethostname()

parser = optparse.OptionParser()
parser.add_option('-i', '--intervals', dest="Intervals", default=100000000, help="numero intervalli" )
options, remainder = parser.parse_args()

Intervals=int(options.Intervals);

PI = 3.14159265358979323846264338327950288 

h = 1.0 / Intervals;

def f1():
   lsum = 0.0
   first=1
   last=Intervals+1
#   print (f' {Intervals} {last}-{first}')
   for i in range(first, last):
       x = h * (i - 0.5)
       lsum += math.sqrt(1 - x*x)
   return (lsum)

def f2():
   lsum = 0.0
   first=1
   last=Intervals+1
#   print (f' {Intervals} {last}-{first}')
   for i in range(first, last):
       x = h * (i - 0.5)
       lsum += 1/(1+x*x)
   return (lsum)

# entry point
if __name__ == '__main__':

    Ta = time.time()
    result1=f1()
    Tb = time.time()
    result2=f2()
    Tc = time.time()

    pi1= 4*h*result1
    pi2= 4*h*result2

    print (f'PY, {Intervals}, {abs(PI-pi1)}, {abs(PI-pi2)}, {round((Tc-Ta),2) },  {round((Tb-Ta),2) },  {round((Tc-Tb),2) }, {host} ')
