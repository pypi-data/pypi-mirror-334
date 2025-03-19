python3 = import('python').find_installation('python3', required: false)

if not python3.found()
    warning('Python bindings are disabled because Python 3 could not be found')
else
    custom_target('usbbluetooth_python',
        build_by_default: false,
        install: false,
        command: [python3, '-m', 'build', meson.current_source_dir(), '-o', meson.current_build_dir()],
        output: ['usbbluetooth-'+meson.project_version()+'.tar.gz', 'usbbluetooth-'+meson.project_version()+'-py3-none-any.whl'])
endif
