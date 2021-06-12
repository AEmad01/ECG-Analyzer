import matplotlib.pyplot as plt
import numpy as np

def getNewEmptyArray(ecg):
  #return new numpy array of zeros with length of ecg
  return np.zeros(len(ecg))

def diff(ecg):
    result = getNewEmptyArray(ecg)
    #slide 20 lec 5 equation with cases for:
    T = 1/512
    for index in range(len(ecg)):
      if index ==0:#first no index - 1 or index - 2
          result[index] = (0.125 * T) * (2 * ecg[index + 1] + ecg[index + 2])
          continue
      if index ==1:#second no index - 2
          result[index] =  (0.125 * T)  * (- 2 * ecg[index - 1] + 2 * ecg[index + 1] + ecg[index + 2])
          continue
      if index == len(ecg)-2:#before last no index+2
          result[index] =  (0.125 * T) * (-ecg[index - 2] - 2 * ecg[index - 1] + 2 * ecg[index + 1])
          continue
      if index == len(ecg)-1:#last no index+1 or index+2
          result[index] = (0.125 * T) * (-ecg[index - 2] - 2 * ecg[index - 1])
          continue
          #base case
      result[index] = (0.125 * T) * (-ecg[index - 2] - 2 * ecg[index - 1] + 2 * ecg[index + 1] + ecg[index + 2])
    return result

def square(ecg):
  #returns the square of each value in the ecg
    result = getNewEmptyArray(ecg)
    for i in range(0,len(ecg)):
        result[i] = ecg[i]*ecg[i]
    return result 
  
def avg(ecg):
  #returns an average window of size 31 on the ecg
    result = getNewEmptyArray(ecg)
    for i in range(0,len(ecg)):
        total=0
        for j in range(0,31):#sum next 31 values
            if(i+j<len(ecg)):#if not out of bounds
                total += ecg[i+j]  #add to total
        result[i] = total/31 #get average 
        i=i+31
    return result

def autoColleration(ecg):
  #autocorrelation equation from the lecture
    result=[]
    for m in range(0,len(ecg)):
        A=0
        for i in range(0,len(ecg)):
          if (i-m)>0:
            A = A + ecg[i] * (ecg[(i-m)])
        result.append(A)
    # for m in range(len(ecg),0,-1):
    #     A=0
    #     for i in range(len(ecg)-1,0,-1):
    #       if (i-m)>0:
    #         A = A + ecg[i] * (ecg[(i-m)])
    #     result.append(A)
    return result

def draw(xAxis,yAxis,count,filename):
  #draw method
  plt.plot(xAxis[0:count],yAxis[0:count])
  plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)

  plt.xlabel("Time (s)")
  plt.ylabel("Amplitude (v)")
  plt.rcParams["figure.figsize"] = [16,9]


  plt.savefig (filename)

def artial_detect(peaks): 
  #detects artial fibrillation through checking the difference between each peak (R Wave). 
  #It checks how regular do the R peaks occur.
  count = 0
  for i in range(len(peaks)-1):
    if abs(peaks[i+1]-peaks[i] - peaks[0]) > 30:
      count+=1
  if (count>1):
    print("Atrial Fibrillation Detected")
    print("Irregular Heart Beats:",count/len(peaks) *100,"%")
  else:
    print("No Atrial Fibrillation Detected")
    print("Irregular Heart Beats:",count/len(peaks) *100,"%")

# def artial_detect2(bpm):
#   if bpm > 100:
#     print("Atrial Fibrillation Detected")
#   else:
#     print("No Atrial Fibrillation Detected")


def getHeartRate(autoc): 
  peaks=[]

  zeroLag = np.amin(autoc[0:512])
  start = np.where(autoc==zeroLag)[0][0]
    
  for i in range (start,len(autoc),512):
    max = np.amax(autoc[i:len(autoc)])
    peaks.append(np.where(autoc == max)[0])
  bpm=(60*512)/peaks[0]
  return bpm,peaks


def main(file):
  #open file
  file = open (file,'r')
  inputfile = file.readlines()
  timeInc=0
  ecg=[]
  time=[]
  i=0
  for item in inputfile:
    item.replace("\n","")
    ecg.append(float(item))
    time.append(timeInc)
    timeInc+=1/512
  
  differenciated = diff(ecg)
  squared = square(differenciated)
  smoothed=avg(squared)
  autoc=autoColleration(smoothed)
  # for t in range (len(time)):
  #   time.append(-1*time[t])

  # time.sort()
  yAxis=autoc
  xAxis=time
  
  bpm,peaks=getHeartRate(autoc)

  artial_detect(peaks)
  #artial_detect2(bpm)

  print("Heart Rate",bpm)

  draw(xAxis,yAxis,len(ecg),"AutoCorr1.jpg")
  

main("Data1.txt")
print()
#main("Data2.txt")
