#Proj2Driver.py
#Test Driver for COSC 251 Project 2
#Spring 2014
#Last Revision - 2/21/2014
#Alan C. Jamieson

#To run, make sure that your Proj2.py file is in the
#same directory as this file.
#Open this file in IDLE and Run Module (F5)

import Proj2

#Problem 1 - user input based
Proj2.Problem1()

#Problem 2
#Expected output
#26
#1
Proj2.Problem2("z a")

#0
Proj2.Problem2("cat")

#83681
Proj2.Problem2("vwxyz")

#0
#18608
#9049
#2944
#307
Proj2.Problem2("alan abfgt defi vwz qr")

#Problem 3
#Expected output
#6H2O+6CO2=6O2+C6H12O6 balances
Proj2.Problem3("6H2O+6CO2=6O2+C6H12O6")

#2Na+2H2O=2NaOH+H2 balances
#C6H12O6=3C2H2+3O2 does not balance
Proj2.Problem3("2Na+2H2O=2NaOH+H2 C6H12O6=3C2H2+3O2")

#2O+3Ag2He=2HeO+3Ag2+He balances
#Au4Ar5Tn4=4AuAr+3Tn+He does not balance
#Au+Ag+H+O+Rb=HORbAgAu balances
Proj2.Problem3("2O+3Ag2He=2HeO+3Ag2+He Au4Ar5Tn4=4AuAr+3Tn+He Au+Ag+H+O+Rb=HORbAgAu")

#Problem 4 - user input based
Proj2.Problem4()
