from math import factorial
import numpy as np

         #Givens
C_I=13.25
TnoOfChannels = 125
offeredLoad_Sec =0
citySize = 450#km2
populationDensity = 200 #count of users per km2
lamda = 10/(24*60) #The number of calls an average user makes in this city/day
E = 1    #The average call duration for users in the city/min
Tusers = populationDensity*citySize
aUser = lamda *E #offerd load/user

reuseFactor = [3,4,7]
n = [[1,3,3,6],[1,2,4,6],[1,2,3,6]] #number of interfering cells

N = []
x = 0

# 3N/n > C/I
for i in reuseFactor :
    
    j = n[x]
    
    a = (3*i)/j[0]
    b = (3*i)/j[1]
    c =(3*i)/j[2]
    d = (3*i)/j[3]
    
    x = x + 1
    if ( a > C_I ):
        N.append([i,36])
    if ( b > C_I):
        N.append([i,3])
    if ( c > C_I):
        N.append([i,2])
    if ( d > C_I):
        N.append([i,1])    


x = 999999
reuse = 0
sector = 0

#get minimum (N*number of sectors) to maximize number of trunks

for i in N :
    
    temp = i[0]*i[1]
    
    if (temp <= x):
        x = temp
        
        reuse = i[0]
        sector = i[1]

noOfTrunks_Cell= (8/2)*(TnoOfChannels/reuse)
print("noOfTrunks_Cell: ",noOfTrunks_Cell)
noOfTrunks_Sec = int(np.floor(noOfTrunks_Cell/sector))
print("noOfTrunks_Sec: ",noOfTrunks_Sec)



pb=0.001#threshold
BlockingProbability=0
#returnes probability of blocking
def erlang(offered_load, number_of_trunks):
            
        L = (offered_load ** number_of_trunks) / factorial(number_of_trunks)
        sum_ = 0
        for n in range(number_of_trunks + 1): sum_ += (offered_load ** n) / factorial(n)
    
        #print("BlockingProbability: ",L / sum_)       
        return (L / sum_)
while BlockingProbability<=pb:
    BlockingProbability = erlang(offeredLoad_Sec,noOfTrunks_Sec)    
    offeredLoad_Sec =offeredLoad_Sec+0.001
print("BlockingProbability: ",BlockingProbability)   
print("offeredLoad_Sec: ",offeredLoad_Sec) 

offeredLoad_Cell = erlang(offeredLoad_Sec,noOfTrunks_Sec)*sector
print(offeredLoad_Cell)
print(aUser)
noOfUsers_Cell = int(offeredLoad_Cell/aUser)     #𝒔𝒖𝒃𝒔𝒄𝒓𝒊𝒃𝒆𝒓𝒔/𝒄𝒆ll
noOfCells = int(np.ceil(Tusers/noOfUsers_Cell)) #total number of cells/city
print("total number of cells/city", noOfCells)