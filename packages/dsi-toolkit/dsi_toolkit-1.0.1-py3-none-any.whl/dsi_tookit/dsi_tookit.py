"""
 The "dsi_toolkit" contains the function package for System Identification
 of polynomial models, with the purpose of carrying out all stages of system
 identification. This includes generating candidate terms for the model,
 selecting and detecting structures, estimating parameters, visually and
 statistically validating the identified model, as well as generating its
 characteristic static curve. This package also serves as a preliminary step
 to the "Parameter Estimation with Constraints" and "Bi-objective Estimation"
 Package, using knowledge of the identified model's static curve.

 The methods included in this class are:

 1 - generateCandidateTerms: generates the candidate terms for the model;
 2 - getInfo: obtains the necessary information from the model;
 3 - detectStructure: detects the model's structure;
 4 - buildRegressorMatrix: constructs the regressors' matrix;
 5 - rmse: calculates the RMSE error;
 6 - delay: produces a delayed signal in discrete time;
 7 - combinationWithRepetition: calculates the combination of terms, with repetition;
 8 - removeClusters: removes inappropriate term groupings;
 9 - validateModel: validates the model;
 10 - correlationFunction: calculates and graphically displays the correlation function;
 11 - correlationCoefficient: calculates the correlation coefficient;
 12 - buildStaticResponse: generates the model's static response;
 13 - groupcoef: calculates the grouping coefficients of terms;
 14 - buildMapping: Mapping matrix between dynamic parameters and term grouping coefficients.
 15 - estimateParametersELS: estimates the model's parameters by Least Squares
 16 - estimateParametersRELS: estimates the model1s parameters by Restrict Least Squares
 17 - displayModel: presents the model in textual format and on a panel;
 18 - displayStaticModel: presents the static model in textual format and on a panel.
 19 - checkSubarrayForGNLY: detects the degree of nonlinearity of the clusters in y.

 Note: For more information on how to use this function, follow this procedure:

 help("function_name")

 Example:

 help("getInfo")

 To showcase the dsitools usage, run the examples contained in the
 PACKAGE: exempleELS.m (1) and exempleRELS.m (2)

 (1) - Using the Extended Least Squares Estimator;
 (2) - Using the Restricted Extended Least Squares Estimator.

 System Identification Package version 1.1
 Electrical Engineering Department - DEPEL
 Federal University of São João del-Rei - UFSJ
 Prof. Dr. Márcio Falcão Santos Barroso - UFSJ
 Prof. Dr. Eduardo Mazoni Andrade Marçal Mendes - UFMG
 MEE Jim Jones da Silveira Marciano
 First semester of 2025.
"""

from inspect import signature
from numpy import (array, prod, sort, max, vstack, any, zeros_like, round, 
                   ones, mean, dot, sqrt, ndarray, floor, sum, std, zeros,
                   roll, unique, hstack, newaxis, where, asarray, all, 
                   log, argmin, array_equal, mod, var, size)
from numpy.linalg import pinv, inv
from itertools import combinations_with_replacement
from matplotlib.pyplot import (figure, plot, axhline, title, xlabel, text,
                             ylabel, legend, grid, box, show, subplots, axis)

#=====================================================================================================
def generateCandidateTerms(nonlinearityDegree, delays):
    """
    The function [model, Tterms] = generateCandidateTerms(nonlinearityDegree, delays) is part of the
    System Identification Package for polynomial models. Its purpose is to
    generate candidate terms for process and noise with a degree of nonlinearity
    and maximum delays provided by the user. The output is the combination of all
    terms as a function of delays and nonlinearity degree, as follows:

    Inputs:
        nonlinearityDegree ==> degree of nonlinearity: if equal to zero, it indicates
                                that the model is linear, and its static representation
                                is of the type Y = AX; if the value is greater than or equal
                                to 1, it indicates that the model is nonlinear and its static
                                representation is of the type Y^nonlinearityDegree = AX^nonlinearityDegree + BX^(nonlinearityDegree-1) + ... M,
                                where M is a constant.

        delays ==> a vector of dimension between 1 and 3 containing the maximum
                   delays for input, output, and noise. If the vector has a
                   dimension of 1, it indicates that the model is of type AR,
                   linear or nonlinear depending on nonlinearityDegree; if the vector has a
                   dimension of 2, it indicates that the model is ARX, linear or
                   nonlinear depending on nonlinearityDegree; if the vector has a dimension of
                   3, it indicates that the model is ARMAX, linear or nonlinear
                   depending on the degree of nonlinearity.

    Outputs:
        model ==> a coded representation of the structure containing
                  candidate terms where the number of columns corresponds
                  to the degree of nonlinearity. The regressors are coded as:
                  y(k-i) = 100i --> output terms
                  u(k-j) = 200j --> input terms
                  e(k-l) = 300l --> noise terms
                  The model will be the combination of all possible terms.
        type ==> reveals the representation type, i.e., (AR, ARX, ARMAX,
                 NAR, NARX, NARMAX, polynomial).
    """
    #Verify the dimensions of the inputs and outputs of the function
    nargin = signature(generateCandidateTerms).parameters
    if len(nargin) != 2:
        raise ValueError("The function requires 2 inputs")
    #Check if the nonlinearityDegree is a positive integer
    test = nonlinearityDegree % 1
    if test != 0 or nonlinearityDegree < 0 :
        raise("The degree of nonlinearity must be a positive integer")
    #Check if the delays vector is not empty. Delays must have
    #a dimension greater than or equal to 1 and less than 4.    
    # Check if the 'delays' list is empty
    if not delays:  # Checks if 'delays' is empty
        raise ValueError("The 'delays' variable must have a dimension greater than or equal to 1")
    delays = array(delays)
    #--------------------------------------------------------------------------
    #Test if the values inside the delays vector are positive integers and if 
    #the dimension is less than or equal to 3
    #--------------------------------------------------------------------------
    # Tests
    test2 = prod(delays % 1)  # Test if all elements are integers
    test3 = prod(delays)      # Test if the product of delays is positive
    test4 = test3 % 1            # Test if the product is an integer
    # Check conditions
    if test2 != 0 or test3 <= 0 or test4 != 0 or delays.ndim > 1 or len(delays) > 3:
        raise ValueError("Delays must be positive integers and the dimension must be less than or equal to 3")
    # --------------------------------------------------------------------------
    # Build the candidate terms matrix.
    # Case 1 - build an AR model
    # --------------------------------------------------------------------------
    if len(delays) == 1 and nonlinearityDegree == 0:
        lagy = delays[0]
        linear = [[i] for i in range(1001, 1000 + lagy + 1)]
        model = linear
        typmodel = 'Polynomial AR'
    
    # --------------------------------------------------------------------------
    # Case 2 - build an ARX model
    # --------------------------------------------------------------------------
    elif len(delays) == 2 and nonlinearityDegree == 0:
        lagy = delays[0]
        lagu = delays[1]
        linear = [[i] for i in range(1001, 1000 + lagy + 1)] + \
                 [[i] for i in range(2000, 2000 + lagu + 1)]
        model = linear
        typmodel = 'Polynomial ARX'
    
    # --------------------------------------------------------------------------
    # Case 3 - build an ARMAX model
    # --------------------------------------------------------------------------
    elif len(delays) == 3 and nonlinearityDegree == 0:
        lagy = delays[0]
        lagu = delays[1]
        lage = delays[2]
        linear = [[i] for i in range(1001, 1000 + lagy + 1)] + \
                 [[i] for i in range(2000, 2000 + lagu + 1)] + \
                 [[i] for i in range(3001, 3000 + lage + 1)]
        model = linear
        typmodel = 'Polynomial ARMAX'
    
    # --------------------------------------------------------------------------
    # Case 4 - build a NAR model
    # --------------------------------------------------------------------------
    elif len(delays) == 1 and nonlinearityDegree != 0:
        lagy = delays[0]
        linear = [[0]] + [[i] for i in range(1001, 1000 + lagy + 1)]
        model = combinationWithRepetition(linear, nonlinearityDegree)
        typmodel = 'Polynomial NAR'
    
    # --------------------------------------------------------------------------
    # Case 5 - build a NARX model
    # --------------------------------------------------------------------------
    elif len(delays) == 2 and nonlinearityDegree != 0:
        lagy = delays[0]
        lagu = delays[1]
        linear = [[0]] + [[i] for i in range(1001, 1000 + lagy + 1)] + \
                 [[i] for i in range(2001, 2000 + lagu + 1)]
        model = combinationWithRepetition(linear, nonlinearityDegree)
        typmodel = 'Polynomial NARX'
    
    # --------------------------------------------------------------------------
    # Case 6 - build a NARMAX model
    # --------------------------------------------------------------------------
    elif len(delays) == 3 and nonlinearityDegree != 0:
        lagy = delays[0]
        lagu = delays[1]
        lage = delays[2]
        linear = [[0]] + [[i] for i in range(1001, 1000 + lagy + 1)] + \
                 [[i] for i in range(2001, 2000 + lagu + 1)] + \
                 [[i] for i in range(3001, 3000 + lage + 1)]
        model = combinationWithRepetition(linear, nonlinearityDegree)
        typmodel = 'Polynomial NARMAX'
    
    # --------------------------------------------------------------------------
    # Check if the dimension of the delays vector is compatible with the number of
    # required inputs
    # --------------------------------------------------------------------------
    elif len(delays) > 3:
        raise ValueError('The delays variable has a maximum dimension of 3')

   
    # Reorder rows such that 0 always appears last in the row
    model = array([
        sort(row)[::-1] if 0 in row else row for row in model
    ])  


    # --------------------------------------------------------------------------
    # Calculate the number of terms in the model
    # --------------------------------------------------------------------------
    Tterms = len(model)
    # --------------------------------------------------------------------------
    
    return model, Tterms, typmodel
