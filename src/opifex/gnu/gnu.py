import pathlib

class gnu:
    """
    Manages configuration and (optionally async) calling of a gnu compiler.
    """
    def __init__(self, path, name, **kwargs):
        """
        Takes the file path to a gnu compiler and a toolchain name for file management.
        Raises AssertionError if path doesn't exist.
        """
        self.path = pathlib.Path(path)
        assert self.path.is_file(), f'gnu(). path must be a valid path to a file.\nUse a wrapper to search PATH and other dirs.\n{self.path.as_posix()} was not found.'
        self.name = name
        assert ' ' not in self.name, f'gnu(). name must not contain spaces.\nname was [{self.name}]'
    
        self.includes = set()
        [self.addincludes(elem) for elem in kwargs.get('includes', [])]
    
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
