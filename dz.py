from itertools import combinations
import pandas as pd


def get_error_factor(factor, size):
    return combinations([1<<n for n in range(size)], factor)

def xor(a, b): 
  
    # initialize result 
    result = [] 
  
    # Traverse all bits, if bits are 
    # same, then XOR is 0, else 1 
    for i in range(0, len(b)): 
        if a[i] == b[i]: 
            result.append('0') 
        else: 
            result.append('1') 
  
    return ''.join(result) 
  
  
  
# Performs Modulo-2 division 
def mod2div(dividend, divisor): 
  
    # Number of bits to be XORed at a time. 
    pick = len(divisor) 
  
    # Slicing the dividend to appropriate 
    # length for particular step 
    tmp = dividend[0: pick] 
  
    while pick < len(dividend): 
  
        if tmp[0] == '1': 
  
            # replace the dividend by the result 
            # of XOR and pull 1 bit down 
            tmp = xor(divisor, tmp)[1:] + dividend[pick] 
  
        else:   # If leftmost bit is '0' 
            # If the leftmost bit of the dividend (or the 
            # part used in each step) is 0, the step cannot 
            # use the regular divisor; we need to use an 
            # all-0s divisor. 
            tmp = xor('0'*pick, tmp)[1:] + dividend[pick] 
  
        # increment pick to move further 
        pick += 1
  
    # For the last n bits, we have to carry it out 
    # normally as increased value of pick will cause 
    # Index Out of Bounds. 
    if tmp[0] == '1': 
        tmp = xor(divisor, tmp) 
    else: 
        tmp = xor('0'*pick, tmp) 
  
    checkword = tmp 
    return checkword 



df = pd.DataFrame()
df["Кратность"] = pd.Series(dtype="int")
df["Количество общее"] = pd.Series(dtype="int")
df["Обнаружено"] = pd.Series(dtype="int")
df["обнаруживающая способность, %"] = pd.Series(dtype="float")



data = "111110100010100"
encoder = "10011"
for factor in range(1, 16):
    errors = get_error_factor(factor, 15)
    e_count = 0
    found_count = 0
    for i in errors:
        e_count += 1
        error_str = bin(sum(i))[2:].rjust(15, "0")
        encoded = xor(data, error_str)
        remainder = mod2div(encoded, encoder)
        if int(remainder) != 0:
            found_count += 1
    df.loc[len(df)] = [factor, e_count, found_count, (found_count / float(e_count)) * 100]
    
print(df.to_markdown(index=False))

