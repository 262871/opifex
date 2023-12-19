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
