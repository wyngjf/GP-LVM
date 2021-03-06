'''
BSD 3-Clause License

Copyright (c) 2017, Jack Miles Hunt
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import sys
sys.path.insert(0, './gplvm_lib')
import urllib.request
import os.path
import csv
import numpy as np
import matplotlib.pyplot as plt
import gplvm_lib as gp

irisURL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
irisFname = 'iris.data'

#Control plotting here.
showPlots = True
savePlots = False

def getIris(useColouring = True):
    """
    Loads the four dimensional Fisher Iris dataset.
    If the 'iris.data' file is not present in the working directory, 
    this function attempts to download it.
    The last column of the dataset(the text labels) are ommitted.
    """
    iris = []
    colours = []
    if not os.path.isfile(irisFname):
        print("Attempting to download the iris dataset.")
        try:
            urllib.request.urlretrieve(irisURL, irisFname)
        except urllib.request.URLError:
            sys.exit("Unable to download iris dataset. Quitting.")
    
    with open(irisFname, newline='') as file:
        reader = csv.reader(file, delimiter = ',')
        for line in reader:
            if len(line) != 0:
                #Extract feature vector.
                iris.append(list(map(float, line[0:4])))
                #Extract class label and assign colour, if necessary.
                if useColouring:
                    if line[4] == "Iris-setosa":
                        colours.append("red")
                    elif line[4] == "Iris-versicolor":
                        colours.append("green")
                    elif line[4] == "Iris-virginica":
                        colours.append("blue")
                    else:
                        sys.exit("Error reading class assignments. Check iris.data")
    
    #Randomise order - TO-DO: make this pythonic.
    for iter in range(0, 20):
        randA = np.random.randint(len(iris), size = len(iris))
        randB = np.random.randint(len(iris), size = len(iris))
        for i in range(0, len(iris)):
            #Permute feature vectors.
            tmp = iris[randA[i]]
            iris[randA[i]] = iris[randB[i]]
            iris[randA[i]] = tmp

            #Permute colours.
            tmp = colours[randA[i]]
            colours[randA[i]] = colours[randB[i]]
            colours[randA[i]] = tmp

    return {'features' : np.asarray(iris), 'colours' : colours}

def plot(data, colours, dimensionality, title, method):
    """
    Helper function to reduce code duplication.
    """
    if dimensionality == 1:
        gp.plot1D(data, title, method, savePlots)
    elif dimensionality == 2:
        gp.plot2D(data, title, method, colours, savePlots)
    elif dimensionality == 3:
        gp.plot3D(data, title, method, colours, savePlots)
    else:
        return None
    
def runPCA(data, reducedDimensions, showScree):
    """
    Runs standard PCA on the given dataset, optionally showing the associated
    Scree plot(normalised Eigenvalues)
    """
    print("-->Running PCA.")
    latent = gp.pca(data['features'], reducedDimensions, showScree, savePlots)
    plot(latent, data['colours'], reducedDimensions, "Iris Dataset", "PCA")
    
def runLinearGPLVM(data, reducedDimensions, beta):
    """
    Runs the Linear Gaussian Process Latent Variable Model on the given dataset. 
    The resultant data plotted if the latent space is 1, 2 or 3 dimensional.
    """
    print("-->Running Linear GP-LVM.")
    gplvm = gp.LinearGPLVM(data['features'])
    gplvm.compute(reducedDimensions, beta)
    latent = gplvm.getLatentSpaceRepresentation()
    plot(latent, data['colours'], reducedDimensions, "Iris Dataset", "Linear GP-LVM")
    
def runNonlinearGPLVM(data, reducedDimensions):
    """
    Runs the Nonlinear Gaussian Process Latent Variable Model on the given dataset, 
    for a given covariance matrix generating kernel.
    The resultant data plotted if the latent space is 1, 2 or 3 dimensional.
    """
    print("-->Running Nonlinear GP-LVM.")
    gplvm = gp.NonlinearGPLVM(data['features'])
    gplvm.compute(reducedDimensions, 50, maxIterations = 50, jitter = 4, learnRate = 0.01, momentum = 0.01, verbose = True)
    latent = gplvm.getLatentSpaceRepresentation()
    plot(latent, data['colours'], reducedDimensions, "Iris Dataset", "Nonlinear GP-LVM")
    
if __name__ == "__main__":
    """
    Parameters of the algorithms may be tweaked here.
    """
    
    #Dimension to reduce to.
    newDimensionality = 2
    
    #Beta parameter for Linear GP-LVM.
    beta = 2.0
    
    #Whether to display the Scree plot for PCA.
    scree = True
    
    data = getIris()
    
    runPCA(data, newDimensionality, scree)
    runLinearGPLVM(data, newDimensionality, beta)
    runNonlinearGPLVM(data, newDimensionality)
    
    if showPlots:
        plt.show()