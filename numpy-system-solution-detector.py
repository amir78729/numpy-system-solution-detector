import numpy as np
import sympy

def find_gcd_of_two_numbers(x, y):   
    while(y): 
        x, y = y, x % y   
    return x

def find_gcd_of_a_row(l):
    num1 = l[0] 
    num2 = l[1] 
    gcd = find_gcd_of_two_numbers(num1, num2) 
    for i in range(2, len(l)): 
        gcd = find_gcd_of_two_numbers(gcd, l[i])   
    return gcd 

def row_simplification(row):
    gcd = find_gcd_of_a_row(row)
    if gcd !=0 and gcd !=1 and gcd !=-1:
        simplified_row = row / gcd
        print('>>>',row,'/',gcd)
        print('   ->',simplified_row)
    else:
        simplified_row = row
    return simplified_row

def matrix_simplification(matrix):
    old_matrix = matrix.copy()
    for row in range(0, matrix.shape[0]):
        if find_pivot_index_in_a_row(matrix,row) != matrix.shape[1]:
            matrix = make_pivot_one(matrix, row)
    is_equal = True
    for row in range(0, matrix.shape[0]):
        for col in range(0, matrix.shape[1]):
            if matrix[row][col] != old_matrix[row][col]:
                is_equal = False      
    if not is_equal:
        print('\nsimplified matrix:')
        print_matrix(matrix)
        print('\n-------------------------------------------------------\n')
    return matrix

def swap_two_rows(matrix, x, y):  
    try:    
        matrix[[x, y]] = matrix[[y, x]]
        return matrix
    except: 
        return matrix

def move_zeros_down(matrix, row, column):
    # صفر های ستون فلانم ماتریس رو از سر فلانم به پایین ببر پایین
    j = matrix.shape[0]-1
    for i in range(row, matrix.shape[0]):
        if matrix[i][column] == 0  and matrix[j][column] != 0 and i<j:
            print(i,j)
            print('>>> replace row',i,' and row',j)
            swap_two_rows(matrix, i, j)
            j = j - 1   
    return matrix

def move_zero_rows_down(matrix):
    j = matrix.shape[0]-1
    for i in range(0, matrix.shape[0]):
        # if matrix[i][column] == 0  and matrix[j][column] != 0 and i<j:
        if is_row_zero(matrix,i)  and not is_row_zero(matrix,j) and i<j:
            print(i,j)
            print('>>> replace row',i,' and row',j)
            swap_two_rows(matrix, i, j)
            j = j - 1   
    return matrix

def find_pivot_index_in_a_row(matrix, row):
    pivot_index = 0
    for i in range(0,matrix.shape[1]):
        if abs(round(matrix[row][i],1)) == 0.0:
            pivot_index += 1
        else:
            break
    return pivot_index

def add_rows_to_eachother(matrix, up, down):
    pivot_index = find_pivot_index_in_a_row(matrix, up)
    if (pivot_index == matrix.shape[1]): #zero row
        print('   >>> interchange:')
        print('      >>> replace row',up,' and row',(matrix.shape[0]-1)-count_zero_rows(matrix)+1)
        swap_two_rows(matrix,up,(matrix.shape[0]-1)-count_zero_rows(matrix)+1)
        return matrix
    up_coefficient = matrix[up][pivot_index]
    down_coefficient = matrix[down][pivot_index]
    print('\n   >>> replacement:')
    print_status_of_adding_row_to_each_other(up,down,up_coefficient,down_coefficient)
    for i in range(0, matrix.shape[1]):
        matrix[down][i] = matrix[down][i] - (down_coefficient/up_coefficient)*matrix[up][i]
    return matrix

def print_status_of_adding_row_to_each_other(up,down,up_coefficient,down_coefficient):
    #EXAMPLE:
    # >>> R4  <- (-8 / 4)R2  + R4
    print('      >>> R',end = '')
    print(down,' <- ',end = '')
    print('(',end = '')
    print(round(down_coefficient,1),end = '')
    print(' / ',end = '')
    print(round(up_coefficient,1),end = '')
    print(')R',end = '')
    print(up,' + R',end = '')
    print(down)

