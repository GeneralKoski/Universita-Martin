import multiprocessing
import math 
import optparse
import time
import socket

host=  socket.gethostname()

parser = optparse.OptionParser()
parser.add_option('-t', '--ntasks',  dest="nt",          default=8    , help="numero di Threads" )
parser.add_option('-i', '--intervals', dest="Intervals", default=10000, help="numero intervalli" )
options, remainder = parser.parse_args()

nt=int(options.nt);
Intervals=int(options.Intervals);

PI = 3.14159265358979323846264338327950288 

h = 1.0 / Intervals;

def f1(tid):
   lsum = 0.0
   size=int(Intervals/nt)
   first=tid*size+1
   last=(tid+1)*size+1
   print (f'#PYM-f1 {tid}/{nt} {Intervals} {first}-{last} ')
   for i in range(first, last):
       x = h * (i - 0.5)
       lsum += math.sqrt(1 - x*x)
   return (lsum)

def f2(tid):
   lsum = 0.0
   size=int(Intervals/nt)
   first=tid*size+1
   last=(tid+1)*size+1
   print (f'#PYM-f2 {tid}/{nt} {Intervals} {first}-{last} ')
   for i in range(first, last):
       x = h * (i - 0.5)
       lsum += 1/(1+x*x)
   return (lsum)
 
# entry point
if __name__ == '__main__':

    Ta = time.time()
    mp = multiprocessing.Pool(nt)
    result1=mp.map(f1, range(nt))
    Tb = time.time()
    mp = multiprocessing.Pool(nt)
    result2=mp.map(f2, range(nt))
    Tc = time.time()

    pi1= 4*h*sum(result1)
    pi2= 4*h*sum(result2)
		   
    print (f'PYM, {nt}, {Intervals},   {round((Tc-Ta),2) }, {round((Tb-Ta),2)}, {round((Tc-Tb),2)},  {abs(PI-pi1)}, {abs(PI-pi2)}, {host} ')
