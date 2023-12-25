import pathlib 
import pytest

from opifex import gnu 


@pytest.fixture
def compiler():
    return gnu('c:/msys64/mingw64/bin/g++.exe', 'mingw64')

def test_name(compiler: gnu):
    assert compiler.name == 'mingw64'

def test_path(compiler: gnu):
    assert compiler.path.as_posix() == 'c:/msys64/mingw64/bin/g++.exe'

def test_stages(compiler: gnu):
    assert compiler.outasm == False and compiler.outobj == False and compiler.outfinal == True
    compiler.setstages(True, True, False)
    assert compiler.outasm == True and compiler.outobj == True and compiler.outfinal == False

def test_static(compiler: gnu):
    assert compiler.static == True
    compiler.setstatic(False)
    assert compiler.static == False

def test_includes(compiler: gnu):
    compiler.addincludes('C:/src/VulkanSDK/Include', 'C:/src/volk')
    assert len(compiler.includes) == 2
    compiler.discardincludes('C:/src/volk')
    assert len(compiler.includes) == 1

def test_libpath(compiler: gnu):
    compiler.addlibpaths('c:/src/boost_1_82_0/libs')
    assert len(compiler.libpaths) == 1
    compiler.discardlibpaths('c:/src/boost_1_82_0/libs')
    assert len(compiler.libpaths) == 0

def test_libs(compiler: gnu):
    compiler.addlibs('boost_1_82_0')
    assert len(compiler.libs) == 1
    compiler.discardlibs('boost_1_82_0')
    assert len(compiler.libs) == 0

def test_opts(compiler: gnu):
    compiler.addopts('-O3')
    assert len(compiler.options) == 5
    compiler.discardopts('-pedantic')
    assert len(compiler.options) == 4

@pytest.fixture
def files():
    return [pathlib.Path('test/mock/main.cpp'), pathlib.Path('test/mock/app.cxx')]

def test_compile(compiler: gnu, files):
    compiler.setstages(True, False, False)
    executable, logs = compiler.compile(files)
    assert executable
    assert len(logs) == 3
    compiler.setstages(True, True, True)
    executable, logs = compiler.compile(files)
    assert executable
    assert len(logs) == 3

@pytest.mark.asyncio
async def test_async_compile(compiler: gnu, files):
    compiler.setstages(True, False, False)
    executable, logs = await compiler.async_compile(files)
    assert executable
    assert len(logs) == 3
    compiler.setstages(True, True, True)
    executable, logs = await compiler.async_compile(files)
    assert executable
    assert len(logs) == 3

def test_safe():
    assert gnu.safe(pathlib.Path('\\test path\\with backslash and spaces')) == '"/test path/with backslash and spaces"'
    
def test_asm_command(compiler: gnu, files):
    compiler.addincludes('test/mock/include')
    asm_files, command = compiler.asm_command(files[0])
    assert len(command) == 10

def test_obj_command(compiler: gnu, files):
    compiler.addincludes('test/mock/include')
    obj_files, command = compiler.obj_command(files[0])
    assert len(command) == 10

def test_final_command(compiler: gnu, files):
    compiler.addincludes('test/mock/include')
    compiler.addlibpaths('test/mock/lib')
    compiler.addlibs('mocklib')
    file, command = compiler.final_command(files)
    assert len(command) == 13
    assert file.resolve() == pathlib.Path('build/opifex_mingw64').resolve()

def test_compile_kernel(compiler: gnu):
    code, stdout, stderr = compiler.compile_kernel(['g++.exe'])
    assert code == 1
    assert stdout == ''
    assert stderr == 'g++.exe: fatal error: no input files\ncompilation terminated.\n'

@pytest.mark.asyncio
async def test_async_compile_kernel(compiler: gnu):
    code, stdout, stderr = await compiler.async_compile_kernel('c:/msys64/mingw64/bin/g++.exe')
    assert code == 1
    assert stdout == ''
    assert stderr == 'g++.exe: fatal error: no input files\ncompilation terminated.\r\n'

def test_create_env(compiler: gnu):
    env = compiler.create_env()
    assert env['Path'].startswith('C:\\msys64\\mingw64\\bin;')

def test_create_prefix(compiler: gnu):
    assert compiler.create_prefix() == 'cd "c:/msys64/mingw64/bin" && '
