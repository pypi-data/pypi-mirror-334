from IPython import get_ipython
import re
import sys
import importlib
import pkg_resources
import pandas as pd
import numpy as np


class libraryfinder():

    default_libary=["keras","torch","tensorflow","transformers","sklearn",'scikit-learn']
    unwanted_lib=['__builtin__', '__builtins__','sys','importlib','re', 'pkg_resources']# List of unwanted libraries
    short_lib_data=pd.DataFrame()
    short_lib_data["library"]=['Pillow','opencv-python','numpy','pandas','matplotlib','seaborn','tensorflow','torch','scikit-learn','scipy',
        're','json','os','sys','requests','beautifulsoup4','xml.etree.ElementTree','gzip','sqlite3','pickle','datetime','math','statistics',
        'collections']
    short_lib_data["Short Form"]=['PIL','cv2','np','pd','plt','sns','tf','torch','sklearn','sp','re','json','os','sys','requests','bs4','xml',
        'gzip','sqlite3','pickle','datetime','math','statistics','collections']

    def __init__(self):
      self.library_names=None
      self.Library_name=None
      self.Library_versions=None

    def libname_get_cell_1(self):    
        library_names2=[]
        for var_name, value in globals().items():
            if isinstance(value, type(np)):  # Adjust as needed
                #print(f"{var_name}: {value}")
                # Regular expression to extract the module name and path
                match = re.search(r"<module '([^']+)' from '([^']+)'>",str(value))

                if match:
                    module_name = match.group(1)  # The module name (e.g., pandas)
                    module_name2 = module_name.split('.')[0]
                    module_path = match.group(2)  # The module path
                    if module_name2 not in library_names2:
                        library_names2.append(module_name2)
                    #print(f"Module Name: {module_name}")
                    #print(f"Module Path: {module_path}")

        for i in library_names2:
          if i in self.unwanted_lib:
            library_names2.remove(i)
        
        return library_names2

    def libname_get_cell_2(self):

        # Set to store unique module names
        imported_modules = set()

        # Regex pattern to match import statements
        import_pattern = re.compile(r'^\s*(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', re.MULTILINE)
        
        # Get the current IPython instance
        ipython = get_ipython()
        
        if ipython is not None:
            # Get the input history
            history = ipython.history_manager.get_range()  

            # Check each input cell for import statements
            for entry in history:
                # Ensure that each entry is valid and contains an input string at the expected position
                if len(entry) > 2:
                    input_str = entry[2]
    
                    # Search for import statements in the input string
                    matches = import_pattern.findall(input_str)
    
                    for module in matches:
                        # Only add the base module name to avoid duplicates from submodules
                        base_module = module.split('.')[0]
                        imported_modules.add(base_module)
    
            # Display the imported modules
            #print("Imported Modules in this Notebook:")
            for module in sorted(imported_modules):
              if module in self.unwanted_lib:
                imported_modules.remove(module)
            #print(list(imported_modules))
        else:
            pass

        return list(imported_modules)





    def get_lib_name(self,import_texts=None,history=True):
        self.library_names=[]

        if import_texts is not None:
          # Extract base library names only
          self.library_names = re.findall(r'^(?:import|from) (\w+)', import_texts, re.MULTILINE)

          if history==True:
            self.library_names.extend(self.libname_get_cell_2())
            self.library_names=list(set(self.library_names))
            self.library_names.extend(self.libname_get_cell_1())
          else:
            self.library_names=list(set(self.library_names))
            self.library_names.extend(self.libname_get_cell_1())
          
        else:
          if history==True:
            self.library_names.extend(self.libname_get_cell_2())
            self.library_names=list(set(self.library_names))
            self.library_names.extend(self.libname_get_cell_1())
          else:
            self.library_names=list(set(self.library_names))
            self.library_names.extend(self.libname_get_cell_1())

        self.library_names.extend(self.default_libary)
        # Remove duplicates (optional)
        self.library_names = list(set(self.library_names))

        return self.library_names


    def get_lib_version(self,import_texts=None,history=True):#get_lib_version
        # Initialize lists to store library names and versions
        Library=[]
        versions=[]
        not_installed=[]
        not_available=[]


        library_names=[]
        if import_texts is None:
          library_names=self.get_lib_name(import_texts=None,history=history)
        else:
          library_names=self.get_lib_name(import_texts=import_texts,history=history)

        # Display extracted library names and versions
        for library in library_names:
            try:
                # Dynamically import the library
                imported_lib = importlib.import_module(library)
                # Get the version using pkg_resources
                version = pkg_resources.get_distribution(library).version
                cleaned_version = re.sub(r'\+.*', '', version)
                Library.append(library)
                versions.append(cleaned_version)

                # Print the library name and version
                #print(f"{library} version: {version}")

            except ImportError:
                #print(f"Library {library} is not installed.")
                not_installed.append(library)

            except pkg_resources.DistributionNotFound:
                not_available.append(library)
                #print(f"Version information for {library} is not available.")

            except Exception as e:
               pass
                #print(f"An error occurred {library}: {e}")


            try:
                if library not in Library:
                  module = __import__(library)
                  # Get the version
                  version = getattr(module, '__version__','No version attribute available')
                  cleaned_version = re.sub(r'\+.*', '', version)
                  if version=='No version attribute available':
                    not_available.append(library)
                  else:
                    Library.append(library)
                    versions.append(cleaned_version)
                else:pass

            except Exception as e:
                pass
                #print(f"An error occurred {library}: {e}")

        self.Library_name=[]
        self.Library_versions=[]

        print("library and versions : " )
        for lib,ver in zip(Library,versions):

          if lib in list(self.short_lib_data["Short Form"]):
            #print(list(short_lib_data["Short Form"]).index(lib))
            lib =self.short_lib_data.at[list(self.short_lib_data["Short Form"]).index(lib),"library"]

          self.Library_name.append(lib)
          self.Library_versions.append(ver)

          print(f"{lib}=={ver}")


        print("\npython version :",sys.version)
        print("\nNot_installed :",set(not_installed)-set(Library))
        print("\nNot_available version:",set(not_available)-set(Library))


        import_lib=[]
        import_ver=[]

        default_lib=[]
        default_ver=[]

        for lib,ver in zip(self.Library_name,self.Library_versions):
          if lib in self.default_libary:
            default_lib.append(lib)
            default_ver.append(ver)
          else:
            import_lib.append(lib)
            import_ver.append(ver)

        return {"Default_library_name":default_lib,"Default_library_version":default_ver,"imported_library_name":import_lib,"imported_library_version":import_ver,"system_version ":sys.version,"Not_installed":set(not_installed)-set(Library),"Not_available_version":set(not_available)-set(Library)}


    def to_txt(self,file_path):
      self.file_path=file_path
      #Run the get_lib_version
      try:
        if self.Library_name is None:
          x=self.get_lib_version()
        else:
          pass
        #create the dictionary
        data=dict(zip(self.Library_name,self.Library_versions))

        #verifythe file path
        if file_path[-4:]!=".txt":
          file_path=file_path+".txt"

        # Write data to the file
        with open(file_path, "w") as file:
            for key, values in data.items():
                file.write(f"{key}=={str(values)}\n")

        print(f"{file_path} file was saved.")

      except TypeError as e:
        print(f"An error occurred: {e}")



