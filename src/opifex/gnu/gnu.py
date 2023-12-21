import asyncio
import os
import pathlib
import subprocess

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
        
        self.options = set()
        [self.addopts(elem) for elem in kwargs.get('options', {'-Wall', '-Wextra', '-pedantic', '-Werror'})]
        
        self.target = kwargs.get('target', pathlib.Path.cwd().absolute().stem.replace(' ', '_') + '_' + self.name)
        self.builddir = kwargs.get('builddir', pathlib.Path('build/').absolute())
    
    def compile_kernel(self, cmd, env=os.environ):
        """
        Executes compilation in a subprocess with the environment specified in env.
        """
        task = subprocess.run(cmd, env=env, capture_output=True, text=True)
        return (task.returncode, task.stdout, task.stderr)
    
    async def async_compile_kernel(self, cmd):
        task = await asyncio.create_subprocess_shell(cmd, stderr=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await task.communicate()
        return (task.returncode, stdout.decode(), stderr.decode())
    
    @staticmethod
    def safe(path):
        """
        Wrap the path in double quotes in case of spaces in path and use forward slashes. 
        """
        return f'"{path.as_posix()}"'
    
    def asm_command(self, cppfiles):
        """
        Creates a compiler command that stops at the asm output stage with input files, includes, target output, and options.
        returns pathlib paths to the future output file(s) and a list of command arguments.
        Raises AssertionError if cppfiles contains 0 elements.
        """
        assert len(cppfiles) != 0
        
        dir = self.builddir / self.name / 'asm'
        os.makedirs(dir, exist_ok=True)
        
        inputs = [gnu.safe(file) for file in cppfiles]
        asmfiles = [(dir / file.stem).with_suffix('.s') for file in cppfiles]
        outputs = ['-o'] + [gnu.safe(file) for file in asmfiles]
        
        includes = []
        if len(self.includes) != 0:
            includes += ['-I' + gnu.safe(include) for include in self.includes]
        
        options = list(self.options)
        
        return (asmfiles, [self.path.name, '-S'] + inputs + includes + outputs + options)
    
    def obj_command(self, files):
        """
        Creates a compiler command that stops at the obj output stage with input files, includes, target output, and options.
        returns pathlib paths to the future output file(s) and a list of command arguments.
        Raises AssertionError if files contains 0 elements.
        """
        assert len(files) != 0
        
        dir = self.builddir / self.name / 'obj'
        os.makedirs(dir, exist_ok=True)
        
        inputs = [gnu.safe(file) for file in files]
        objfiles = [(dir / file.stem).with_suffix('.obj') for file in files]
        outputs = ['-o'] + [gnu.safe(file) for file in objfiles]
        
        includes = []
        if len(self.includes) != 0 and not self.outasm:
            includes += ['-I' + gnu.safe(include) for include in self.includes]
        
        options = list(self.options)
        
        return (objfiles, [self.path.name, '-c'] + inputs + includes + outputs + options)

    def final_command(self, files):
        """
        Creates a compiler command with input files, includes, target output, options, libpaths, libs and the static option.
        returns pathlib paths to the future output file(s) and a list of command arguments.
        Raises AssertionError if files contains 0 elements.
        """
        assert len(files) != 0
        
        inputs = [gnu.safe(file) for file in files]
        outfile = self.builddir / self.target
        output = ['-o', gnu.safe(outfile)]
        
        includes = []
        if len(self.includes) != 0 and not (self.outasm or self.outobj):
            includes += ['-I' + gnu.safe(include) for include in self.includes]
        
        options = list(self.options)
        
        libpaths = []
        if len(self.libpaths) != 0:
            libpaths += ['-L' + gnu.safe(libpath) for libpath in self.libpaths]
        
        libs = []
        if len(self.libs) != 0:
            libs += ['-l' + lib for lib in self.libs]
        
        static = ['-static'] if self.static else []
        
        return (outfile, [self.path.name] + inputs + includes + output + options + libpaths + libs + static)
    
    def create_env(self):
        """
        Prepends the compilers parent directory to path on a copy of the systems environment variables.
        """
        env = os.environ 
        env['PATH'] = str(self.path.parent.resolve()) + os.pathsep + os.environ['PATH']
        return env
    
    def create_prefix(self):
        """
        Create a prefex to prepend to commands to set the e
        """
        return 'cd ' + gnu.safe(self.path.parent) + ' && '
    
    async def async_compile(self, files):
        """
        Run compiler concurrently, with internal configuration and files as input and return the path(s) to the output files in builddir.
        """
        os.makedirs(self.builddir, exist_ok=True)
        logs = []
        failed = False
        prefix = self.create_prefix()
        if self.outasm:
            files, command = self.asm_command(files)
            ret, stdout, stderr = await self.async_compile_kernel(prefix + ' '.join(command))
            failed = False if ret == 0 else True
            logs.append([ret, stdout, stderr])
        if self.outobj and not failed:
            files, command = self.obj_command(files)
            ret, stdout, stderr = await self.async_compile_kernel(prefix + ' '.join(command))
            failed = False if ret == 0 else True
            logs.append([ret, stdout, stderr])
        if self.outfinal and not failed:
            files, command = self.final_command(files)
            ret, stdout, stderr = await self.async_compile_kernel(prefix + ' '.join(command))
            logs.append([ret, stdout, stderr])
        return (files, logs)
    
    def compile(self, files):
        """
        Run compiler with internal configuration and files as input and return the path(s) to the output files in builddir.
        """
        os.makedirs(self.builddir, exist_ok=True)
        logs = []
        failed = False
        env = self.create_env()
        if self.outasm:
            files, command = self.asm_command(files)
            ret, stdout, stderr = self.compile_kernel(command, env)
            failed = False if ret == 0 else True
            logs.append([ret, stdout, stderr])
        if self.outobj and not failed:
            files, command = self.obj_command(files)
            ret, stdout, stderr = self.compile_kernel(command, env)
            failed = False if ret == 0 else True
            logs.append([ret, stdout, stderr])
        if self.outfinal and not failed:
            files, command = self.final_command(files)
            ret, stdout, stderr = self.compile_kernel(command, env)
            logs.append([ret, stdout, stderr])
        return (files, logs)
    
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
    
    def addopts(self, *options):
        """
        Adds each string-like entry in options.
        Raises AssertionError if entry doesn't start with - or contains spaces.
        """
        for option in options:
            assert option.startswith('-') and ' ' not in option, f'gnu.addopts(). options must start with a - and not contain spaces. option was [{option}].'
            self.options.add(option)
        return self
    
    def discardopts(self, *options):
        """
        Removes each string-like entry in options.
        """
        for option in options:
            self.options.remove(option)
        return self
