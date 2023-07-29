import zipfile
import pathlib
import shutil

import pytest

import maxutils

FIXTURE_DIR = pathlib.Path('fixtures')

def remove_detritus(fixture_dir):
    detritus = fixture_dir / '__MACOSX'
    if detritus.exists():
        shutil.rmtree(detritus)

@pytest.fixture
def standalone():
    with zipfile.ZipFile(FIXTURE_DIR / 's4.zip', 'r') as zip_ref:
        zip_ref.extractall(FIXTURE_DIR)
    _standalone = FIXTURE_DIR / 's4.app'
    yield _standalone
    shutil.rmtree(_standalone)
    remove_detritus(FIXTURE_DIR)

@pytest.fixture
def max_standalone(standalone):
    yield maxutils.MaxStandalone(standalone, '0.0.1')

@pytest.fixture
def external():
    with zipfile.ZipFile(FIXTURE_DIR / 'csound~.mxo.zip', 'r') as zip_ref:
        zip_ref.extractall(FIXTURE_DIR)
    _external = FIXTURE_DIR / 'csound~.mxo'
    yield _external
    shutil.rmtree(_external)
    remove_detritus(FIXTURE_DIR)

@pytest.fixture
def max_external(external):
    yield maxutils.MaxExternal(external, '0.0.1')

@pytest.fixture
def package():
    with zipfile.ZipFile(FIXTURE_DIR / 'karma.zip', 'r') as zip_ref:
        zip_ref.extractall(FIXTURE_DIR)
    _package = FIXTURE_DIR / 'karma'
    yield _package
    shutil.rmtree(_package)
    remove_detritus(FIXTURE_DIR)

@pytest.fixture
def max_package(package):
    yield maxutils.MaxPackage(package, '0.0.1')

def test_max_standalone_init(max_standalone):
    s = max_standalone
    assert s.name == 's4'
    assert s.version == '0.0.1'


def test_max_external_init(max_external):
    e = max_external
    assert e.name == 'csound~'
    assert e.version == '0.0.1'

def test_max_package_init(max_package):
    p = max_package
    assert p.name == 'karma'
    assert p.version == '0.0.1'

def test_max_standalone_manager(max_standalone):
    m = maxutils.MaxStandaloneManager(max_standalone)
    assert m.product

def test_max_package_manager(max_package):
    m = maxutils.MaxPackageManager(max_package)
    assert m.product

def test_max_external_manager(max_external):
    m = maxutils.MaxExternalManager(max_external)
    assert m.product

def test_max_release_manager_with_standalone(standalone):
    m = maxutils.MaxReleaseManager(standalone)
    assert m.product
    assert isinstance(m.manager, maxutils.MaxStandaloneManager)
    assert m.manager.product

def test_max_release_manager_with_package(package):
    m = maxutils.MaxReleaseManager(package)
    assert m.product
    assert isinstance(m.manager, maxutils.MaxPackageManager)
    assert m.manager.product

def test_max_release_manager_with_external(external):
    m = maxutils.MaxReleaseManager(external)
    assert m.product
    assert isinstance(m.manager, maxutils.MaxExternalManager)
    assert m.manager.product

def test_max_release_manager_with_standalone_sign(standalone):
    m = maxutils.MaxReleaseManager(standalone)
    m.sign()

def test_max_release_manager_with_package_sign(package):
    m = maxutils.MaxReleaseManager(package)
    m.sign()

def test_max_release_manager_with_external_sign(external):
    m = maxutils.MaxReleaseManager(external)
    m.sign()
