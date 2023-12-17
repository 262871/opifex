import pathlib

class gnu:
    """
    Manages configuration and (optionally async) calling of a gnu compiler.
    """
    def __init__(self, path, name, **kwargs):
        """
        Takes the file path to a gnu compiler and a toolchain name for file management and suffix.
        Raises AssertionError if path doesn't exist or if name contains spaces.
        """
        self.path = pathlib.Path(path)
        assert self.path.is_file(), f'gnu(). path must be a valid path to a file.\nUse a wrapper to search PATH and other dirs.\n{self.path.as_posix()} was not found.'
        self.name = name
        assert ' ' not in self.name, f'gnu(). name must not contain spaces.\nname was [{self.name}]'
        
        self.outasm = kwargs.get('stages', {'asm': False}).get('asm')
        self.outobj = kwargs.get('stages', {'obj': False}).get('obj')
        self.outfinal = kwargs.get('stages', {'final': True}).get('final')
        
        self.static = kwargs.get('static', True)
    
        self.includes = set()
        [self.addincludes(elem) for elem in kwargs.get('includes', [])]
        self.libpaths = set()
        [self.addlibpaths(elem) for elem in kwargs.get('libpaths', [])]
        self.libs = set()
        [self.addlibs(elem) for elem in kwargs.get('libraries', [])]
    
    def setstages(self, asm, obj, final):
        """
        Set which stages to intermit at and output during compilation. 
        kwargs: asm, obj, and final
        """
        self.outasm = asm
        self.outobj = obj
        self.outfinal = final
        return self
    
    def setstatic(self, isstatic):
        """
        Set whether to link statically or dynamically. Static by default to avoid missing libraries at runtime
        """
        self.static = isstatic
        return self
    
    def addincludes(self, *includes):
        """
        Adds each path-like entry in includes. Ignores duplicates (except for symlinc non-identity).
        Raises AssertionError if not a valid directory.
        """
        for include in includes:
            dir = pathlib.Path(include)
            assert dir.is_dir(), f'gnu.addincludes(). Each include in includes must be a valid directory.\n{dir.as_posix()} was not found.'
            self.includes.add(dir)
        return self

    def discardincludes(self, *includes):
        """
        Removes each path-like entry in includes.
        """
        for include in includes:
            self.includes.remove(pathlib.Path(include))
        return self
    
    def addlibpaths(self, *libpaths):
        """
        Adds each path-like entry in libpaths. Ignores duplicates (except for symlinc non-identity).
        Raises AssertionError if not a valid directory.
        """
        for libpath in libpaths:
            dir = pathlib.Path(libpath)
            assert dir.is_dir(), f'gnu.addlibpaths(). Each libpath in libpaths must be a valid directory.\n{dir.as_posix()} was not found.'
            self.libpaths.add(dir)
        return self
    
    def discardlibpaths(self, *libpaths):
        """
        Removes each path-like entry in libpaths.
        """
        for libpath in libpaths:
            self.libpaths.remove(pathlib.Path(libpath))
        return self
    
    def addlibs(self, *libnames):
        """
        Adds each string-like entry in libnames.
        Raises AssertionError if entry doesn't start with - or contains spaces.
        """
        for libname in libnames:
            assert ' ' not in libname, f'gnu.addlibs(). libnames must not contain spaces. libname was [{libname}].'
            self.libs.add(libname)
        return self
    
    def discardlibs(self, *libnames):
        """
        Removes each string-like entry in libnames.
        """
        for libname in libnames:
            self.libs.remove(libname)
        return self
    
