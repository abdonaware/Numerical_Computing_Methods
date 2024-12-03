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


class Jacobi:
    def __init__(self, matrixA, matrixB, initial_guess, Figures):
        self.matrixA = matrixA
        self.matrixB = matrixB
        self.old = initial_guess
        self.new = [0] * len(initial_guess)
        self.SignificantFigures = Figures
        self.res = []
        self.time = 0.0
        self.iterations = 0
        self.steps = "" 

    def getSolution(self):
        return self.res

    def getExecutionTime(self):
        return self.time

    def getIterations(self):
        return self.iterations

    def getSteps(self):
        return self.steps

    def solve_with_iterations(self, num_iterations):
        self.steps += f"Given initial guess of solution as {self.old}\n\n\n"
        start_time = time.perf_counter_ns()
        for t in range(num_iterations):
            self.steps += f"    Iteration # {t + 1}\n"
            for i in range(len(self.matrixB)):
                self.new[i] = self.matrixB[i]
                self.steps += f"        X{i+1} = ({self.matrixB[i]} "
                for j in range(len(self.matrixB)):
                    if i != j:
                        self.new[i] -= SFCalc(float(self.matrixA[i][j]) * float(self.old[j]), self.SignificantFigures)
                        self.steps += f"+ {-1 * self.matrixA[i][j]}({self.old[j]}) "
                self.new[i] /= SFCalc(self.matrixA[i][i], self.SignificantFigures)
                self.steps += f")/{self.matrixA[i][i]} = {SFCalc(self.new[i], self.SignificantFigures)}\n"
            self.old = self.new[:]
            self.new = [SFCalc(num, self.SignificantFigures) for num in self.new]
            self.steps += f"      Solution after iteration #{t + 1}: {self.new}\n\n"
        end_time = time.perf_counter_ns()
        self.time = end_time - start_time
        self.res = self.new

    def solve_with_tolerance(self, tolerance):
        valid = False
        iteration = 0
        self.steps += f"Given initial guess of solution as {self.old}\n\n"
        start_time = time.perf_counter_ns()
        while not valid:
            valid = True
            iteration += 1
            self.steps += f"    Iteration # {iteration}\n"
            for i in range(len(self.matrixB)):
                self.new[i] = self.matrixB[i]
                self.steps += f"        X{i+1} = ({self.matrixB[i]} "
                for j in range(len(self.matrixB)):
                    if i != j:
                        self.new[i] -= SFCalc(float(self.matrixA[i][j]) * float(self.old[j]), self.SignificantFigures)
                        self.steps += f"+ {-1 * self.matrixA[i][j]}({self.old[j]}) "
                self.new[i] /= SFCalc(self.matrixA[i][i], self.SignificantFigures)
                if(self.new[i]==0):
                  relative_error=self.old[i]
                    
                else:
                     relative_error = abs(float(self.new[i]) - float(old[i])) / abs(self.new[i])
                self.steps += f")/{self.matrixA[i][i]} = {SFCalc(self.new[i], self.SignificantFigures)}\n"
                self.steps += f"           # Relative error for X{i+1} = {SFCalc(relative_error,self.SignificantFigures)}\n"
                if relative_error > tolerance:
                    valid = False
            self.old = self.new[:]
            self.new = [SFCalc(num, self.SignificantFigures) for num in self.new]
            self.steps += f"      Solution after iteration #{iteration}: {self.new}\n\n"
        end_time = time.perf_counter_ns()
        self.time = end_time - start_time
        self.res = self.new
        self.iterations = iteration
