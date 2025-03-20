[![Publish Python distributions to PyPI and TestPyPI](https://github.com/KaushiML3/libfinder/actions/workflows/python-publish.yml/badge.svg)](https://github.com/KaushiML3/libfinder/actions/workflows/python-publish.yml)

# libfinder

`libfinder` is a simple Python package that helps check if a library is installed in your python jupyter environment.

## 📌 Installation

Clone the repository and install:

```bash
git clone https://github.com/KaushiML3/libfinder
cd libfinder
pip install .

```

## Uses

common step
 ```bash
  pip install libfinder
```

1. Call the functions
   ```python
     import libfinder
   ```

    1. Get the module names
        ```python
          lib_name=libfinder.get_lib_name() **or** libfinder.get_lib_name()
          print(lib_name)
        ```

    2. Get the module versions and save the new_requirements.txt file
        ```python
          lib_ver=libfinder.get_lib_ver() **or** libfinder.get_lib_ver()
          print(lib_ver)
        ```

3. Use libfinder class  
     ```python
      import libfinder
      ```

    1. Create object
       ```python
         lib=libfinder.libraryfinder()
       ```

    3. Get the module names
        ```python
          lib.get_lib_name()
        ```

    4. Get the module versions
         ```python
          lib.get_lib_ver()
         ```

    5. Get the .txt file 
        ```python
          lib.to_txt("new_requirements.txt")
        ```

4. params
   
     ![image](https://github.com/KaushiML3/libfinder/blob/main/img/Screenshot%20(82).png)







