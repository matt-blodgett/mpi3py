import os
import time
import shutil
import subprocess


project_name = 'mpi3pc'
project_icon = 'rsrc/gui/mario.ico'
project_dependencies = [
    'six',
    'wmi',
    'pillow',
    'mutagen',
    'pydub',
    'pytube',
    'pyaudio',
    'pypiwin32',
    'pyinstaller'
]


def pip_depends(install):
    piparg = install
    for depend in project_dependencies:
        print('-------------------------')
        print()
        proc = ['pip', piparg, depend]
        if piparg == 'uninstall':
            proc.append('-y')
        subprocess.call(proc)
        print()


def freeze():
    print('-------------------------')
    print()

    print('Remove pre-existing dist path')
    shutil.rmtree('dist', ignore_errors=True)
    time.sleep(1)

    freeze_temp = 'freezetemp'
    freeze_args = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--workpath',
        freeze_temp,
        '--name',
        project_name,
        '--icon',
        project_icon,
        'pcmain.py']

    print('Invoking pyinstaller:')
    print(' '.join(freeze_args))

    print()
    print('-------------------------')
    time.sleep(2)
    print()

    subprocess.call(freeze_args)

    print()
    print('-------------------------')
    time.sleep(1)
    print()

    print('Cleaning pyinstaller files:')
    print('Remove file: temp')
    shutil.rmtree(freeze_temp, ignore_errors=True)
    print('Remove file: __pycache__')
    shutil.rmtree('__pycache__', ignore_errors=True)
    print('Remove file: .spec')
    try: os.remove('{}{}'.format(project_name, '.spec'))
    except FileNotFoundError: pass
    print('Adding project resources: dist/rsrc')
    shutil.copytree('rsrc', 'dist/rsrc')

    print()
    print('-------------------------')
    time.sleep(1)
    print()

def main():
    os.system('title Project Build Tool')
    print()
    print('-------------------------')
    print('Project Build Tool')
    print('-------------------------')
    print()
    print('Options:')
    print('1: Freeze Project')
    print('2: Install Dependencies')
    print('3: Uninstall Dependencies')
    print()
    option = input('Option: ')
    print()
    print('-------------------------')

    if option == '1':
        print('Freezing Project')
        freeze()

    elif option == '2':
        print('Installing Dependencies')
        pip_depends('install')

    elif option == '3':
        print('Uninstalling Dependencies')
        pip_depends('uninstall')

    if option in ['1', '2', '3']:
        print('-------------------------')
        print('Option Process Completed')
        print('-------------------------')
        print()
        input()

if __name__ == '__main__': main()

######################################################################