#################################################################################################################

default_libary=["keras","torch","tensorflow","transformers","sklearn",'scikit-learn']
unwanted_lib=['__builtin__', '__builtins__','sys','importlib','re', 'pkg_resources']# List of unwanted libraries
short_lib_data=pd.DataFrame()
short_lib_data["library"]=['Pillow','opencv-python','numpy','pandas','matplotlib','seaborn','tensorflow','torch','scikit-learn','scipy',
        're','json','os','sys','requests','beautifulsoup4','xml.etree.ElementTree','gzip','sqlite3','pickle','datetime','math','statistics',
        'collections']
short_lib_data["Short Form"]=['PIL','cv2','np','pd','plt','sns','tf','torch','sklearn','sp','re','json','os','sys','requests','bs4','xml',
        'gzip','sqlite3','pickle','datetime','math','statistics','collections']


def libname_get_cell_1():    
    library_names2=[]
    for var_name, value in globals().items():
        if isinstance(value, type(np)):  # Adjust as needed
            #print(f"{var_name}: {value}")
            # Regular expression to extract the module name and path
            match = re.search(r"<module '([^']+)' from '([^']+)'>",str(value))

            if match:
                module_name = match.group(1)  # The module name (e.g., pandas)
                module_name2 = module_name.split('.')[0]
                module_path = match.group(2)  # The module path
                if module_name2 not in library_names2:
                    library_names2.append(module_name2)
                #print(f"Module Name: {module_name}")
                #print(f"Module Path: {module_path}")

    for i in library_names2:
      if i in unwanted_lib:
        library_names2.remove(i)
    
    return library_names2

