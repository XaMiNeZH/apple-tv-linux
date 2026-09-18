project(
  'tvweb',
  version: '0.3.0',
  meson_version: '>= 1.1.0',
  default_options: [
    'prefix=/usr',
  ],
)

pymod = import('python')
python = pymod.find_installation('python3', required: true)

subdir('data')
subdir('src')

install_subdir(
  'app',
  install_dir: get_option('prefix') / get_option('datadir') / meson.project_name(),
)
