import numpy as np
import pandas as pd

def _check_input_type(c, output_names):
    if isinstance(c, np.ndarray):
        assert c.shape[0] == 2, "Numpy array does not have shape (2, N)"
        if len(c.shape)>1:
            x = c[:,0]
            y = c[:,1]
        else:
            x = c[0]
            y = c[1]
            
        ret = lambda E,N: np.array((E,N)).T
        
    elif isinstance(c, pd.DataFrame):
        x = c.iloc[:,0]
        y = c.iloc[:,1]
        ret = lambda E,N: pd.concat([E,N], axis=1).rename(columns={0:output_names[0], 1:output_names[1]})
    
    else:
        x = np.array(c[0])
        y = np.array(c[1])
        ret = lambda E,N: np.array((E,N)).T
        
    return x,y,ret

def RD_to_UTM(c, zone=31, output_names=["E","N"]):  
    """ Transforms RD-coordinates to Easting,Northing in UTM-WGS84. 

    Parameters
    ----------
    c : tuple, numpy-array or pandas dataframe
        Coordinates in the RD system. Either a tuple of (X,Y), ndarray of size (2,N) 
        or a data frame with 2 columns.
    zone : int
        UTM zone for which to compute the coordinates. These transformations are only
        valid for zones 31 and 32.
    output_names : tuple
        Names for the output columns, if input was a dataframe.

    Returns
    -------
    ndarray of shape (2,N) or dataframe
        This method will return the transformed coordinates. Output type depends on
        the input. A dataframe will be returned if the input was also a dataframe,
        otherwise the output will be a numpy array of shape (2,N), where N is the 
        number of coordinate-pairs in the input.
    """
    
    assert zone==31 or zone==32 , "These transformations are only valid for UTM zones 31 and 32."

    if zone==31:
        # Zone 31 parameters
        A = [663304.11, 99947.539, 20.008, 2.041, 0.001]
        B = [5780984.54, 3290.106, 1.310, 0.203, 0.]
    
    else:
        # Zone 32 parameters
        A = [252878.65, 99919.783, -30.208, 2.035, -0.002]
        B = [5784453.44, -4982.166, 3.016, -0.309, 0.001]     
    
    x,y,ret = _check_input_type(c, output_names)
    X = (x-155000.)*10e-6
    Y = (y-463000.)*10e-6

    E = A[0] + A[1]*X - B[1]*Y + A[2]*(X**2 - Y**2) - B[2]*(2*X*Y) + \
        A[3]*(X**3 - 3*X*Y**2) - B[3]*(3*X**2*Y - Y**3) + \
        A[4]*(X**4 - 6*X**2*Y**2 + Y**4) - B[4]*(4*X**3*Y - 4*Y**3*X) 
        
    N = B[0] + B[1]*X + A[1]*Y + B[2]*(X**2 - Y**2) + A[2]*(2*X*Y) + \
        B[3]*(X**3 - 3*X*Y**2) + A[3]*(3*X**2*Y - Y**3) + \
        B[4]*(X**4 - 6*X**2*Y**2 + Y**4) + A[4]*(4*X**3*Y - 4*Y**3*X)
            
    return ret(E,N)


def UTM_to_RD(c, zone=31, output_names=["X","Y"]):  
    """ Transforms Easting,Northing in UTM-WGS84 to RD-coordinates. 
    
    Parameters
    ----------
    c : tuple, numpy-array or pandas dataframe
        Coordinates in the UTM-WGS84 system. Either a tuple of (E,N), ndarray of 
        size (2,N) or a data frame with 2 columns.
    zone : int
        UTM zone for which to compute the coordinates. These transformations are only
        valid for zones 31 and 32.
    output_names : tuple
        Names for the output columns, if input was a dataframe.

    Returns
    -------
    ndarray of shape (2,N) or dataframe
        This method will return the transformed coordinates. Output type depends on
        the input. A dataframe will be returned if the input was also a dataframe,
        otherwise the output will be a numpy array of shape (2,N), where N is the 
        number of coordinate-pairs in the input.
    """
    assert zone==31 or zone==32 , "These transformations are only valid for UTM zones 31 and 32."
            
    if zone==31:
        # Zone 31 parameters
        E0 = 663304.11
        N0 = 5780984.54
        
        A = [155000, 99944.187, -20.039, -2.042, 0.001]
        B = [463000, -3289.996, 0.668, 0.066, 0.0]

    else:
        # Zone 32 parameters
        E0 = 252878.65
        N0 = 5784453.44
        
        A = [155000, 99832.079, 30.280, -2.034, -0.001]
        B = [463000, 4977.793, 1.514, -0.099, 0.0]
 
    E,N,ret = _check_input_type(c, output_names)
    e = (E-E0)*10e-6
    n = (N-N0)*10e-6
    
    x = A[0] + A[1]*e - B[1]*n + A[2]*(e**2 - n**2) - B[2]*(2*e*n) + \
        A[3]*(e**3 - 3*e*n**2) - B[3]*(3*e**2*n - n**3) + \
        A[4]*(e**4 - 6*e**2*n**2 + n**4) - B[4]*(4*e**3*n - 4*n**3*e)
        
    y = B[0] + B[1]*e + A[1]*n + B[2]*(e**2 - n**2) + A[2]*(2*e*n) + \
        B[3]*(e**3 - 3*e*n**2) + A[3]*(3*e**2*n - n**3) + \
        B[4]*(e**4 - 6*e**2*n**2 + n**4) + A[4]*(4*e**3*n - 4*n**3*e)

    return ret(x,y)


