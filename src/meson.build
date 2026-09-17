pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()

install_subdir(
  'tvweb',
  install_dir: pkgdatadir,
  exclude_directories: ['__pycache__'],
)

conf = configuration_data()
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'tvweb.in',
  output: 'tvweb',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x',
)
