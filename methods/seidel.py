import time
import math

def SFCalc(number, significantFigures):
    if number == 0:
        return 0

    # Calculate the order of magnitude of the number
    order_of_magnitude = math.floor(math.log10(abs(number)))
    
    # Scale the number to the desired significant figures
    scale = 10**(significantFigures - 1 - order_of_magnitude)
    scaled_number = math.trunc(number * scale)
    
    # Scale back to the original magnitude
    result = scaled_number / scale
    return result


class Seidel:
    
    def __init__(self, matrixA, matrixB, initial_guess, Figures):
        self.matrixA = matrixA
        self.matrixB = matrixB
        self.new =initial_guess
        self.initial_guess = initial_guess
        self.SignificantFigures = Figures
        self.iteration=0
        self.time=0
        self.res=[]
        self.steps=""

    def getSolution (self):
        return self.res
    
    def getIterations(self):
        return self.iteration

    def getExcutionTime(self):
        return self.time
    
    def getSteps(self):
        return self.steps

    def writeSolution(self, matrix, signifcantFigure):
        self.steps += "\n"


    def solve_with_iterations(self, num_iterations):
        
        self.steps += f"Given intial guess of solution as {self.initial_guess}"
        self.steps += "\n"
        startTime=time.perf_counter_ns()
        for t in range(num_iterations):
            self.steps += "\n"
            self.steps += f"    iteration # {t+1}"
            self.steps += "\n"
            for i in range(len(self.matrixB)):
                sum = self.matrixB[i]
                self.steps += f"        X{i+1} = ( {self.matrixB[i]} "
                for j in range(len(self.matrixB)):
                    if i != j:
                        sum -= SFCalc(float(self.matrixA[i][j] )* float(self.new[j]), self.SignificantFigures)
                        self.steps += f"+ {-1*self.matrixA[i][j]} ({self.new[j]}) "
                self.new[i] = SFCalc(sum / self.matrixA[i][i], self.SignificantFigures)
                self.steps += f")/{self.matrixA[i][i]} = {self.new[i]}\n"
            self.steps+="\n"
            
            self.old = self.new[:]
            
            self.steps+=f"      Solution after #{t+1} iteration is {self.old}"
            self.steps+="\n\n"
        endTime=time.perf_counter_ns()
        self.time=endTime - startTime
        self.res=self.new

    def solve_with_tolerance(self, tolerance):
        startTime = time.perf_counter_ns()
        old = self.new[:] 
        tolerance /= 100
        valid = False
        iteration = 0
        self.steps += f"Given intial guess of solution as {self.initial_guess}"
        self.steps += "\n\n"

        while not valid and iteration<200:
            valid = True
            iteration += 1
            self.steps += "\n" 
            self.steps += f"    iteration # {iteration}"
            self.steps += "\n"

            for i in range(len(self.matrixB)):
                sum = self.matrixB[i]

                self.steps += f"        X{i+1} = ( {self.matrixB[i]} "
                for j in range(len(self.matrixB)):
                    if i != j:
                        sum -= SFCalc(float(self.matrixA[i][j]) * float(self.new[j]), self.SignificantFigures)
                        if iteration<=10:
                            self.steps += f"+ {-1*self.matrixA[i][j]} ({self.new[j]}) "
                self.new[i] = SFCalc(sum / self.matrixA[i][i], self.SignificantFigures)
            
                self.steps += f")/{self.matrixA[i][i]} = {self.new[i]}"
                self.steps+="\n"
                if(self.new[i]==0):
                  relative_error=old[i]
                    
                else:
                    relative_error = abs(float(self.new[i]) - float(old[i])) / abs(self.new[i])

                self.steps+=f"        #Relative error of X{i+1} after {iteration} iteration = |{self.new[i]} - {old[i]} / {abs(self.new[i])}| ={SFCalc(relative_error,self.SignificantFigures)}"
                self.steps+="\n"
                if relative_error > tolerance:
                    valid = False

            self.steps+=f"      Solution after #{iteration} iteration is {self.new}"
            self.steps+="\n\n"
            old = self.new[:]

        endTime = time.perf_counter_ns()
        self.time = endTime - startTime
        self.res = self.new[:]
        self.iteration = iteration