def RD_to_latlon(c, output_names=["lat", "lon"]):  
    """ Transforms RD-coordinates to latitude/longitude in WGS84. 
    
    
    Parameters
    ----------
    c : tuple, numpy-array or pandas dataframe
        Coordinates in the RD system. Either a tuple of (X,Y), ndarray of size (2,N) 
        or a data frame with 2 columns.

    output_names : tuple
        Names for the output columns, if input was a dataframe.

    Returns
    -------
    ndarray of shape (2,N) or dataframe
        This method will return the transformed coordinates. Output type depends on
        the input. A dataframe will be returned if the input was also a dataframe,
        otherwise the output will be a numpy array of shape (2,N), where N is the 
        number of coordinate-pairs in the input.
    """
    
    x,y,ret = _check_input_type(c, output_names)
    X = (x-155000.)*10e-6
    Y = (y-463000.)*10e-6

    P=6
    Q=5
    
    K = np.zeros((P,Q))
    K[0,1] = 3235.65389
    K[2,0] = -32.58297
    K[0,2] = -0.24750
    K[2,1] = -0.84978
    K[0,3] = -0.06550
    K[2,2] = -0.01709
    K[1,0] = -0.00738
    K[4,0] = 0.00530
    K[2,3] = -0.00039
    K[4,1] = 0.00033
    K[1,1] = -0.00012
    
    L = np.zeros((P,Q))
    L[1,0] = 5260.52916
    L[1,1] = 105.94684
    L[1,2] = 2.45656
    L[3,0] = -0.81885
    L[1,3] = 0.05594
    L[3,1] = -0.05607
    L[0,1] = 0.01199
    L[3,2] = -0.00256
    L[1,4] = 0.00128
    L[0,2] = 0.00022
    L[2,0] = -0.00022
    L[5,0] = 0.00026
    
    lat = 0.
    lon = 0.
    for p in range(P):
        for q in range(Q):
            lat += K[p,q] * X**p * Y**q
            lon += L[p,q] * X**p * Y**q
            
    lat = lat/3600 + 52.15517440 
    lon = lon/3600 + 5.38720621
    
    return ret(lat,lon)


def latlon_to_RD(c, output_names=["X","Y"]):  
    """ Transforms latitude/longitude in WGS84 to RD-coordinates. 
    
    Parameters
    ----------
    c : tuple, numpy-array or pandas dataframe
        Coordinates in the WGS84 system. Either a tuple of (lat,lon), ndarray of size (2,N) 
        or a data frame with 2 columns.
    output_names : tuple
        Names for the output columns, if input was a dataframe.

    Returns
    -------
    ndarray of shape (2,N) or dataframe
        This method will return the transformed coordinates. Output type depends on
        the input. A dataframe will be returned if the input was also a dataframe,
        otherwise the output will be a numpy array of shape (2,N), where N is the 
        number of coordinate-pairs in the input.
    """   
    lat,lon,ret = _check_input_type(c, output_names)
    La = (lat-52.15517440)*0.36
    Lo = (lon-5.38720621)*0.36

    P=4
    Q=5
    
    K = np.zeros((P,Q))
    K[0,1] = 190094.945
    K[1,1] = -11832.228
    K[2,1] = -114.221
    K[0,3] = -32.391
    K[1,0] = -0.705
    K[3,1] = -2.340
    K[1,3] = -0.608
    K[0,2] = -0.008
    K[2,3] = 0.148
    
    L = np.zeros((P,Q))
    L[1,0] = 309056.544
    L[0,2] = 3638.893
    L[2,0] = 73.077
    L[1,2] = -157.984
    L[3,0] = 59.788
    L[0,1] = 0.433
    L[2,2] = -6.439
    L[1,1] = -0.032
    L[0,4] = 0.092
    L[1,4] = -0.054
    
    x = 155000.
    y = 463000.
    for p in range(P):
        for q in range(Q):
            x += K[p,q] * La**p * Lo**q
            y += L[p,q] * La**p * Lo**q

    return ret(x,y)