#=====================================================================================================

#=====================================================================================================
def getInfo(model):
    """
    The function getInfo(model) is part of the System Identification Package for polynomial models. Its
    purpose is to retrieve relevant information in the system identification process, such as Process terms, Noise terms, maximum delays, etc., as follows:

    Input:
          model ==> coded representation of the structure containing candidate
                    terms where the number of columns corresponds to the degree
                    of nonlinearity. The regressors are coded as follows:
                    y(k-i) = 100i --> output terms
                    u(k-j) = 200j --> input terms
                    e(k-l) = 300l --> noise terms

    Outputs:
          numProcessTerms ==> number of process terms
          numNoiseTerms ==> number of noise terms
          maxDelay ==> maximum delay present in the model
          maxOutputDelay ==> maximum delay of output terms
          maxInputDelay ==> maximum delay of input terms
          maxNoiseDelay ==> maximum delay of noise terms
      processModel ==> Model containing only Process terms
      noiseModel ==> Model containing only Noise terms
      model ==> Model containing Process terms followed by Noise terms

    """

    # Verify the input of the function
    if model is None:
        raise ValueError("The function requires one input only")

    # Get only the process model:
    #Ip = model[:, 0] <= 3000
    #processModel = model[Ip, :]
    #numProcessTerms = len(processModel)
    
    Ip = ~any((model >= 3000), axis=1)
    processModel = model[Ip]
    numProcessTerms = len(processModel)

    # Get only the noise model:
    #Ir = model[:, 0] >= 3000
    Ir = any((model >= 3000), axis=1)
    if not any(Ir):
        noiseModel = None
        numNoiseTerms = 0
    else:
        noiseModel = model[Ir]
        numNoiseTerms = len(noiseModel)

    # Get models in y
    Jy = (model > 0) & (model < 2000)
    maxOutputDelay = max(model[Jy] - 1000)

    # Get models in u
    Ju = (model >= 2000) & (model < 3000)
    maxInputDelay = max(model[Ju] - 2000)

    # Get models in e
    Je = model > 3000
    if not any(Je):
        maxNoiseDelay = 0
    else:
        maxNoiseDelay = max(model[Je] - 3000)

    # Get the maximum delay
    maxDelay = max([maxOutputDelay, maxInputDelay, maxNoiseDelay])

    # Model with process terms first and noise terms after
    if not any(Ir):
        model = processModel
    else:
        model = vstack((processModel, noiseModel))

    return numProcessTerms, numNoiseTerms, maxDelay, maxOutputDelay, maxInputDelay, maxNoiseDelay, processModel, noiseModel, model
#=====================================================================================================

#=====================================================================================================
def detectStructure(model, ui, yi, numProcessTerms, numNoiseTerms, err, aic):
    """
    The function [model, processModel, noiseModel, ERR, ERRp, ERRr] = detectStructure(model, ui, yi, numProcessTerms, numNoiseTerms, err, aic)
    is part of the System Identification Package for polynomial models. Its purpose
    is to detect the candidate structure that best explains the output data, as follows:

    Input:
        model ==> coded representation of the structure containing candidate
                  terms where the number of columns corresponds to the degree
                  of nonlinearity, and the rows represent the regressors, coded as:
                                           y(k-i) = 100i --> output terms
                                           u(k-j) = 200j --> input terms
                                           e(k-l) = 300l --> noise terms
           ui ==> input identification vector to be used for parameter estimation
                 of the coded structure
           yi ==> output identification vector to be used for parameter estimation
                 of the coded structure
           numProcessTerms ==> number of process terms to be considered
           numNoiseTerms ==> number of noise terms to be considered
          err ==> enables the technique of sorting candidate regressors based on
                 the Error Reduction Rate, using the RMSE value of each candidate
                 term as the error (i.e., the contribution of each term in explaining
                 the output data).
                 If err = 1, enabled;
                 If err = 0, disabled;
          aic ==> enables verification of the number of terms using the Akaike Criterion,
                 which determines a parsimonious relationship between the number of
                 process terms and the RMSE error incurred when trying to explain the output data.
                 If aic = 1, enabled;
                 If aic = 0, disabled;

    Note: If err or aic are not enabled, numProcessTerms and numNoiseTerms will be used. Otherwise,
    structure detection will be performed automatically based on ERR and AIC
    criteria. If numProcessTerms or numNoiseTerms are inadequate, for example, having values greater than
    the total number of candidate terms, numProcessTerms and numNoiseTerms will default to the total number
    of process and noise terms, respectively.

    Output:
        model ==> Model with detected structure containing both process and
                  noise terms
        processModel ==> Model with detected structure containing only process terms
        noiseModel ==> Model with detected structure containing only noise terms
        ERR ==> Error Reduction Rate of the model
        ERRp ==> Error Reduction Rate of the processModel
        ERRr ==> Error Reduction Rate of the noiseModel
    """
    
    #Verify the dimensions of the inputs and outputs of the function
    #---------------------------------------------------------------------------
    if numProcessTerms is None:
        raise ValueError('numProcessTerms cannot be empty')
    
    if numNoiseTerms is None:
        raise ValueError('numNoiseTerms cannot be empty')
    
    if not isinstance(numProcessTerms, int) or numProcessTerms < 0:
        raise ValueError('numProcessTerms must be a positive integer')
    #--------------------------------------------------------------------------
    
    if not isinstance(numNoiseTerms, int) or numNoiseTerms < 0:
        raise ValueError('numNoiseTerms must be a positive integer')
    #--------------------------------------------------------------------------

    
    #--------------------------------------------------------------------------
    #Verify information about the model to make decisions
    #-------------------------------------------------------------------------
    numProcess, numNoise, maxDelay, maxOutputDelay, maxInputDelay, maxNoiseDelay, processModel, noiseModel, Model = getInfo(model)
    
    if numProcessTerms > numProcess:
        numProcessTerms =  numProcess
    if numNoiseTerms > numNoise:
        numNoiseTerms = numNoise
    
    #--------------------------------------------------------------------------
    #Calculate ERR
    #--------------------------------------------------------------------------
    if err == 1:
        # Obter informações iniciais
        nP, _, _, _, _, _, processModel, _, model = getInfo(model)
    
        # Construir matriz de regressores para o modelo de processo
        Pp = buildRegressorMatrix(processModel, ui, yi)
        y = Pp @ pinv(Pp) @ yi
        e = yi - y
    
        # Construir matriz de regressores para o modelo completo com erro
        P = buildRegressorMatrix(model, ui, yi, e)
        Pr = P[:, nP:]
    
        # Parâmetros do modelo de processo e ruído
        ParametersP = pinv(Pp) @ yi
        ParametersR = pinv(Pr) @ yi
        
        if len(ParametersR) != 0:
                    # Erros normalizados
            ERRp = zeros((len(ParametersP), 1))
            ERRr = zeros((len(ParametersR), 1))
        
            for i in range(len(ParametersP)):
                ERRp[i, 0] = (ParametersP[i]**2 * (Pp[:, i].T @ Pp[:, i])) / (yi.T @ yi)
        
            for i in range(len(ParametersR)):
                ERRr[i, 0] = (ParametersR[i]**2 * (Pr[:, i].T @ Pr[:, i])) / (yi.T @ yi)
        
            # Ordenar erros do modelo de processo
            ERRp, I = zip(*sorted(zip(ERRp.flatten(), range(len(ERRp))), reverse=True))
            ERRp = array(ERRp).reshape(-1, 1)
            processModel = processModel[I, :]
        
            # Ordenar erros do modelo de ruído
            ERRr, J = zip(*sorted(zip(ERRr.flatten(), range(len(ERRr))), reverse=True))
            ERRr = array(ERRr).reshape(-1, 1)
            noiseModel = noiseModel[J, :]
        
            # Atualizar o modelo completo
            model = vstack((processModel, noiseModel))
            ERR = vstack((ERRp, ERRr))
        elif len(ParametersR) == 0:
            ERRp = zeros((len(ParametersP), 1))
        
            for i in range(len(ParametersP)):
                ERRp[i, 0] = (ParametersP[i]**2 * (Pp[:, i].T @ Pp[:, i])) / (yi.T @ yi)
        
            # Ordenar erros do modelo de processo
            ERRp, I = zip(*sorted(zip(ERRp.flatten(), range(len(ERRp))), reverse=True))
            ERRp = array(ERRp).reshape(-1, 1)
            processModel = processModel[I, :]
        
            noiseModel = None
        
            # Atualizar o modelo completo
            model = vstack(processModel)
            ERR = vstack(ERRp)
            ERRr = None
            
    else:
        ERR = None
        ERRr = None
        ERRp = None
            
    #--------------------------------------------------------------------------
    #Calculate AIC
    #--------------------------------------------------------------------------
    if aic == 1:
        P = buildRegressorMatrix(processModel, ui, yi)
        Par = pinv(P) @ yi
        N = len(ui)
        f = zeros(len(Par))
        for i in range(len(Par)):
            linha = P[:,:i+1] 
            yhat = linha @ Par[:i+1]
            r = var(yi-yhat)
            f[i] = N * log(r) + 2*(i+1)        
        # Passo 5: Encontrar o índice de f que tem o valor mínimo
        mint = argmin(f)+1
    else:
        mint = numProcessTerms
    #--------------------------------------------------------------------------
    #Build the matrices and vectors of ERR and Models
    #--------------------------------------------------------------------------

    processModel = array(processModel[:mint])
    nP, nR, _, _, _, _, _, _, model = getInfo(model)
    if nR !=0:
        noiseModel = array(noiseModel[:numNoiseTerms])
        model = array(vstack((processModel, noiseModel)))
    elif nR == 0:
        noiseModel = None
        model = processModel
    
    return model, processModel, noiseModel, ERR, ERRp, ERRr, mint
