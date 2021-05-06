import numpy as np
import sys
import os

###Script has to be converted to .exe in Console-Mode because it ask for inputs and will print some values###

def get_xyz_and_res_file():
    """Lists all xyz and res files in the directory.
    
    The User has to choose the files he want by inputting the corresponding number.

    Returns a List: list_files = [xyz_file, res_file]

    """
    global xyz_file
    global res_file
    list_files_inDir = os.listdir(os.getcwd())
    dict_xyz_files = {}
    dict_res_files = {}
    text_xyz_files = ""
    text_res_files = ""
    count_xyz = 0
    count_res = 0
    check_xyz = False
    check_res = False
    for file in list_files_inDir:
        if file.endswith(".xyz"):
            count_xyz = count_xyz + 1
            text_xyz_files = text_xyz_files + f"[{count_xyz}]\t{file}\n"
            dict_xyz_files[count_xyz] = file        
            check_xyz = True
        elif file.endswith(".res"):
            count_res = count_res + 1
            text_res_files = text_res_files + f"[{count_res}]\t{file}\n"
            dict_res_files[count_res] = file
            check_res = True
    if check_xyz == False:
        print("No xyz-file was found!")
        while True:
            i = 0 #infinite while loop so that the user can see the message in the console.
    if check_res == False:
        print("No xyz-file was found!!!!")
        while True:
            i = 0 #infinite while loop so that the user can see the message in the console.
        
    print("Found the following xyz-files in the script's directory:")
    while True:
        print(text_xyz_files)
        xyz_input_str = input("Choose the desired xyz-file by signing in the corresponding number: ")
        try:
            xyz_input_int = int(xyz_input_str)
            if xyz_input_int > count_xyz or xyz_input_int <= 0:
                print("\nError! Please only sign in a valid number:")
            else:
                xyz_file = dict_xyz_files[xyz_input_int]
                break
        except ValueError:
            print("\nError! Please only sign in the corresponding number:")

    print("\n")
    print("Found the following res-files in the script's directory:")
    while True:
        print(text_res_files)
        res_input_str = input("Choose the desired res-file by signing in the corresponding number: ")
        try:
            res_input_int = int(res_input_str)
            if res_input_int > count_res or res_input_int <= 0:
                print("\nError! Please only sign in a valid number:")
            else:
                res_file = dict_res_files[res_input_int]
                break
        except ValueError:
            print("\nError! Please only sign in the corresponding number:")
    
    list_files = [xyz_file, res_file]
    return list_files

#def Mbox(title, text, style):
	##  Styles:
	##  0 : OK
	##  1 : OK | Cancel
	##  2 : Abort | Retry | Ignore
	##  3 : Yes | No | Cancel
	##  4 : Yes | No
	##  5 : Retry | Cancel 
	##  6 : Cancel | Try Again | Continue

#    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def get_cell_parameters(res_file):
    """Function reads the .res-file given by the input and search for the CELL line.


    Returns a dictionary as follows:
    {"a":a,
    "b":b,
    "c":c,
    "alpha":alpha,
    "beta":beta,
    "gamma":gamma
    }

    a,b,c,alpha,beta,gamme = Float
    """
    res_file_read = open(res_file, "r", encoding="utf-8")
    list_lines = res_file_read.readlines()
    res_file_read.close()
    for line in list_lines:
        if "CELL" in line:
            cell = line
            break
    cell = cell.replace("\t", " ")
    cell = cell.replace("\n", "")
    list_cell_split = cell.split(" ")
    list_cell_split = list(filter(None, list_cell_split)) #delets empty strings out of list incase there would be more than 1 spacebar between numbers

    a = float(list_cell_split[2])
    b = float(list_cell_split[3])
    c = float(list_cell_split[4])
    alpha = float(list_cell_split[5])
    beta = float(list_cell_split[6])
    gamma = float(list_cell_split[7])

    #returns a dictionary
    return {"a":a,
    "b":b,
    "c":c,
    "alpha":alpha,
    "beta":beta,
    "gamma":gamma
    }

