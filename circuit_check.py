"""Simple logic comparison for circuit problems."""


def solution(x: bool, y: bool, z: bool):
    # enter solution logic here
    return (not y and not x) or (x and not z);

def student(x: bool, y: bool, z: bool):
    # enter student logic here
    return ((not y or x) and not x) or (not z and x);


match = True;
for x in [True, False]:
    for y in [True, False]:
        for z in [True, False]:
            out_answer = solution(x, y, z);
            out_student = student(x, y, z);
            if (out_answer != out_student):
                match = False;
                x_str = 'T' if x else 'F';
                y_str = 'T' if y else 'F';
                z_str = 'T' if x else 'F';
                
                print(f"For x={x_str}, y={y_str}, z={z_str}, the output is {out_student} when it should be {out_answer}")
            
print("All good" if match else "Something is wrong")