#=====================================================================================================    

#=====================================================================================================
def buildRegressorMatrix(model, ui, yi, errorData=None):
    """
    The function buildRegressorMatrix(model, ui, yi, errorData) is part of the System
    Identification Package for polynomial models. Its purpose is to construct
    the regressors' matrix of candidate terms, as follows:
    
    Input:
        model ==> coded representation of the structure containing candidate
                  terms where the number of columns corresponds to the degree
                  of nonlinearity, and the rows represent the regressors, coded as:
                                     y(k-i) = 100i --> output terms
                                     u(k-j) = 200j --> input terms
                                     e(k-l) = 300l --> noise terms
        ui ==> input identification vector to be used for parameter estimation
              of the coded structure
        yi ==> output identification vector to be used for parameter estimation
              of the coded structure
        errorData ==> one-step-ahead estimation error vector to be used for parameter
              estimation of the coded structure, if the use of an ELS estimator
              (Extended Least Squares Estimator) is desired
              
    Output:
        P ==> Regressors Matrix of Process terms, if "errorData" is not provided,
              or Regressors Matrix of both Process and Noise terms, if "errorData"
              is provided.
    """
    # Verify the number of inputs and outputs of the function
    if ui is None or yi is None:
        raise ValueError('The function requires at least 3 input variables')

    # Evaluate if there is a noise model to build the regressors matrix appropriately
    _, numNoiseTerms, _, _, _, _, processModel, _, model = getInfo(model)
    if numNoiseTerms == 0 or errorData is None or len(errorData) == 0:
        errorData = None  # Ensure errorData is None if not provided or empty
        model = processModel
    else:
        lengths = [len(ui), len(yi), len(errorData)]
        if len(set(lengths)) != 1:
            raise ValueError('The input, output, and noise vectors must have the same length')

    # Verify the dimensions of the input and output vectors
    if len(ui) != len(yi):
        raise ValueError('The input and output vectors must have the same length')

    # Adjust dimensions
    ui = array(ui).reshape(-1, 1)
    yi = array(yi).reshape(-1, 1)
    errorData = array(errorData).reshape(-1, 1) if errorData is not None else None

    # Initialize the delay and type matrices
    delayMatrix = zeros_like(model)
    typeMatrix = zeros_like(model)

    # Conditions for updating the matrices
    cond1 = (model > 0) & (model < 2000)
    cond2 = (model >= 2000) & (model < 3000)
    cond3 = (model >= 3000)

    # Update matrices based on conditions
    delayMatrix[cond1] = model[cond1] - 1000
    typeMatrix[cond1] = round(model[cond1] / 1000)
    delayMatrix[cond2] = model[cond2] - 2000
    typeMatrix[cond2] = round(model[cond2] / 1000)
    delayMatrix[cond3] = model[cond3] - 3000
    typeMatrix[cond3] = round(model[cond3] / 1000)

    # Initialize necessary variables
    rows, cols = model.shape
    Paux = ones((len(ui), cols))
    P = ones((len(ui), rows))

    # Build the Process and Noise regressors matrix
    for i in range(rows):
        for j in range(cols):
            if typeMatrix[i, j] == 0:
                Paux[:, j] = ones(len(ui))
            elif typeMatrix[i, j] == 1:
                Paux[:, j] = delay(yi, delayMatrix[i, j]).flatten()
            elif typeMatrix[i, j] == 2:
                Paux[:, j] = delay(ui, delayMatrix[i, j]).flatten()
            elif typeMatrix[i, j] == 3:
                if errorData is not None:  # Ensure errorData is valid before using
                    Paux[:, j] = delay(errorData, delayMatrix[i, j]).flatten()
                else:
                    Paux[:, j] = ones(len(ui))  # Fallback if errorData is not provided
            P[:, i] = prod(Paux, axis=1)

    return P
#=====================================================================================================