def make_lower_elements_zero (matrix, row):
    old_matrix = matrix.copy()
    for i in range(row + 1, matrix.shape[0] ):
        matrix= add_rows_to_eachother(matrix, row, i)
    is_equal = True
    for row in range(0, matrix.shape[0]):
        for col in range(0, matrix.shape[1]):
            if matrix[row][col] != old_matrix[row][col]:
                is_equal = False
                break
        if not is_equal:
            break
    if not is_equal:
        print('\nsimplified matrix:')
        print_matrix(matrix)
        print('\n-------------------------------------------------------\n')
    return matrix

def is_inconsistent(echelon_matrix):
    for row in range(0, echelon_matrix.shape[0]):
        coefficients_are_zero = True
        for col in range(0,echelon_matrix.shape[1]-1):
            if echelon_matrix[row][col] != 0:
                coefficients_are_zero = False
                break
        if coefficients_are_zero and echelon_matrix[row][-1] != 0:
            return True
    return False      

def count_zero_rows(matrix):
    number_of_zero_rows = 0
    for row in range(0,matrix.shape[0]):
        coefficients_are_zero = True
        for col in range(0,matrix.shape[1]):
            if matrix[row][col] != 0:
                coefficients_are_zero = False
                break
        if coefficients_are_zero:
            number_of_zero_rows += 1
    return number_of_zero_rows

def state_of_system(matrix):
    print_pivot_form(matrix)
    print('')
    if is_inconsistent(matrix):
        print('The system is INCONSISTENT -> 0 answers.')
    elif count_zero_rows(matrix)==0:
        print('The system is CONSISTENT.')
    else:
        print('The system is CONSISTENT with infinite answer.(with',count_zero_rows(matrix),'zero row(s))')

def the_system_has_one_answer(matrix):
    return not is_inconsistent(matrix) and count_zero_rows(matrix) == 0

def print_pivot_form(matrix):
    #the input must be echelon
    print('pivots:')
    for row in range(0,matrix.shape[0]):
        print('[  ', end = '')
        pivot_found = False
        inconsistent = False
        for col in range(0,matrix.shape[1]):
            if not pivot_found:
                if abs(round(matrix[row][col],1)) == 0.0:
                    print('0', end = '  ')
                else:
                    print('P', end = '  ')
                    pivot_found = True
                    if col == matrix.shape[1]-1:
                        inconsistent = True
            else:
                print('?', end = '  ')
        if inconsistent:
            print('] <- because of this row the system is INCONSISTENT')
        elif is_row_zero(matrix, row):
            print('] <- zero row')
        else:
            print(']')

def is_row_zero(matrix, row):
    is_zero = True
    for i in range(0, matrix.shape[1]):
        if abs(round(matrix[row][i],1)) != 0.0:
            is_zero = False
            break
    return is_zero

def augmented(coefficients_matrix, constant_matrix):
    A = coefficients_matrix
    b = constant_matrix
    print('A:')
    print_matrix(coefficients_matrix)
    print('b:')
    print_matrix(constant_matrix)
    augmented = np.column_stack((A, b))
    print('augmented matrix:')
    print_matrix(augmented)
    return augmented

def make_upper_elements_zero (matrix, row):
    old_matrix = matrix.copy()
    for i in range(0, row ):
        matrix= add_rows_to_eachother(matrix, row, i)
    is_equal = True
    for row in range(0, matrix.shape[0]):
        for col in range(0, matrix.shape[1]):
            if matrix[row][col] != old_matrix[row][col]:
                is_equal = False
                break
        if not is_equal:
            break
    if not is_equal:
        print('\nsimplified matrix:')
        print_matrix(matrix)
        print('\n-------------------------------------------------------\n')
    return matrix

def make_echelon(matrix):
    row = 0
    for i in range(0,matrix.shape[1]):
        move_zero_rows_down(matrix)
        print_equations(matrix)
        print('>>> elementary row operations:')
        print('   >>> scaling:')
        matrix = matrix_simplification(matrix)
        matrix = make_lower_elements_zero(matrix,row)
        if row > matrix.shape[0]-1:
            break
        if matrix[row][i] != 0:
            matrix = move_zeros_down(matrix, row, i)
            row += 1
    return matrix