def libname_get_cell_2():
    # Set to store unique module names
    imported_modules = set()

    
    # Regex pattern to match import statements
    import_pattern = re.compile(r'^\s*(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', re.MULTILINE)
    
    # Get the current IPython instance
    ipython = get_ipython()

    if ipython is not None:
        
        # Get the input history
        history = ipython.history_manager.get_range()  # Get all input cells
        
        # Check each input cell for import statements
        for entry in history:
            # Ensure that each entry is valid and contains an input string at the expected position
            if len(entry) > 2:
                input_str = entry[2]
    
                # Search for import statements in the input string
                matches = import_pattern.findall(input_str)
    
                for module in matches:
                    # Only add the base module name to avoid duplicates from submodules
                    base_module = module.split('.')[0]
                    imported_modules.add(base_module)
    
        # Display the imported modules
        #print("Imported Modules in this Notebook:")
        for module in sorted(imported_modules):
          if module in unwanted_lib:
            imported_modules.remove(module)
        #print(list(imported_modules))
    else:
        pass

    return list(imported_modules)





def get_lib_name(import_texts=None,history=True):
    
    library_names=[]

    if import_texts is not None:
      # Extract base library names only
      library_names = re.findall(r'^(?:import|from) (\w+)', import_texts, re.MULTILINE)

      if history==True:
        library_names.extend(libname_get_cell_2())
        library_names=list(set(library_names))
        library_names.extend(libname_get_cell_1())
      else:
        library_names=list(set(library_names))
        library_names.extend(libname_get_cell_1())

    else:
      if history==True:
        library_names.extend(libname_get_cell_2())
        library_names=list(set(library_names))
        library_names.extend(libname_get_cell_1())
      else:
        library_names=list(set(library_names))
        library_names.extend(libname_get_cell_1())

    library_names.extend(default_libary)
    # Remove duplicates (optional)
    library_names = list(set(library_names))

    return library_names


def get_lib_version(import_texts=None,history=True,file_path=None):
    # Initialize lists to store library names and versions
    Library=[]
    versions=[]
    not_installed=[]
    not_available=[]


    library_names=[]


    if import_texts is None:
      library_names=get_lib_name(import_texts=None,history=history)
    else:
      library_names=get_lib_name(import_texts=import_texts,history=history)

    # Display extracted library names and versions
    for library in library_names:
        try:
            # Dynamically import the library
            imported_lib = importlib.import_module(library)
            # Get the version using pkg_resources
            version = pkg_resources.get_distribution(library).version
            cleaned_version = re.sub(r'\+.*', '', version)
            Library.append(library)
            versions.append(cleaned_version)

            # Print the library name and version
            #print(f"{library} version: {version}")

        except ImportError:
            #print(f"Library {library} is not installed.")
            not_installed.append(library)

        except pkg_resources.DistributionNotFound:
            not_available.append(library)
            #print(f"Version information for {library} is not available.")

        except Exception as e:
           pass
            #print(f"An error occurred {library}: {e}")


        try:
            if library not in Library:
              module = __import__(library)
              # Get the version
              version = getattr(module, '__version__','No version attribute available')
              cleaned_version = re.sub(r'\+.*', '', version)
              if version=='No version attribute available':
                not_available.append(library)
              else:
                Library.append(library)
                versions.append(cleaned_version)
            else:pass

        except Exception as e:
            pass
            #print(f"An error occurred {library}: {e}")

    Library_name=[]
    Library_versions=[]

    print("library and versions : " )
    for lib,ver in zip(Library,versions):

      if lib in list(short_lib_data["Short Form"]):
        #print(list(short_lib_data["Short Form"]).index(lib))
        lib =short_lib_data.at[list(short_lib_data["Short Form"]).index(lib),"library"]

      Library_name.append(lib)
      Library_versions.append(ver)

      print(f"{lib}=={ver}")


    print("\npython version :",sys.version)
    print("\nNot_installed :",set(not_installed)-set(Library))
    print("\nNot_available version:",set(not_available)-set(Library))


    import_lib=[]
    import_ver=[]

    default_lib=[]
    default_ver=[]

    for lib,ver in zip(Library_name,Library_versions):
      if lib in default_libary:
        default_lib.append(lib)
        default_ver.append(ver)
      else:
        import_lib.append(lib)
        import_ver.append(ver)


    def to_txt(file_path):
      file_path
      #Run the get_lib_version
      try:
        #create the dictionary
        data=dict(zip(Library_name,Library_versions))

        #verifythe file path
        if file_path[-4:]!=".txt":
          file_path=file_path+".txt"

        # Write data to the file
        with open(file_path, "w") as file:
            for key, values in data.items():
                file.write(f"{key}=={str(values)}\n")

        print(f"{file_path} file was saved.")

      except TypeError as e:
        print(f"An error occurred: {e}")


    if file_path is None:
      to_txt(file_path="new_requirements.txt")
    else:
      to_txt(file_path=file_path)

    return {"Default_library_name":default_lib,"Default_library_version":default_ver,"imported_library_name":import_lib,"imported_library_version":import_ver,"system_version ":sys.version,"Not_installed":set(not_installed)-set(Library),"Not_available_version":set(not_available)-set(Library)}
       
