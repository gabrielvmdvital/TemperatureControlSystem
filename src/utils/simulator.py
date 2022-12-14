import numpy as np
import repackage
repackage.up()

class Simulator:

    def __init__(self, nEnvironment: int, interval: tuple = (15, 20), matrixA: np.ndarray = None,
                 matrixB: np.ndarray = None, arrayT: np.ndarray = None) -> None:
        """This method is the constructor of the Simulator class

        Args: nEnvironment: Integer value
              matrixA: Environment relationship matrix with float valus
              matrixB: Influence matrix of actuators in the environment
              arrayT: array of temperature in environment

        Return: None
        """
        self.__nEnvironment = nEnvironment
        self.__l, self.__h = interval
        self.__matrixA = self.__generate_matrixA_values() if matrixA is None else np.array(matrixA, dtype=np.float32)
        self.__matrixB = self.__generate_matrixB_values() if matrixB is None else np.array(matrixB, dtype=np.float32)
        self.__arrayT = self.__generate_arrayT_values() if arrayT is None else np.array(arrayT, dtype=np.float32)
        self.__memory = [self.__arrayT]
        

    @property
    def nEnvironment(self) -> int:
        """This method is a property used to return the number of environments        
        Args: None
        Return: number of environments        
        """        
        return self.__nEnvironment

    @property
    def matrixA(self) -> np.ndarray:
        """This method is a property used to return the matrix A       
        Args: None
        Return: Matrix A    
        """
        return self.__matrixA
    
    @property
    def matrixB(self) -> np.ndarray:
        """This method is a property used to return the matrix B        
        Args: None
        Return: Matrix B        
        """
        return self.__matrixB
  
    @property
    def arrayT(self) -> np.ndarray:
        """This method is a property used to return the array T    
        Args: None
        Return: Array of temperature      
        """
        return self.__arrayT

    @property
    def memory_list(self) -> np.ndarray:
        """This method is a property used to return the array T    
        Args: None
        Return: Array of temperature      
        """
        return self.__memory

    @property
    def high(self):
        """This method is a property used to return a High value of interval random temperature array.    
        Args: None
        Return: High interval value of random temperature array.       
        """
        return self.__h
    
    @property
    def low(self):
        """This method is a property used to return a Low value of interval random temperature array.   
        Args: None
        Return: Low value of interval random temperature array.      
        """
        return self.__l
                
    def __generate_matrixA_values(self) -> np.ndarray:
        """This method is used to initialize matrix A with random values in the range between [0,1]      
        Args: None
        Return: np.ndarray with dimensions (nEnvironment x nEnvironment) which represents the matrix A      
        """
        aux_matrixA_values = np.random.rand(self.__nEnvironment, self.__nEnvironment)
        for i in range(len(aux_matrixA_values)):
            for j in range(len(aux_matrixA_values[i])):
                if i == j:
                    aux_matrixA_values[i][j] = 1
                else:
                     aux_matrixA_values[i][j] =  aux_matrixA_values[i][j]/10

        print("[STATUS] -> Initializing matrix A with random values and unit diagonal")
        #print(aux_matrixA_values)         
        return aux_matrixA_values.astype(np.float32)

    def __generate_matrixB_values(self) -> np.ndarray:
        """This method is used to initialize diagonal matrix B representing the nth interaction 
        between the environment and the actuator.
        Args: None
        Return: diagonal np.ndarray with dimensions (nEnvironment x nEnvironment)      
        """
        print("[STATUS] -> Initializing the diagonal matrix B")
        return np.eye(self.__nEnvironment, dtype=np.float32)
 
    def __generate_arrayT_values(self) -> np.ndarray:
        """This method is used to initialize array T with random values in the range between [15,35].
        Args: None
        Return: np.ndarray with dimensions (nEnvironment) which represents the array of Temperature      
        """
        print(f"[STATUS] -> Initializing the temperature array with random values between {self.__l} and {self.__h}")

        return np.random.randint(low=18, high=22, size=self.__nEnvironment).astype(np.float32)


    def update_arrayT(self, arrayU) -> None:
        """This method is used to update the values of the array of Temperature
        Args: array with the new powers to reach the desired temperature
        Return: array T with updated values      
        """
        print("[STATUS] -> Calculating the new temperature data for the environments")
        temp = np.zeros(self.__nEnvironment, dtype=np.float32)
        for i in range(len(temp)):
            for j in range(len(temp)):
                if i != j:
                    temp[i] += (self.__matrixA[i][j]*(self.__arrayT[j] - self.__arrayT[i])) + self.__matrixB[i][i]*arrayU[i]
                else:
                    temp[i] += self.__matrixB[i][i]*arrayU[i]
            temp[i] = temp[i]

        aux = np.round(self.__arrayT + temp, 2)
        self.update_memory_list(aux)        
        self.__arrayT = aux
        #print(f"arryT atualizado: {aux}")
        print(f"[STATUS] -> New Temperature array: {self.__arrayT}")
        return aux

    def update_memory_list(self, arrayT: np.ndarray) -> None:
        """this method is used to store in memory the array containing the temperature of the environments
        Args: instance of Simulator class
        Return: array T with updated values      
        """
        print("[STATUS] -> Storing the temperature values of the environments")
        self.__memory.append(arrayT)

    def post_temperature_status(self) -> np.ndarray:
        """this method is used to post the sending of temperature information from the 
           control center to the simulator
        Args: instance of ControlCenter class
        Return: array T with updated values      
        """
        print("[STATUS] -> sending the temperature information of the environments")
        return self.__memory[-1]

    def get_arrayU(self, other) -> np.ndarray:
        """this method is used to request the sending of temperature information from the 
           control center to the simulator 
        Args: instance of ControlCenter class
        Return: array T with updated values      
        """
        return other.post_upadate_arrayU()
