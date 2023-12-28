import pathlib
import pytest

from opifex import msvc


@pytest.fixture
def compiler():
    return msvc('C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat', 'msvc64')

def test_name(compiler: msvc):
    assert compiler.name == 'msvc64'

def test_path(compiler: msvc):
    assert compiler.path.as_posix() == 'C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvars64.bat'
    
def test_stages(compiler: msvc):
    assert compiler.outasm == False and compiler.outobj == False and compiler.outfinal == True
    compiler.setstages(True, True, False)
    assert compiler.outasm == True and compiler.outobj == True and compiler.outfinal == False

def test_static(compiler: msvc):
    assert compiler.static == True
    compiler.setstatic(False)
    assert compiler.static == False

def test_includes(compiler: msvc):
    compiler.addincludes('C:/src/VulkanSDK/Include', 'C:/src/volk')
    assert len(compiler.includes) == 2
    compiler.discardincludes('C:/src/volk')
    assert len(compiler.includes) == 1

def test_libpath(compiler: msvc):
    compiler.addlibpaths('c:/src/boost_1_82_0/libs')
    assert len(compiler.libpaths) == 1
    compiler.discardlibpaths('c:/src/boost_1_82_0/libs')
    assert len(compiler.libpaths) == 0

def test_defaultlibs(compiler: msvc):
    compiler.adddefaultlibs('User32')
    assert len(compiler.defaultlibs) == 1
    compiler.discarddefaultlibs('User32')
    assert len(compiler.defaultlibs) == 0

def test_nodefaultlibs(compiler: msvc):
    compiler.addnodefaultlibs('boost_1_82_0')
    assert len(compiler.nodefaultlibs) == 1
    compiler.discardnodefaultlibs('boost_1_82_0')
    assert len(compiler.nodefaultlibs) == 0

def test_opts(compiler: msvc):
    compiler.addopts('/O2')
    assert len(compiler.options) == 4
    compiler.discardopts('/options:strict')
    assert len(compiler.options) == 3

def test_safe():
    assert msvc.safe(pathlib.Path('/test path/with fwd-slash and spaces')) == '"\\test path\\with fwd-slash and spaces"'

@pytest.fixture
def files():
    return [pathlib.Path('test/mock/main.cpp'), pathlib.Path('test/mock/app.cxx')]

def test_asm_output_true(compiler: msvc, files):
    compiler.outasm = True
    asms, _ = compiler.asm_output(files)
    assert len(asms) == len(files)

def test_asm_output_false(compiler: msvc, files):
    compiler.outasm = False
    asms, _ = compiler.asm_output(files)
    assert not asms

def test_obj_output_false(compiler: msvc, files):
    compiler.outobj = False
    objs, _ = compiler.obj_output(files)
    assert not objs

def test_obj_output_true(compiler: msvc, files):
    compiler.outobj = True
    objs, _ = compiler.obj_output(files)
    assert len(objs) == len(files)

@pytest.fixture
def objs():
    return [pathlib.Path('mock/build/msvc64/main.obj'), pathlib.Path('mock/build/msvc64/app.obj')]

def test_final_output(compiler: msvc, objs):
    target, _ = compiler.final_output(objs)
    assert msvc.safe(target) == '"C:\\Users\\User\\Desktop\\python\\opifex\\build\\opifex_msvc64"'

def test_includes_command(compiler: msvc):
    compiler.includes = ['include1', 'include2']
    expected_command = ['/I"include1"', '/I"include2"']
    assert compiler.includes_command() == expected_command

def test_libpaths_command(compiler: msvc):
    compiler.libpaths = ['libpath1', 'libpath2']
    expected_command = ['/LIBPATH:"libpath1"', '/LIBPATH:"libpath2"']
    assert compiler.libpaths_command() == expected_command

def test_defaultlibs_command(compiler: msvc):
    compiler.defaultlibs = ['lib1', 'lib2']
    expected_command = ['/DEFAULTLIB:lib1', '/DEFAULTLIB:lib2']
    assert compiler.defaultlibs_command() == expected_command

def test_nodefaultlibs_command(compiler: msvc):
    compiler.nodefaultlibs = ['nodefaultlib1', 'nodefaultlib2']
    expected_command = ['/NODEFAULTLIB:nodefaultlib1', '/NODEFAULTLIB:nodefaultlib2']
    assert compiler.nodefaultlibs_command() == expected_command

def test_compile(compiler: msvc, files):
    compiler.setstages(True, True, True)
    result = compiler.compile(files)
    asms, objs, target, logs = result
    assert all(asms)
    assert all(objs)
    assert target is not None
    assert logs[0][0] == logs[1][0] == 0

@pytest.mark.asyncio
async def test_async_compile_kernel(compiler: msvc, files):
    compiler.name += 'a'
    compiler.target += 'a'
    compiler.setstages(True, True, True)
    result = await compiler.async_compile(files)
    asms, objs, target, logs = result
    assert all(asms)
    assert all(objs)
    assert target is not None
    assert logs[0][0] == logs[1][0] == 0