#build_conversion_matrix_fract_to_cart not needed in this script. However, its nice to know how it works ;)
def build_conversion_matrix_fract_to_cart(a, b, c, alpha, beta, gamma):
    """
    Return the transformation matrix that converts cartesian coordinates to
    fractional coordinates.

    Parameters
    ----------
    a, b, c : float
        The lengths of the edges.
    alpha, gamma, beta : float
        The angles between the sides.
    
    Returns
    -------
    r : array_like
        The 3x3 rotation matrix. ``V_frac = np.dot(r, V_cart)``.
    """
    #Conversion from Deg to Rad-----------
    alpha = (np.pi/180)*alpha #First way to do it
    beta = np.deg2rad(beta) #Second way to do it
    gamma = np.deg2rad(gamma)

    #-------------------------------------    
    cosa = np.cos(alpha)
    cosb = np.cos(beta)
    cosg = np.cos(gamma)
    #sina = np.sin(alpha)
    #sinb = np.sin(beta)
    sing = np.sin(gamma)
    volume = a*b*c*np.sqrt(1-(cosa**2)-(cosb**2)-(cosg**2)+(2*cosa*cosb*cosg))
    
    #Conversionmatrix----------------------------------------------
    vec_x1 = a
    vec_x2 = b * cosg
    vec_x3 = c * cosb
    vec_y1 = 0
    vec_y2 = b * sing
    vec_y3 = (c * (cosa - cosb * cosg)) / sing
    vec_z1 = 0
    vec_z2 = 0
    vec_z3 = volume/(a*b*sing)
    conversion_matrix_fract_to_cart = np.array([[vec_x1, vec_x2, vec_x3], [vec_y1, vec_y2, vec_y3], [vec_z1, vec_z2, vec_z3]], dtype=np.float32)
    return conversion_matrix_fract_to_cart

def build_conversion_matrix_cart_to_fract(a, b, c, alpha, beta, gamma):
    """
    Return the transformation matrix that converts cartesian coordinates to
    fractional coordinates.

    Parameters
    ----------
    a, b, c : float
        The lengths of the edges.
    alpha, gamma, beta : float
        The angles between the sides.
    
    Returns
    -------
    r : array_like
        The 3x3 rotation matrix. ``V_frac = np.dot(r, V_cart)``.
    """
    #Conversion from Deg to Rad-----------
    alpha = (np.pi/180)*alpha #First way to do it
    beta = np.deg2rad(beta) #Second way to do it
    gamma = np.deg2rad(gamma)

    #-------------------------------------    
    cosa = np.cos(alpha)
    cosb = np.cos(beta)
    cosg = np.cos(gamma)
    #sina = np.sin(alpha)
    #sinb = np.sin(beta)
    sing = np.sin(gamma)
    volume = a*b*c*np.sqrt(1-(cosa**2)-(cosb**2)-(cosg**2)+(2*cosa*cosb*cosg))
    
    #Conversionmatrix----------------------------------------------
    vec_x1 = 1/a
    vec_x2 = -cosg/(a*sing)
    vec_x3 = (((b*cosg*c*(cosa-cosb*cosg))/sing)-(b*c*cosb*sing))/volume
    vec_y1 = 0
    vec_y2 = 1/(b*sing)
    vec_y3 = -(a*c*(cosa-cosb*cosg))/(volume*sing)
    vec_z1 = 0
    vec_z2 = 0
    vec_z3 = (a*b*sing)/volume
    conversion_matrix_cart_to_fract = np.array([[vec_x1, vec_x2, vec_x3], [vec_y1, vec_y2, vec_y3], [vec_z1, vec_z2, vec_z3]], dtype=np.float32)
    return conversion_matrix_cart_to_fract