#=====================================================================================================
def rmse(x, y):
    """
    The function rmse(x, y) is part of the System Identification Package
    for polynomial models, aimed at calculating the RMSE - Root Mean Square Error, as follows:
    
    Inputs:
                x ==> base vector for the RMSE calculation
                y ==> vector for comparison and RMSE calculation relative to x
    Outputs:
                r ==> RMSE value calculated between x and y

    """

    # Ajustar as dimensões das variáveis de entrada
    # --------------------------------------------------------------------------
    if len(x.shape) > 1 and x.shape[1] > x.shape[0]:
        x = x.T
    if len(y.shape) > 1 and y.shape[1] > y.shape[0]:
        y = y.T
    
    if x.shape != y.shape:
        raise ValueError('The vectors must have the same dimensions')
    
    # --------------------------------------------------------------------------
    # Definir o erro de ajuste
    # --------------------------------------------------------------------------
    e = (x - y)
    em = (x - mean(y))
    
    # --------------------------------------------------------------------------
    # Definir o erro quadrático
    # --------------------------------------------------------------------------
    errorE = dot(e.T, e)
    errorM = dot(em.T, em)
    
    # --------------------------------------------------------------------------
    # Calcular o valor do RMSE
    # --------------------------------------------------------------------------
    r = (sqrt(errorE)) / (sqrt(errorM))
    
    return r
#=====================================================================================================

#=====================================================================================================
def delay(signal, delay):
    """
    The function delayedsitoolsgnal = delay(signal, delay) is part of the System Identification
    Package for polynomial models. Its purpose is to apply a pure time delay to a signal, as follows:
    
    Inputs:
        signal ==> vector to be shifted in time
        
        delay ==> delay to be applied to the signal
        
    Outputs:
        delayedsitoolsgnal ==> vector shifted by a delay in discrete time
        
    """
    
    # Adjust the input and output characteristics of the delay function
    # --------------------------------------------------------------------------
    if signal is None or delay is None:
        raise ValueError('2 inputs are required: signal and delay')
    # --------------------------------------------------------------------------
    
    # Convert signal to a NumPy array if it is not already
    signal = array(signal).reshape(-1, 1)
    # Verify the dimension of the signal vector. If the number of columns is greater than
    # the number of rows, the vector is transposed.
    # --------------------------------------------------------------------------
    rows, cols = signal.shape if signal.ndim == 2 else (len(signal), 1)
    if cols > rows:
        signal = signal.T
    # --------------------------------------------------------------------------
    
    # Delay the signal vector
    # --------------------------------------------------------------------------
    if delay == len(signal):
        delay = delay - 1
    
    delayedsitoolsgnal = zeros_like(signal)
    if delay != 0:
        delayedsitoolsgnal[delay:] = signal[:-delay]
    else:
        delayedsitoolsgnal = signal
    # --------------------------------------------------------------------------

    return delayedsitoolsgnal
#=====================================================================================================

#=====================================================================================================
def combinationWithRepetition(v, d):
    """
    The function combinationWithRepetition(v, d) is part of the Estimation of Dynamic
    Systems package for discrete polynomial models. It calculates the combination
    of the elements of vector v given the dimension d, as follows:

    Inputs:
        v ==> vector of elements to be combined, with repetition
        d ==> dimension of the combinations

    Outputs:
        combinations ==> combinations where the number of columns is the dimension
                         of the combinations

    """

    # Verify the dimensions of the inputs and outputs of the function
    # --------------------------------------------------------------------------
    if not isinstance(v, (list, ndarray)):
        raise TypeError('The first input must be a list or numpy array')
    if not isinstance(d, int):
        raise TypeError('Dimension must be a positive integer')
    if d <= 0:
        raise ValueError('Dimension must be a positive integer')
    # --------------------------------------------------------------------------

    # Verify the dimension of the vector to be combined
    # --------------------------------------------------------------------------
    v = array(v).flatten()  # Ensure v is a one-dimensional array
    # --------------------------------------------------------------------------

    # Name the dimension
    # --------------------------------------------------------------------------
    k = d
    # --------------------------------------------------------------------------

    # Perform the combination with repetition
    # --------------------------------------------------------------------------
    if k == 1:
        combinations = v[:, None]
    else:
        combinations = array(list(combinations_with_replacement(v, k)))
    # --------------------------------------------------------------------------

    return combinations
#=====================================================================================================

#=====================================================================================================
def removeClusters(model, cy, cu):
    """
    The function removeClusters(model, cy, cu) is part of the System
    Identification Package for polynomial models. Its purpose is to remove
    clusters from the model as specified by the user, as follows:
    
    Inputs:
        model ==> coded representation of the structure containing candidate
                  terms where the number of columns corresponds to the degree
                  of nonlinearity. The regressors are coded as follows:
                  y(k-i) = 100i --> output terms
                  u(k-j) = 200j --> input terms
                  e(k-l) = 300l --> noise terms
                  The model will include the combination of all possible terms.
                  
        cy    ==> cluster (Grouping of Terms) of output terms to be removed
                  from the candidate model, corresponding to the degree of
                  nonlinearity of the grouping.
        cu    ==> cluster (Grouping of Terms) of input terms to be removed
                  from the candidate model, corresponding to the degree of
                  nonlinearity of the grouping.
                  
    Outputs:
        model ==> new set of candidate terms without the presence of the
                  clusters cy and cu.
                  
    """
    
    # --------------------------------------------------------------------------
    if len([model, cy, cu]) != 3:
        raise ValueError('The function requires 3 inputs')
    
    # --------------------------------------------------------------------------
    # Extract clusters: create a vector with all clusters, the size of the model
    # --------------------------------------------------------------------------
    clusters = floor(model / 1000).astype(int)
    
    # --------------------------------------------------------------------------
    # Candidates to be excluded
    # --------------------------------------------------------------------------
    exclude = (sum(clusters == 1, axis=1) == cy) & (sum(clusters == 2, axis=1) == cu)
    
    # --------------------------------------------------------------------------
    # Filter the model by removing the indicated clusters
    # --------------------------------------------------------------------------
    model = model[~exclude, :]
    
    # --------------------------------------------------------------------------
    # Verify if the term grouping exists
    # --------------------------------------------------------------------------
    if model.size == 0:
        raise ValueError('The indicated grouping does not exist in the model.')
    
    return model
#=====================================================================================================

#=====================================================================================================
def validateModel(model, Parameters, tv, uv, yv, index1, index2, visual1, visual2):
    """
    The function validateModel(model, Parameters, tv, uv, yv, index1, index2, visual1, visual2)
    is part of the System Identification Package for polynomial models. Its
    purpose is to validate the identified model, as follows:
    
    Inputs:
          model ==> coded representation of the structure containing candidate
                    terms where the number of columns corresponds to the degree
                    of nonlinearity. The regressors are coded as follows:
                    y(k-i) = 100i --> output terms
                    u(k-j) = 200j --> input terms
    
      Parameters ==> vector of parameters estimated by the ELS
      tv, uv, yv ==> time (discrete), input, and output validation vectors
         index1 ==> If 1, calculates the correlation coefficient of the
                    validation residuals
         index2 ==> If 1, calculates the RMSE between the simulated output
                    and validation data
         visual1 ==> If 1, displays the simulated output compared to the
                    real data
         visual2 ==> If 1, displays the correlation function of the
                    validation residuals
    
    Outputs:
            yhat ==> simulated output infinite steps ahead (free simulation)
               r ==> correlation coefficient of the validation residuals
               R ==> RMSE index between the simulated output and real data
              ev ==> validation residuals
    
    """

    # Verify the compatibility of the dimensions of the input and output vectors
    uv = asarray(uv).reshape(-1, 1)
    yv = asarray(yv).reshape(-1, 1)
    tv = asarray(tv).reshape(-1, 1)

    # Test the dimension of the parameters
    if not (array_equal(tv.shape, uv.shape) and array_equal(tv.shape, yv.shape)):
        raise ValueError("The time, input, and output vectors must have the same dimension")

    # Test if the values are positive integers
    indicators1 = [visual1, visual2]
    indicators2 = [index1, index2]
    if prod(indicators1) < 0 or prod(indicators2) < 0 or any(mod(indicators1 + indicators2, 1) != 0):
        raise ValueError("The last 4 variables must be positive integers")

    # Get necessary information for the algorithm
    _, _, max_delay, _, _, _, _, _, model = getInfo(model)

    # Generate initial conditions
    rows, cols = model.shape
    l = len(uv)

    yhat = zeros((l, 1))
    yhat[:max_delay] = yv[:max_delay]

    # Build the simulation
    for i in range(max_delay, l):
        signal = zeros(rows)
        for j in range(rows):
            P = ones(cols)
            type = model[j, :] // 1000
            delay = model[j, :] - type * 1000
            k = where(type == 1)[0]
            if k.size > 0:
                for L in k:
                    P[L] *= yhat[i - delay[L]]
            k = where(type == 2)[0]
            if k.size > 0:
                for L in k:
                    P[L] *= uv[i - delay[L]]
            signal[j] = Parameters[j] * prod(P)
        yhat[i] = sum(signal)

    # Calculate the validation residuals
    ev = yv - yhat

    # Calculate the validation indices
    if index1 == 1:
        _, Y = correlationFunction(ev, len(ev) - 1, visual2)
        r = mean(Y)
    else:
        r = None

    if index2 == 1:
        R = rmse(yhat, yv)
    else:
        R = None

    if visual1 == 1:
        figure()
        plot(tv, yv, 'r', label='Validation Output')
        plot(tv, yhat, 'b-.', label='Simulated Output')
        title('Visual Validation - Free Simulation of the Model')
        xlabel('Time [k]')
        ylabel('y[k]')
        legend()
        grid()
        show()

    return yhat, r, R, ev
