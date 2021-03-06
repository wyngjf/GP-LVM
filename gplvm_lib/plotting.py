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

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot1D(data, title, method, savePlot = False):
    """
    Plots data in one dimension.
    """
    if data.shape[0] == 0 or data.shape[1] != 1:
        raise ValueError("Incorrect dimensions of data for 1D plotting.")

    #Plot.
    plt.figure()
    x = np.array(range(1, data.shape[0]+1))
    plt.plot(x, data)
    plt.xticks(x)
    plt.xlabel("Data point ID's")
    plt.ylabel("Value")
    plt.title("1D Latent Space Representation of %s using %s" % (title, method))
    #plt.grid(True)
    
    if savePlot:
        plt.savefig("1D_latent_%s_%s.png" % (title.replace(" ", ""), method.replace(" ", "")))
    #plt.show()
    
def plot2D(data, title, method, colours = [], savePlot = False):
    """
    Plots the data in two dimensions as a 2D scatter graph.
    Optionally, a list of per point colours can be provided.
    """
    if data.shape[0] == 0 or data.shape[1] != 2:
        raise ValueError("Incorrect dimensions of data for 2D plotting.")
        
    x = data[:, 0]
    y = data[:, 1]
        
    #Plot
    plt.figure()
    if len(colours) == data.shape[0]:
        plt.scatter(x, y, c = colours)
    else:
        plt.scatter(x, y)
    plt.xlabel("X Dimension")
    plt.ylabel("Y Dimension")
    plt.title("2D Latent Space Representation of %s using %s" % (title, method))
    #plt.grid(True)
    
    if savePlot:
        plt.savefig("2D_latent_%s_%s.png" % (title.replace(" ", ""), method.replace(" ", "")))
    #plt.show()
    
def plot3D(data, title, method, colours = [], savePlot = False):
    """
    Plots the data in three dimensions as a 3D scatter graph.
    Optionally, a list of per point colours can be provided.
    """
    if data.shape[0] == 0 or data.shape[1] != 3:
        raise ValueError("Incorrect dimensions of data for 3D plotting.")
        
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    
    #Plot.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if len(colours) == data.shape[0]:
        ax.scatter(x, y, z, c = colours)
    else:
        ax.scatter(x, y, z)
    ax.set_xlabel('X Dimension')
    ax.set_ylabel('Y Dimension')
    ax.set_zlabel('Z Dimension')
    ax.set_title("3D Latent Space Representation of %s using %s" % (title, method))
    
    if savePlot:
        plt.savefig("3D_latent_%s_%s.png" % (title.replace(" ", ""), method.replace(" ", "")))