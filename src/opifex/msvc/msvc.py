import os
import pathlib
import subprocess

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
    
        self.includes = set()
        [self.addincludes(elem) for elem in kwargs.get('includes', [])]
        self.libpaths = set()
        [self.addlibpaths(elem) for elem in kwargs.get('libpaths', [])]
        self.defaultlibs = set()
        [self.adddefaultlibs(elem) for elem in kwargs.get('defaultlibs', [])]
        self.nodefaultlibs = set()
        [self.addnodefaultlibs(elem) for elem in kwargs.get('nodefaultlibs', [])]
        
        self.options = set()
        [self.addopts(elem) for elem in kwargs.get('options', {'/W4', '/EHsc', '/options:strict'})]
        
        self.target = kwargs.get('target', pathlib.Path.cwd().absolute().stem.replace(' ', '_') + '_' + self.name)
        self.builddir = kwargs.get('builddir', pathlib.Path('build/').absolute())
    
    @staticmethod
    def safe(path: pathlib.Path):
        """
        Wrap the path in double quotes in case of spaces in path and use double back-slashes as forward slashes are parsed as options.
        """
        return f'"{str(path)}"'
    
    def asm_output(self, files = []):
        """
        return a component command that instructs the compiler to output asm during compilation if self.outasm and creates a folder for them in builddir
        and optionally process the filepaths in files and return their corresponding targets in the new location
        """
        dir = self.builddir / self.name / 'asm'
        command = []
        asms = []
        if self.outasm:
            os.makedirs(dir, exist_ok=True)
            command = ['/Fa' + str(dir) + '\\']
            asms = [(dir / file.stem).with_suffix('.asm') for file in files]
        return asms, command
    
    def obj_output(self, files):
        """
        return a component command that instructs the compiler to output obj during compilation if self.outobj and creates a folder for them in builddir
        and process the filepaths in files and return their corresponding targets in the new location
        """
        dir = self.builddir / self.name / 'obj'
        command = []
        objs = []
        if self.outobj:
            os.makedirs(dir, exist_ok=True)
            command = ['/Fo' + str(self.builddir / self.name / 'obj') + '\\']
            objs = [(dir / file.stem).with_suffix('.obj') for file in files]
        return objs, command
    
    def final_output(self, objs):
        """
        return a component linker command that instructs the linker to name the output self.target in self.builddir
        """
        final = self.builddir / self.target
        os.makedirs(self.builddir, exist_ok=True)
        static = ['/DEFAULTLIB:LIBCMT', '/NODEFAULTLIB:MSVCRT'] if self.static else []
        command = ['/OUT:' + str(final) + '.exe'] + static + objs
        return final, command
    
    def includes_command(self):
        """
        return a component command that contains all the includes in self.includes
        """
        return ['/I' + msvc.safe(include) for include in self.includes]
    
    def libpaths_command(self):
        """
        return a component linker command that contains all the libpaths in self.libpaths
        """
        return ['/LIBPATH:' + msvc.safe(libpath) for libpath in self.libpaths]
    
    def defaultlibs_command(self):
        """
        return a component linker command that contains all the defaultlibs in self.defaultlibs
        """
        return ['/DEFAULTLIB:' + defaultlib for defaultlib in self.defaultlibs]
    
    def nodefaultlibs_command(self):
        """
        return a component linker command that contains all the nodefaultlibs in self.nodefaultlibs
        """
        return ['/NODEFAULTLIB:' + nodefaultlib for nodefaultlib in self.nodefaultlibs]
    
    def compile_kernel(self, cmd):
        batprefix = [self.path.resolve(), '&&', 'cl']
        task = subprocess.run(batprefix + cmd, capture_output=True, text=True)
        return (task.returncode, task.stdout, task.stderr)
    
    def link_kernel(self, cmd):
        batprefix = [self.path.resolve(), '&&', 'link']
        task = subprocess.run(batprefix + cmd, capture_output=True, text=True)
        return (task.returncode, task.stdout, task.stderr)
    
    def compile(self, files):
        """
        Run compiler and linker with internal configuration and files as input and return the path(s) to the output files in builddir.
        """
        asms, fa = self.asm_output(files)
        objs, fo = self.obj_output(files)
        includes = self.includes_command()
        options = [self.options]
        
        ret, stdout, stderr = self.compile_kernel(fa + fo + includes + options + files)
        logs = [[ret, stdout, stderr]]
        if self.outfinal:
            target, fe = self.final_output(objs)
            libpaths = self.libpaths_command()
            defaultlibs = self.defaultlibs_command()
            nodefaultlibs = self.nodefaultlibs_command()
            ret, stdout, stderr = self.link_kernel(fe + libpaths + defaultlibs + nodefaultlibs)
            logs += [ret, stdout, stderr]
        
        return (asms, objs, target, logs)
    
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
    
    def adddefaultlibs(self, *libnames):
        """
        Adds each string-like entry in libnames.
        Raises AssertionError if entry doesn't start with - or contains spaces.
        """
        for libname in libnames:
            assert ' ' not in libname, f'gnu.addlibs(). libnames must not contain spaces. libname was [{libname}].'
            self.defaultlibs.add(libname)
        return self
    
    def discarddefaultlibs(self, *libnames):
        """
        Removes each string-like entry in libnames.
        """
        for libname in libnames:
            self.defaultlibs.remove(libname)
        return self
    
    def addnodefaultlibs(self, *libnames):
        """
        Adds each string-like entry in libnames.
        Raises AssertionError if entry doesn't start with - or contains spaces.
        """
        for libname in libnames:
            assert ' ' not in libname, f'gnu.addlibs(). libnames must not contain spaces. libname was [{libname}].'
            self.nodefaultlibs.add(libname)
        return self
    
    def discardnodefaultlibs(self, *libnames):
        """
        Removes each string-like entry in libnames.
        """
        for libname in libnames:
            self.nodefaultlibs.remove(libname)
        return self
    
    def addopts(self, *options):
        """
        Adds each string-like entry in options.
        Raises AssertionError if entry doesn't start with / or contains spaces.
        """
        for option in options:
            assert option.startswith('/') and ' ' not in option, f'gnu.addopts(). options must start with a / and not contain spaces. option was [{option}].'
            self.options.add(option)
        return self
    
    def discardopts(self, *options):
        """
        Removes each string-like entry in options.
        """
        for option in options:
            self.options.remove(option)
        return self