#=====================================================================================================

#=====================================================================================================
def correlationFunction(signal, delay, flag):
    """
    The function correlationFunction(signal, delay, flag) is part of the System
    Identification Package for polynomial models. Its purpose is to calculate
    the correlation function of a signal, as follows:
    
    Inputs:
        signal ==> vector for which the correlation function will be calculated
        
        delay  ==> maximum signal shift for calculating the correlation function
        
        flag   ==> if flag = 1, the correlation function is plotted
    
    Outputs:
        H      ==> vector of lags used for calculating the correlation function
        Y      ==> correlation vector for the lags in H
    
    """
    
    # Verify the inputs and outputs
    # --------------------------------------------------------------------------
    if signal is None or delay is None or flag is None:
        raise ValueError('The function requires 3 inputs')
    
    # --------------------------------------------------------------------------
    # Verify the dimension of the signal and adjust if necessary
    # --------------------------------------------------------------------------
    if signal.ndim > 1 and signal.shape[1] > signal.shape[0]:
        signal = signal.T
    
    # --------------------------------------------------------------------------
    # Calculate the correlation and store in vectors, for each of the delays
    # --------------------------------------------------------------------------
    H = zeros(delay - 1)
    Y = zeros(delay - 1)
    
    for n in range(1, delay):
        H[n - 1] = n - 1
        r = dot(signal.T, roll(signal, n - 1, axis=0))
        Y[n - 1] = r
    
    # --------------------------------------------------------------------------
    # Normalize the data between -1 and 1
    # --------------------------------------------------------------------------
    if max(Y) > 1:
        Y = Y / max(Y)
    
    # --------------------------------------------------------------------------
    # Plot the data, if flag is equal to 1
    # --------------------------------------------------------------------------
    if flag == 1:
        figure()
        plot(H, Y)
        axhline(y=0.08, color='red', linestyle='--', label='+0.08 Threshold')
        axhline(y=-0.08, color='red', linestyle='--', label='-0.08 Threshold')
        title('Correlation Function')
        xlabel('Delay')
        ylabel('Correlation')
        legend(['Correlation Function', '+0.08 Threshold', '-0.08 Threshold'])
        grid(True)
        box(True)
        show()
    
    return H, Y
#=====================================================================================================

#=====================================================================================================
def correlationCoefficient(signal1, signal2):
    """
    The function correlationCoefficient(signal1, signal2) is part of the System
    Identification Package for polynomial models. Its purpose is to calculate
    the correlation coefficient between two signals, as follows:
    
    Inputs:
        signal1 ==> vector containing one of the signals for cross-correlation
                    coefficient calculation
        
        signal2 ==> vector containing the other signal for cross-correlation
                    coefficient calculation
    
    Output:
        r       ==> cross-correlation coefficient between the two signals.
    
    """
    
    # Verify the inputs and outputs of the function
    # --------------------------------------------------------------------------
    if signal1 is None or signal2 is None:
        raise ValueError('The function requires two inputs')
    
    # Ensure the signals are in the correct dimensions
    # --------------------------------------------------------------------------
    if signal1.ndim > 1 and signal1.shape[1] > signal1.shape[0]:
        signal1 = signal1.T
    if signal2.ndim > 1 and signal2.shape[1] > signal2.shape[0]:
        signal2 = signal2.T
    
    if signal1.shape[0] != signal2.shape[0]:
        raise ValueError('The signals must have the same dimensions')
    
    # Calculate the correlation
    # --------------------------------------------------------------------------
    num = dot((signal1 - mean(signal1)).T, (signal2 - mean(signal2)))
    den = signal1.shape[0] * std(signal1, ddof=0) * std(signal2, ddof=0)
    r = num / den
    
    return r
#=====================================================================================================

#=====================================================================================================
def buildStaticResponse(staticModel, u, y):
    """
    The function [yest, Pest, EstimatedParameters] = buildStaticResponse(staticModel, ui, yi)
    is part of the System Identification Package for polynomial models. Its purpose
    is to simulate the static model and construct the static regressors' matrix, as follows:
    
    Inputs:
             staticModel ==> matrix containing the grouping of terms and their coefficients,
                            generated by the groupcoef.m function
    
                        u ==> static input
                        y ==> output data
    
    Outputs:
                    yest ==> simulated output for the static model for models where yi has
                            a degree of nonlinearity equal to or greater than 2, with or
                            without cross terms.
    --------------------------------------------------------------------------
    Note: When the degree of nonlinearity of yi is less than or equal to 1,
    including cross terms, use the function
    
    [yest, eqest] = displayStaticModel(staticModel, u, p);
    --------------------------------------------------------------------------
                    Pest ==> static data matrix
    EstimatedParameters ==> vector of static model parameters
    
    """
    
    # Verify the dimension of the input and output of the function
    #--------------------------------------------------------------------------
    if staticModel is None or u is None or y is None:
        raise ValueError('The function requires 3 inputs')
    
    # Verify the compatibility of the dimensions of the input and output vectors
    #--------------------------------------------------------------------------
    ui = array(u)
    yi = array(y)
    if ui.ndim == 1:
        ui = ui[:, newaxis]
    if yi.ndim == 1:
        yi = yi[:, newaxis]
    
    if ui.shape[0] != yi.shape[0]:
        raise ValueError('The vectors must have the same dimension')
    
    # Initialize the variables for building the static matrix
    #--------------------------------------------------------------------------
    rows, cols = staticModel.shape
    value = zeros((ui.shape[0], cols - 1))
    Pest = zeros((ui.shape[0], rows))
    
    # Build the static matrix
    #--------------------------------------------------------------------------
    if cols - 1 == 1:
        linear1 = staticModel[:, :-1] == 0
        # Verify if it is linear or not
        #----------------------------------------------------------------------
        if linear1[0] == 0:
            yest = staticModel[0, -1] * ui / (1 - staticModel[1, -1])
            EstimatedParameters = staticModel[:, -1]
            Pest = hstack((ones(ui.shape), ui))
        else:
            for i in range(rows):
                for j in range(cols - 1):
                    if staticModel[i, j] == 0:
                        value[:, j] = ones(ui.shape[0])
                    elif staticModel[i, j] == 1:
                        value[:, j] = yi[:, 0]
                    elif staticModel[i, j] == 2:
                        value[:, j] = ui[:, 0]
                Pest[:, i] = prod(value, axis=1) * staticModel[i, -1]
            EstimatedParameters = staticModel[:, -1]
            yest = sum(Pest, axis=1)
    else:
        for i in range(rows):
            for j in range(cols - 1):
                if staticModel[i, j] == 0:
                    value[:, j] = ones(ui.shape[0])
                elif staticModel[i, j] == 1:
                    value[:, j] = yi[:, 0]
                elif staticModel[i, j] == 2:
                    value[:, j] = ui[:, 0]
            Pest[:, i] = prod(value, axis=1) * staticModel[i, -1]
        EstimatedParameters = staticModel[:, -1]
        yest = sum(Pest, axis=1)
    
    return yest.reshape(-1,1), Pest, EstimatedParameters.reshape(-1,1)