def make_reduced_echelon(echelon_matrix):
    for row in reversed(range(1,echelon_matrix.shape[0])):
        echelon_matrix = make_upper_elements_zero(echelon_matrix , row)
        echelon_matrix = make_pivot_one(echelon_matrix, row)
        print_equations(echelon_matrix)
    print('reduced echelon form:')
    print_matrix(echelon_matrix)
    return echelon_matrix

def make_pivot_one(matrix ,row):
    if is_row_zero(matrix, row):
        return matrix
    pivot = matrix[row][find_pivot_index_in_a_row(matrix, row)]
    if abs(round(pivot,1)) != 0.0 and pivot !=1:
        simplified_row = matrix[row] / pivot
        print('\n      >>> [',end='')
        for col in range(0, matrix.shape[1]):
            print(round(matrix[row][col],1), end='   ')
        print('] /',round(pivot,1))
        print('           -> [ ',end='')
        for col in range(0, matrix.shape[1]):
            print(round(simplified_row[col],1), end='   ')
        print(']')
    else:
        simplified_row = matrix[row]
    matrix[row] = simplified_row
    return matrix

def print_matrix(matrix):
    for row in range(matrix.shape[0]):
        if row == 0:
            print('  [[', end = ' ')
        else:
            print('   [', end = ' ')
        for col in range(matrix.shape[1]):
            print(round(matrix[row][col], 1), end ='   \t\t')
        if row == matrix.shape[0] - 1:
            print(']]')
        else:
            print(']')

def print_equations(matrix):
    print('>>> row equations:')
    for row in range(0, matrix.shape[0]):
        print('\n   >>> row',end = '')
        print(row+1,': ', end='')
        left_side_is_zero = True
        for col in range(0, matrix.shape[1] - 1):
            if matrix[row][col] != 0:
                if not left_side_is_zero:
                    print('+ ', end = '')
                left_side_is_zero = False
                print('x', end = '')
                print(col + 1, end = '')
                print('(', end = '')
                print(round(matrix[row][col], 1), end = ')\t')
        if left_side_is_zero:
            if round(matrix[row][-1]) != 0 :
                print('0 ', end = '')
                print('=', round(matrix[row][-1], 1))
            else: 
                print('0 ', end = '')
                print('=', round(matrix[row][-1], 1))
        else :
            print('=', round(matrix[row][-1], 1))
    print('')

def show_answers_for_unique_answer(pivot_indexes, answers):
    print('>>> the only answer of this system is:')
    for i in range(0, answers.shape[0]):
        print('   >>> x', end ='')
        print(pivot_indexes[i] + 1,'= ', end ='')
        print(round(answers[i][0],1))

def return_pivot_indexes(matrix):
    pivot_indexes = []
    for row in range (0, matrix.shape[0]):
        if find_pivot_index_in_a_row(matrix, row) != matrix.shape[1]:
            pivot_indexes.append(find_pivot_index_in_a_row(matrix, row))
    return pivot_indexes

def return_free_indexes(matrix):
    pivot_indexes = []
    for row in range (0, matrix.shape[0]):
        if not row in return_pivot_indexes(matrix):
            pivot_indexes.append(find_pivot_index_in_a_row(matrix, row))
    return pivot_indexes

def show_answers_for_infinity_answers(matrix):
    print('>>> the answers of this system are:')
    a = matrix
    for row in range(0,a.shape[0]):
        pivot = find_pivot_index_in_a_row(a, row)
        if pivot != a.shape[1]:
            print('   >>> x', end='')
            print(pivot + 1 , '= ', end = '')
            left_side_is_zero = True
            for col in range(0, matrix.shape[1] - 1):
                if matrix[row][col] != 0 and col !=  pivot:
                    left_side_is_zero = False
                    print('- x', end = '')
                    print(col + 1, end = '')
                    print('(', end = '')
                    print(round(matrix[row][col], 1), end = ')\t')
            print('+',round(a[row][-1],1))
    #print free variables:
    for i in range (0,a.shape[1]-1):
        if not i in return_pivot_indexes(matrix):
            print('   >>> x', end='')
            print(i + 1 , '= free')

