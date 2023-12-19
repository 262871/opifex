import pathlib 

class msvc:
    """
    Manages configuration and (optionally async) calling of a msvc compiler.
    """
    def __init__(self, path, name, **kwargs):
        """
        Takes the file path to microsofts vcvars64.bat and a toolchain name for file management and suffix.
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