#=====================================================================================================

#=====================================================================================================
def groupcoef(Model, Parameters):
    """
    The function [clusters, coefficients, staticModel, E] = groupcoef(Model, Parameters)
    is part of the System Identification Package for polynomial models. Its purpose is
    to obtain the clusters (grouping of terms) and their respective grouping coefficients,
    as well as to construct a static model and the mapping matrix between dynamic and
    static parameters, as follows:
    
    Inputs:
         Model ==> coded representation of the structure containing candidate
                   terms where the number of columns corresponds to the degree
                   of nonlinearity. The regressors are coded as follows:
                   y(k-i) = 100i --> output terms
                   u(k-j) = 200j --> input terms
    Parameters ==> vector of process parameters estimated
                   using ELS
    
    Outputs:
        clusters ==> matrix containing the composition of clusters (grouping
                     of terms) present in the dynamic model
    coefficients ==> vector containing the coefficients of the term groupings
                     calculated based on the dynamic model
     staticModel ==> matrix containing the information for assembling the
                     static model, where columns from 1 to end-1 represent the
                     code of the term grouping, such as:
                     0 = constant, 1 = output, 2 = input. The number of columns
                     corresponds to the degree of nonlinearity, as follows (example):
                     [0, 0, c] ==> constant term grouping, with the last column
                                   being the coefficient's value
                     [1, 1, c] ==> cross-term grouping with a degree of
                                   nonlinearity 2, with the last column being the coefficient's value
              E ==> matrix that maps the dynamic parameters to the equivalent
                     grouping coefficients
    """

    # Verify the input dimensions
    if Model is None or Parameters is None:
        raise ValueError("The function requires two inputs.")

    if len(Parameters) != Model.shape[0]:
        raise ValueError("The length of 'Parameters' must match the number of rows in 'Model'.")

    # Extract clusters from the Model
    clusters = floor(Model / 1000).astype(int)

    # Find unique clusters and their positions
    unique_clusters, idx = unique(clusters, axis=0, return_inverse=True)

    # Sum parameters for each unique cluster and calculate their coefficients
    coefficients = zeros(len(unique_clusters))
    for i in range(len(coefficients)):
        coefficients[i] = Parameters[idx == i].sum().reshape(-1, 1)  # Align boolean indexing
    # Create the static model by combining unique clusters and coefficients
    staticModel = hstack((unique_clusters, coefficients[:, newaxis]))

    # Initialize and compute the E mapping matrix
    num_clusters = unique_clusters.shape[0]
    E = zeros((num_clusters, len(Parameters)))
    for i in range(num_clusters):
        E[i, where(idx == i)[0]] = 1  # Ensure proper alignment

    clusters = unique_clusters
    return clusters, coefficients.reshape(-1,1), staticModel, E
#=====================================================================================================

#=====================================================================================================
def buildMapping(Model):
    """
    The function [A] = buildMapping(Model)
    is part of the System Identification Package for polynomial models. Its purpose is
    to obtain the matrix that maps the dynamic parameters to the equivalent
    grouping coefficients, as follows:
    
    Inputs:
           Model ==> coded representation of the structure containing candidate
                     terms where the number of columns corresponds to the degree
                     of nonlinearity. The regressors are coded as follows:
                     y(k-i) = 100i --> output terms
                     u(k-j) = 200j --> input terms
    
    Outputs:
    
               A ==> matrix that maps the dynamic parameters to the equivalent
                     grouping coefficients
    
    """
    
    # Verify the dimensions of the input and output of the function
    #--------------------------------------------------------------------------
    if Model is None:
        raise ValueError('The function requires one input')
    
    #--------------------------------------------------------------------------
    # Extract clusters from the Model
    #--------------------------------------------------------------------------
    clusters = floor(Model / 1000).astype(int)
    
    #--------------------------------------------------------------------------
    # Find unique clusters and their positions
    #--------------------------------------------------------------------------
    unique_clusters, idx = unique(clusters, axis=0, return_inverse=True)
    
    #--------------------------------------------------------------------------
    # Initialize a zero matrix
    #--------------------------------------------------------------------------
    num_clusters = unique_clusters.shape[0]
    A = zeros((num_clusters, Model.shape[0]))
    
    #--------------------------------------------------------------------------
    # Determine the E mapping matrix between static and dynamic parameters
    #--------------------------------------------------------------------------
    for i in range(num_clusters):
        rows = idx == i
        A[i, rows] = 1
    
    return A
#=====================================================================================================

#=====================================================================================================
def estimateParametersELS(model, ui, yi, *args):
    """
    The function [Parameters, ParametersP, ParametersR, vP, MP] = estimateParametersELS(model, u, yi, N)
    is part of the System Identification Package for polynomial models. Its purpose
    is to estimate the parameters of a previously detected structure using Extended Least Square method, as follows:

    Inputs:
           model ==> coded representation of the structure containing candidate
                    terms where the number of columns corresponds to the degree
                    of nonlinearity. The regressors are coded as follows:
                    y(k-i) = 100i --> output terms
                    u(k-j) = 200j --> input terms
                    e(k-l) = 300l --> noise terms

              ui ==> input data for identification
              yi ==> output data for identification
               N ==> number of iterations for MA filtering of the model.
    --------------------------------------------------------------------------
    Note: If N = [] or N = 0 (zero) parameter estimation, or if N is omitted,
    will be performed without the MA model, using Conventional Least Squares.
    --------------------------------------------------------------------------

    Outputs:
      Parameters ==> Vector of model parameters, including MA parameters when applicable
     ParametersP ==> Vector of process parameters, without the MA model
     ParametersR ==> Vector of noise parameters, only from the MA model
              vP ==> Vector of variances for the N noise iterations, when applicable
              MP ==> Matrix of estimated parameters for the N noise iterations
               e ==> Vector of identification residuals
    """
   
    #Evaluate the dimension of the input and output of the function
    N = args[0] if len(args) > 0 else 0
    
    ui = ui.reshape(-1, 1)
    yi = yi.reshape(-1, 1)
    
    #Use LS if the model is not noise or the user does not want
    numProcessTerms, numNoiseTerms, maxDelay, maxOutputDelay, maxInputDelay, maxNoiseDelay, processModel, noiseModel, model = getInfo(model)
    NT = numProcessTerms + numNoiseTerms
    P = buildRegressorMatrix(model, ui, yi)
    Par = (pinv(P) @ yi).reshape(-1, 1)
    y = P@Par
    e = yi - y
    
    if N == 0 :
        Parameters = Par
        ParametersP = Par
        ParametersR = array([])
        vP = array([])
        MP = array([])
    elif not N:
        Parameters = Par
        ParametersP = Par
        ParametersR = array([])
        vP = array([])
        MP = array([])
    else:
        MP = zeros((NT, N))
        #Estimate the model parameters
        for i in range(N):
            P = buildRegressorMatrix(model, ui, yi, e)
            Par = (pinv(P) @ yi).reshape(-1, 1)  # Mantém Par como um vetor 1D
            MP[:, i] = Par.ravel()
            y = P @ Par
            e = yi - y
         
        Parameters = mean(MP, axis=1).reshape(-1, 1)
        vP = var(MP, axis=1).reshape(-1, 1)
        # Identifica as linhas de `model` que estão em `processModel`
        I = where(any(all(model[:, None] == processModel[None, :], axis=2), axis=1))[0]
        ParametersP = Parameters[I]
    
        if numNoiseTerms != 0:
            # Identifica as linhas de `model` que estão em `noiseModel`
            J = where(any(all(model[:, None] == noiseModel[None, :], axis=2), axis=1))[0]
            ParametersR = Parameters[J]
        else:
            ParametersR = array([])

    
    return Parameters, ParametersP, ParametersR, vP, MP, e
#=====================================================================================================