def show_answers_by_vectors(matrix):
    #input is reduced echelon
    print('>>> vector form of the answers')
    number_of_variables = matrix.shape[1]-1
    if number_of_variables > matrix.shape[0]:
        zero_row = []
        for i in range (matrix.shape[1]):
            zero_row.append(0.0)
        zero_row = np.array(zero_row)
    for i in range(number_of_variables - matrix.shape[0]):
        matrix = np.vstack((matrix, zero_row))

    x = []
    for i in range(0, number_of_variables):
        x.append(i+1)
    x = np.array(x)
    x = x.reshape(-1,1)

    c = [] #constast
    for i in range(0, number_of_variables):
        if i < matrix.shape[0]:
            c.append(matrix[i][-1])
        else:
            c.append(0.)
    c = np.array(c)
    c = c.reshape(-1,1)

    number_of_free_variables = len(return_free_indexes(matrix))
    f = {} #free variables
    for i in range(0, number_of_variables):
        if i not in return_pivot_indexes(matrix):
            tmp = []
            for var in range(0, number_of_variables):
                if var != i:
                    tmp.append(-matrix[var][i])
                else:
                    tmp.append(1.0)
            
            tmp = np.array(tmp)
            tmp = tmp.reshape(-1,1)
            f[i] = tmp
    print('   >>>  X = C ',end='')
    for i in f:
        print('+ x',end = '')
        print(i+1, end = '')
        print('(F',end = '')
        print(i+1, end = ') ')
    print('\nWhere:')
    print('\n>>> X:')
    
    for row in range(x.shape[0]):
        if row == 0:
            print('[[', end = ' ')
        else:
            print(' [', end = ' ')
        for col in range(x.shape[1]):
            print('x',end='')
            print(round(x[row][col], 1), end ='   \t')
        if row == x.shape[0] - 1:
            print(']]')
        else:
            print(']')
    print('\n>>> C:')
    print_matrix(c)

    for i in f:
        print('\n>>> F',end = '')
        print(i+1,':')
        print_matrix(f[i])
        print('')

def calculate_rankA(matrix):
    print('>>> rank(A) = dim(Col(A)) =', np.linalg.matrix_rank(matrix))

def calculate_dim_NulA(matrix):
    print('>>> dim(Nul(A)) =', matrix.shape[1] - np.linalg.matrix_rank(matrix))

def create_matrix(R,C,name):
    matrix = [] 
    print("Enter the entries rowwise:")  
    for i in range(R):
        a =[] 
        for j in range(C):
            print(name,end='')
            print('[',end='')
            print(i,end='')
            if C > 1:
                print('][',end='') 
                print(j,end='')
            print('] = ',end='')
            a.append(float(input())) 
        matrix.append(a) 
    numpy_matrix = np.array(matrix)
    print('matrix',name,'created!:')
    print_matrix(numpy_matrix)
    return numpy_matrix

def exercise_1(coefficients_matrix, constant_matrix):
    print('\n\n*******************************************************')
    print('********************** EXERCISE1 **********************')
    print('*******************************************************')
    print('************ CREATING THE AUGMENTED MATRIX ************')
    print('*******************************************************')
    augmented_matrix = augmented(coefficients_matrix, constant_matrix)

    print('\n\n*******************************************************')
    print('*************** MAKE THE SYSTEM ECHELON ***************')
    print('*******************************************************')
    echelon = make_echelon(augmented_matrix)
    print("echelon form:")
    print_matrix(echelon)

    
    print('\n\n*******************************************************')
    print('*********** MAKE THE SYSTEM REDUCED ECHELON ***********')
    print('*******************************************************')
    reduced_echelon = make_reduced_echelon(echelon)

    print('\n\n*******************************************************')
    print('*********************** RESULTS ***********************')
    print('*******************************************************')
    state_of_system(reduced_echelon)

    if(not is_inconsistent(reduced_echelon)):
        print('\n\n*******************************************************')
        print('*********************** ANSWERS ***********************')
        print('*******************************************************')
        try:
            # if the system has 1 answer
            show_answers_for_unique_answer(sympy.Matrix(reduced_echelon).rref()[1], np.linalg.solve(coefficients_matrix,constant_matrix))
            show_answers_by_vectors(reduced_echelon)
            return 
        except:
            # if the system has infinite answers
            show_answers_for_infinity_answers(reduced_echelon)
            show_answers_by_vectors(reduced_echelon)
            return

