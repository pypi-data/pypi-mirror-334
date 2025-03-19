#Dependencies for testing only
from random import randint
from CiteSoft_py import *

def main():
    print("Welcome to CiteSoft!")
    print("Running test cases...")
    test_inline_citation()
    test_inline_citation_err()
    test_wrapper_func()
    test_semantic_version()
    test_decimal_version()
    print("Appending citations to data file")
    compile_checkpoints_log()
    compile_consolidated_log()

#Test Cases
def test_inline_citation():
    print("Testing inline citations")
    unique_id = "TestID"
    software_name = "CiteSoft"
    import_cite(unique_id, software_name)

def test_inline_citation_err():
    print("Testing inline citations")
    unique_id = "TestID"
    software_name = "CiteSoft"
    kwargs = {"nonstandardfieldname" : "value"}
    import_cite(unique_id, software_name, **kwargs)

def test_semantic_version():
    print("Testing semantic version comparison")
    unique_id = "ver_test"
    software_name = "CiteSoft"
    for _ in range(1, 4):
        kwargs = {"version": str(randint(0,10)) + '.' + str(randint(0,10)) + '.' + str(randint(0,10))}
        print("Adding citation with version : " + kwargs["version"])
        import_cite(unique_id, software_name, **kwargs)

def test_decimal_version():
    print("Testing decimal version comparison")
    unique_id = "ver_test"
    software_name = "CiteSoft"
    for _ in range(1, 4):
        kwargs = {"version": str(randint(0,10)) + '.' + str(randint(0,10))}
        print("Adding citation with version : " + kwargs["version"])
        import_cite(unique_id, software_name, **kwargs)

def test_wrapper_func():
    print("Testing wrapper function")
    a = 5
    b = 12
    print("Adding %d and %d", a, b)
    unique_id = "add_test_with_function_call_cite"
    software_name = "CiteSoft_function_call_cite"
    @function_call_cite(unique_id, software_name)
    def func_cite_test_add(a1, b1):
        return a1 + b1
    
    res = func_cite_test_add(a, b)
    print("Result : %d", res)



if __name__ == '__main__':
    main()