#=====================================================================================================
def displayModel(model, parameters, p):
    """
    The function eq = displayModel(model, parameters) is part of the System
    Identification Package for polynomial models. Its purpose is to create a vector
    containing the elements of the model in string format, allowing the user to
    visualize the encoded model in terms of input, output, and noise data, when applicable, as follows:
    
    Inputs:
          model ==> coded representation of the structure containing candidate
                    terms where the number of columns corresponds to the degree
                    of nonlinearity. The regressors are coded as follows:
                    y(k-i) = 100i --> output terms
                    u(k-j) = 200j --> input terms
                    e(k-l) = 300l --> noise terms
    
     parameters ==> parameters estimated by the least squares estimator based on
                    the structure of the model and identification data
    
                p ==> presents the equation on a panel.
    
    Outputs:
               eq ==> vector containing the equation in string format, where each
                    row corresponds to a regressor and its parameter.
    
    """
    
    # Verify the dimension of the input and output of the function
    #--------------------------------------------------------------------------
    if model is None or parameters is None or p is None:
        raise ValueError('The function requires three inputs')
    
    # Initialize an empty string list
    #--------------------------------------------------------------------------
    eq = [''] * (model.shape[0] + 1)
    
    # Add "y(k) =" in the first row
    #--------------------------------------------------------------------------
    eq[0] = 'y(k) ='
    
    # Iterate through the rows of the model
    #--------------------------------------------------------------------------
    for i in range(model.shape[0]):
        # Initialize the term as empty
        #----------------------------------------------------------------------
        term = ''
        # Iterate through the columns of the model
        #----------------------------------------------------------------------
        for j in range(model.shape[1]):
            # Get the value of the model at the current position
            #------------------------------------------------------------------
            value = model[i, j]
            # Define the appropriate term based on the value
            #------------------------------------------------------------------
            if value >= 1000 and value < 2000:
                single_term = f'y(k-{value - 1000})'
            elif value >= 2000 and value < 3000:
                single_term = f'u(k-{value - 2000})'
            elif value >= 3000:
                single_term = f'e(k-{value - 3000})'
            else:
                single_term = ''
            #------------------------------------------------------------------
            # Multiply the elements of the columns
            #------------------------------------------------------------------
            if single_term:
                if not term:
                    term = single_term
                else:
                    term = f'{term}*{single_term}'
        
        # Add the corresponding parameter
        #----------------------------------------------------------------------
        if parameters[i] < 0:
            if not term:
                term = f'  {parameters[i]}'
            else:
                term = f'  {parameters[i]}*{term}'
        else:
            if not term:
                term = f' + {parameters[i]}'
            else:
                term = f' + {parameters[i]}*{term}'
        
        # Remove the first space and the addition sign if present
        #----------------------------------------------------------------------
        if term.startswith(' + '):
            term = term[3:]
        elif term.startswith(' - '):
            term = f'-{term[3:]}'
        
        # Add the term to the string list
        #----------------------------------------------------------------------
        eq[i + 1] = term
        
        formatted_result = [eq[0]]
        for line in eq[1:]:
            # Remover colchetes e espaços adicionais
            formatted_line = line.strip().replace('[', '').replace(']', '')
            formatted_result.append(formatted_line)
        eq = formatted_result
    if p == 1:
        # Convert the string list into a single string
        #------------------------------------------------------------------
        fullText = '\n'.join(eq)
        
        # Create a new figure with a specified size
        #------------------------------------------------------------------
        fig, ax = subplots(figsize=(5, 4))
        axis('off')
        title('Identified Model')
        
        # Add an edit control with sliders
        #------------------------------------------------------------------
        text(0.5, 0.5, fullText, fontsize=10, ha='left', va='center')
        
        show()
        
        print(' ')
        print('Dynamic Model:')
        for item in eq:
            print(f' {item}')
            
    return eq
#=====================================================================================================

#=====================================================================================================
def displayStaticModel(staticModel, u, y, p):
    """
    The function eqest = displayStaticModel(staticModel, p) is part of the System
    Identification Package for polynomial models. Its purpose is to display the
    static model in string format, allowing the user to visualize the encoded model
    in terms of input and output data, as follows:
    
    Inputs:
    staticModel ==> matrix model containing the grouping of terms and their
                    respective grouping coefficients
              u ==> static input vector
              p ==> presents the equation on a panel.
    
    Outputs:
       eqest ==> vector containing the equation in string format
        yest ==> vector of calculated output
    
    """

    # Verify the dimension of the input and output of the function
    #--------------------------------------------------------------------------
    if staticModel is None or u is None or y is None or p is None:
        raise ValueError("The function requires four inputs")

    # Chamar a função checkSubarrayForGNLY com staticModel
    result = checkSubarrayForGNLY(staticModel)
    
    # Verificar o resultado
    if result == 1:
        eqest = buildStaticModelAgroup(staticModel)
        yest, _, _ = buildStaticResponse(staticModel, u, y)
        if p == 1:
            eqestLatex = f"{eqest}"
            figure(figsize=(6, 2))
            text(0.5, 0.5, eqestLatex, fontsize=16, ha='center', va='center')
            title("Static Equation", pad=20)
            axis("off")
            show()
            
            print(' ')
            print('Static Model: ')
            print(eqest)
    else:
        # Initialize the denominator and numerator matrices
        #--------------------------------------------------------------------------
        denominator = []
        numerator = []
    
        # Initialize strings for numerator and denominator equations
        #--------------------------------------------------------------------------
        numeratorEquation = ''
        denominatorEquation = ''
    
        # Iterate over each row of the staticModel matrix
        #--------------------------------------------------------------------------
        for i in range(staticModel.shape[0]):
            # Initialize the row equation as an empty string
            #----------------------------------------------------------------------
            equation = ''
    
            # Iterate over each column, except the last (parameter)
            #----------------------------------------------------------------------
            for j in range(staticModel.shape[1] - 1):
                value = staticModel[i, j]
                if value == 1:
                    term = 'y'
                elif value == 2:
                    term = 'u'
                else:
                    term = ''  # Ignore the constant term (0)
    
                #------------------------------------------------------------------
                # Concatenate the term in the equation, ignoring constant terms
                #------------------------------------------------------------------
                if term:
                    if not equation:
                        equation = term
                    else:
                        equation += ' * ' + term
    
            # Multiply the equation by the corresponding parameter
            #----------------------------------------------------------------------
            parameter = staticModel[i, -1]
            if not equation:
                equation = f"{parameter:+g}"
            else:
                equation = f"{parameter:+g} * {equation}"
    
            # Check if the row should be added to the numerator or denominator
            #----------------------------------------------------------------------
            if 1 in staticModel[i, :]:
                denominator.append(staticModel[i, :])
                # Invert the parameter sign and add
                invertedParameter = -parameter
                if not denominatorEquation:
                    if 2 in staticModel[i, :]:
                        denominatorEquation = f"{invertedParameter:+g} * u"
                    else:
                        denominatorEquation = f"{invertedParameter:+g}"
                else:
                    if 2 in staticModel[i, :]:
                        denominatorEquation += f"  {invertedParameter:+g} * u"
                    else:
                        denominatorEquation += f"  {invertedParameter:+g}"
            else:
                numerator.append(staticModel[i, :])
                if not numeratorEquation:
                    numeratorEquation = equation
                else:
                    numeratorEquation += f"  {equation}"
    
        # Remove the initial '+' sign, if present, in the numerator
        #--------------------------------------------------------------------------
        if numeratorEquation.startswith('+'):
            numeratorEquation = numeratorEquation[1:]
    
        # Build the final equation
        #--------------------------------------------------------------------------
        eqest = f"y = ({numeratorEquation}) / (1 {denominatorEquation})"
    
        # Evaluate the calculated output
        #--------------------------------------------------------------------------
        Y = eval(f"({numeratorEquation}) / (1 {denominatorEquation})")
        yest = array(Y)
    
        # Display the equation in a panel if p == 1
        #--------------------------------------------------------------------------
        if p == 1:
            eqestLatex = f"$y = \\frac{{{numeratorEquation}}}{{1 {denominatorEquation}}}$"
            figure(figsize=(6, 2))
            text(0.5, 0.5, eqestLatex, fontsize=16, ha='center', va='center')
            title("Static Equation", pad=20)
            axis("off")
            show()
            
            print(' ')
            print('Static Model: ')
            print(eqest)

    return yest.reshape(-1,1), eqest