def convert_coordinates(xyz_file, conversion_matrix_cart_to_fract):
    """Converts the vector (np.array) of cartesian coordinates to a cell dependent fractional coordinate vektor (np.array) by using the created matrix (np.array, dtype = float32).

    Input:  
    xyz_file: Filename of the .xyz-file to get the cartesian coordinates from
    conversion_matrix_cart_to_fract: 3x3 matrix (np.array, dtype=float32) to convert the coordinates

    Returns the text (str) to write into the choosen .res-file
    """
    #variables:-------------------------------------------------
    atom_count = 901 #needed for naming the atoms later 
    text_write_total = "\nAFIX 137\n"
    check_for_H = False
    #-----------------------------------------------------------

    xyz = open(xyz_file, "r", encoding="utf-8")
    list_lines_xyz = xyz.readlines()
    xyz.close
    new_xyz_file = xyz_file.replace(".xyz","") + "_converted.xyz"
    file_write = open(new_xyz_file, "w", encoding="utf-8")
    file_write.write(f"{list_lines_xyz[0]}{list_lines_xyz[1]}")

    for i in range(2,len(list_lines_xyz),1):
        line =  list_lines_xyz[i].replace("\t", " ")
        line = line.replace("\n", "")
        xyz_cart_list = line.split(" ")
        xyz_cart_list = list(filter(None, xyz_cart_list)) #delets empty strings out of list incase there would be more than 1 spacebar between numbers
        atom_name = xyz_cart_list[0]
        del xyz_cart_list[0]
        xyz_cart_arr = np.array(xyz_cart_list, dtype=np.float32)
        xyz_frac_arr = conversion_matrix_cart_to_fract.dot(xyz_cart_arr) #convert coordinates by multiplying matrix (conversion_matrix_cart_to_fract) with  xyz_cart_arr

        if atom_name == "H": #puts number behind H Atoms. Should only be dummy atoms out of shape measurements! Creates a string, which can be used later to write into the res.file
            check_for_H = True
            text_write = f"{atom_name}{atom_count}"+"  "+"2"+"    "+"{:.6f}".format(xyz_frac_arr[0])+"   "+"{:.6f}".format(xyz_frac_arr[1])+"    "+"{:.6f}".format(xyz_frac_arr[2])+"    "+"11.00000"+"   "+"-1.50000"+"\n"
            text_write_total = text_write_total + text_write            
            atom_count = atom_count + 1

        file_write.write(f"{atom_name}"+"\t"+"{:.6f}".format(xyz_frac_arr[0])+"\t"+"{:.6f}".format(xyz_frac_arr[1])+"\t"+"{:.6f}".format(xyz_frac_arr[2])+"\n")
    
    text_write_total = text_write_total + "\nHKLF 4\n"
    file_write.close()

    if check_for_H == False:
        print("No Dummy-H atoms found! Please change the .xyz-file to the necessary format")
        while True:
            i = 0 #infinite while loop so that the user can see the message in the console.

    return  text_write_total

def write_into_res(res_file, text_into_res): 
    """Writes Dummy H-Atoms into the choosen .res-file.

    Searches for "HKLF 4" in res-file, which marks the end of the coordinates.
    """
    res_file_handle = open(res_file, "r", encoding="utf-8")
    list_lines_res = res_file_handle.readlines()
    res_file_handle.close()
    for i in range(0, len(list_lines_res),1):
        if "HKLF 4" in list_lines_res[i]:
            list_lines_res[i] = text_into_res
            break
    res_file_handle = open(res_file, "w", encoding="utf-8")
    res_file_handle.writelines(list_lines_res)
    res_file_handle.close()
    
if __name__ == "__main__":    
    print("----------JulezxXXx: Coordinate-Converter-----------")
    print("Searching for files in scripts directory...\n")
    list_files = get_xyz_and_res_file()
    xyz_file = list_files[0]
    res_file = list_files[1]
    dict_cell_parameters = get_cell_parameters(res_file)
    print("\n----------------------------------------------------")
    print("Cell parameters:\n")
    print(f"a = {dict_cell_parameters['a']}")
    print(f"b = {dict_cell_parameters['b']}")
    print(f"c = {dict_cell_parameters['c']}")
    print(f"alpha = {dict_cell_parameters['alpha']}")
    print(f"beta = {dict_cell_parameters['beta']}")
    print(f"gamma = {dict_cell_parameters['gamma']}")
    print("----------------------------------------------------")
    conversion_matrix_cart_to_fract = build_conversion_matrix_cart_to_fract(dict_cell_parameters["a"], dict_cell_parameters["b"], dict_cell_parameters["c"], dict_cell_parameters["alpha"], dict_cell_parameters["beta"], dict_cell_parameters["gamma"])
    print("Conversion Matrix:\n")
    print(conversion_matrix_cart_to_fract)
    print("----------------------------------------------------")
    text_into_res = convert_coordinates(xyz_file, conversion_matrix_cart_to_fract)
    print(f"Text to insert into {res_file}:")
    text_into_res_print = text_into_res.replace("\nHKLF 4\n", "") #removes the \nHKLF4 for the console user-print
    text_into_res_print = text_into_res_print[:-1]#removes the \n at the end.
    print(text_into_res_print)
    print("----------------------------------------------------")
    write_into_res(res_file, text_into_res)
    print(f"\nSuccessfully converted coordinates and transferred Dummy-H atoms into {res_file}.\nCopyright 2021 by JulezX aka Hackerman.")
    while True:
        i = 0