def exercise_2(coefficients):
    print('\n*******************************************************')
    print('********************** EXERCISE2 **********************')
    print('*******************************************************')
    print('A =')
    print_matrix(coefficients)
    calculate_dim_NulA(coefficients)
    calculate_rankA(coefficients)
    print('   >>> we can see that:\n       rank(A) + dim(Nul(A)) =', np.linalg.matrix_rank(coefficients),'+',coefficients.shape[1] - np.linalg.matrix_rank(coefficients),'=',coefficients.shape[1],'= n')

def start():
    print('*******************************************************')
    print('**************** Applied Linear Algebra ***************')
    print('********************** Project #1 *********************')
    print('**************** Amirhossein Alibakhshi ***************')
    print('********************** id:9731096 *********************')
    print('*******************************************************\n')
    print('Hi! How do you want to work with this ')
    print('program?')
    print('1 - using ready matrixes')
    print('2 - using my own inputs')
    print('-1 - exit the program')
    command = int(input('please enter your choice:  '))
    while command != -1:
        if command == 1:
            exercise_1(coefficients,constant)
            exercise_2(coefficients)
            print('Now how do you want to work with this ')
            print('program?')
            print('1 - using ready matrixes')
            print('2 - using my own inputs')
            print('-1 - exit the program')
            command = int(input('please enter your choice:  '))
        elif command == 2:
            R = int(input("Enter the number of rows:")) 
            C = int(input("Enter the number of columns:")) 
            my_coefficients =  create_matrix(R, C,'A')
            my_constant = create_matrix(R, 1, 'b')
            exercise_1(my_coefficients,my_constant)
            exercise_2(my_coefficients)
            print('\n*******************************************************')
            print('**************** Applied Linear Algebra ***************')
            print('********************** Project #1 *********************')
            print('**************** Amirhossein Alibakhshi ***************')
            print('********************** id:9731096 *********************')
            print('*******************************************************\n')
            print('Now how do you want to work with this ')
            print('program?')
            print('1 - using ready matrixes')
            print('2 - using my own inputs')
            print('-1 - exit the program')
            command = int(input('please enter your choice:  '))
        else:
            command = int(input('please enter a valid number:  '))
    print('bye:)')


#####################################################################
# READY MATRIXES
# homework examples
coefficients = np.array([[1.,3.,2.,-4.,3.],
    [-2.,-1.,2.,6.,4.],
    [0.,-1.,3.,-5.,1.],
    [3.,-4.,2.,5.,-7.],
    [1.,2.,-8.,6.,1.]])

constant = np.array([[-3.],
    [19.],
    [-2.],
    [-11.],
    [4.]])

################################################
# homework example with a zero row
# coefficients = np.array([[1.,3.,2.,-4.,3.],
#     [-2.,-1.,2.,6.,4.],
#     [0.,-1.,3.,-5.,1.],
#     [3.,-4.,2.,5.,-7.],
#     [0.,0.,0.,0.,0.]])

# constant = np.array([[-3.],
#     [19.],
#     [-2.],
#     [-11.],
#     [0.]
#     ])

# ################################################
# # ex1
# coefficients = np.array([[3.,5.,-4.],
# [-3.,-2.,4.],
# [6.,1.,8.]])

# constant = np.array([[7.],
# [-1.],
# [-4.]
# ])

# ################################################
# #ex2
# coefficients = np.array([[3.,5.,-4.],
# [-3.,-2.,4.],
# [0.,0.,0.]])

# constant = np.array([[7.],
# [-1.],
# [0.]
# ])

start()