#=====================================================================================================

#=====================================================================================================
def checkSubarrayForGNLY(matrix):
    """
    The function result = checkSubarrayForGNLY(matrix) is part of the System
    Identification Package for polynomial models. checkSubarrayForGNLY checks 
    if there is a row with subarray [1 1] in any column combinations
    
    Inputs:
        matrix ==> The input matrix to be checked.
    
    Outputs:
        result ==> Returns 1 if there is at least one row with subarray [1 1], else returns 0.
    
    """
    
    # Initialize the result to 0 (not found)
    result = 0
    
    # Get the number of rows and columns in the matrix
    numRows, numCols = matrix.shape
    
    # Iterate over each row of the matrix
    for i in range(numRows):
        # Iterate over each combination of two columns
        for j in range(numCols - 1):
            for k in range(j + 1, numCols):
                # Check if the subarray [1 1] is present
                if matrix[i, j] == 1 and matrix[i, k] == 1:
                    result = 1
                    return result  # Exit the function as we have found a match
    
    return result
#=====================================================================================================

#=====================================================================================================
def estimateParametersRELS(model, ui, yi, N, A, B):
    """
    The function estimateParametersRELS(model, ui, yi, N, A, B)
    is part of the System Identification Package for polynomial models. Its purpose
    is to estimate the parameters of a previously detected structure using Restricted Extended Least Square, as follows:

    Inputs:
            model ==> code matrix containing the selected process and
                        noise terms a priori;
                u ==> system input data;
                y ==> system output data;
                N ==> number of noise iterations, if N is 0 the estimator executed will be the traditional Least Square;
                A ==> mapping matrix between the parameters and the
                    model term groupings;
                B ==> constraint vector;
    --------------------------------------------------------------------------
    Note: If N = [] or N = 0 (zero), or if N is omitted, parameter estimation
    will be performed without the MA model, using Conventional Least Squares.
    --------------------------------------------------------------------------

    Outputs:
    Parameters ==> Vector of model parameters, including MA parameters when applicable
    ParametersP ==> Vector of process parameters, without the MA model
    ParametersR ==> Vector of noise parameters, only from the MA model
            vP ==> Vector of variances for the N noise iterations, when applicable
            MP ==> Matrix of estimated parameters for the N noise iterations
            e  ==> Vector of identification residuals

    """

    # Evaluate the dimension of the input and output of the function
    # --------------------------------------------------------------------------
    if len([model, ui, yi, N, A, B]) < 6:
        raise ValueError('The function requires 6 inputs')
    
    # Estimate the model parameters
    # --------------------------------------------------------------------------
    # Verify if N is appropriate for use in the function
    # ----------------------------------------------------------------------
    if N is not None:
        test = N % 1
        if test != 0 or N < 0 or size(N) != 1:
            raise ValueError('N must be a positive integer')
    else:
        N = 0
    # ----------------------------------------------------------------------
    
    numProcessTerms, numNoiseTerms, _, _, _, _, processModel, _, _ = getInfo(model)
    if N == 0 or numNoiseTerms == 0:
        # Use LS if the model is not noise or the user does not want
        # ----------------------------------------------------------------------
        
        P = buildRegressorMatrix(processModel, ui, yi)
        Parameters = pinv(P).dot(yi)
        x_corr = inv(P.T @ P) @ A.T @ inv(A @ inv(P.T @ P) @ A.T) @ (A @ Parameters[:numProcessTerms] - B)
        Parameters = Parameters[:numProcessTerms] - x_corr
        e = yi - P @ Parameters
        ParametersP = Parameters
        ParametersR = []
        vP = []
        MP = []
        
    else:
        # Estimate the parameters for N noise iterations, with MA model
        # Calculate the first iteration to generate an initial noise vector
        # ----------------------------------------------------------------------
        
        P = buildRegressorMatrix(processModel, ui, yi)
        Par = pinv(P).dot(yi)
        e = yi - P @ Par
        # Initialize the variables of interest, in this case the Parameter Matrix
        # ----------------------------------------------------------------------
        MP = zeros((numProcessTerms + numNoiseTerms, N))
        MP[:numProcessTerms, 0] = Par
        # Perform the N noise iterations
        # ----------------------------------------------------------------------
        for i in range(N):
            P = buildRegressorMatrix(model, ui, yi, e)
            MP[:, i] = pinv(P).dot(yi)
            P = buildRegressorMatrix(processModel, ui, yi)
            e = yi - P @ (pinv(P).dot(yi))
        
        # Calculate the mean and variance of the estimator
        # ----------------------------------------------------------------------
        Parameters = mean(MP, axis=1)
        vP = var(MP, axis=1)
        # Allocate the parameters in terms of process or noise
        # ----------------------------------------------------------------------
        ParametersP = Parameters[:numProcessTerms]
        x_corr = inv(P.T @ P) @ A.T @ inv(A @ inv(P.T @ P) @ A.T) @ (A @ ParametersP - B)
        ParametersP = ParametersP - x_corr
        ParametersR = Parameters[numProcessTerms:]
    
    return Parameters.reshape(-1,1), ParametersP.reshape(-1,1), ParametersR.reshape(-1,1), vP.reshape(-1,1), MP, e.reshape(-1,1)
#=====================================================================================================

#=====================================================================================================
def buildStaticModelAgroup(staticModel):
    """
    The function eqest = buildStaticModelAgroup(staticModel) is an auxiliary function
    part of the System Identification Package for polynomial models.
    Its purpose is to display the static model in string format, allowing the user
    to visualize the encoded model in terms of input and output
    data when the nonlinearity degree is equal to or more than 2, as follows:
    
    Inputs:
    staticModel ==> matrix model containing the grouping of terms and their
                    respective grouping coefficients
           u ==> static input vector
           y ==> static output vector
           p ==> presents the equation on a panel.
    
    Outputs:
        eqest ==> string containing the equation in string format
    
    Example of application:
    
    # clc; close all; clear all;
    # load converter_dataset
    # nonlinearityDegree = 1
    # delay_y = 2
    # delay_u = 2
    # delay_e = 2
    # Model, Tterms, type = dsitools.generateCandidateTerms(nonlinearityDegree, [delay_y, delay_u, delay_e])
    # Model, processModel, noiseModel, ERR, ERRp, ERRr = dsitools.detectStructure(Model, u, yi, 20, 20, 1, 1)
    # Parameters, ParametersP, _, _, _ = dsitools.estimateParametersELS(Model, u, yi, 10)
    # _, _, staticModel, _ = dsitools.groupcoef(processModel, ParametersP)
    # eqest = buildStaticModelAgroup(staticModel)
    """

    # Initialize the string for the final equation
    finalEquation = 'y = '

    # Loop through each row of staticModel
    for i in range(len(staticModel)):
        termStr = ''  # Initialize the term for the current row as empty
        for j in range(len(staticModel[i]) - 1):
            if staticModel[i][j] == 0:
                continue  # Skip zero values
            elif staticModel[i][j] == 1:
                termStr += 'y'  # Replace 1 with 'y'
            elif staticModel[i][j] == 2:
                termStr += 'u'  # Replace 2 with 'u'

        # Add the coefficient (staticModel[i][-1]) to the concatenated term
        if termStr:
            finalEquation += f"{staticModel[i][-1]}*{termStr} + "
        else:
            # If all elements up to end-1 are zero, add only the coefficient
            finalEquation += f"{staticModel[i][-1]} + "

    # Check and manually remove the extra '+ ' at the end
    if len(finalEquation) > 3 and finalEquation[-3:] == ' + ':
        finalEquation = finalEquation[:-3]  # Remove the last 3 characters
    eqest = finalEquation

    return eqest
#=====================================================================================================
