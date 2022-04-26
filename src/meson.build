pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'gtk4_css_shadow')
gnome = import('gnome')

gnome.compile_resources('gtk4_css_shadow',
  'gtk4_css_shadow.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'gtk4_css_shadow.in',
  output: 'gtk4_css_shadow',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

gtk4_css_shadow_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(gtk4_css_shadow_sources, install_dir: moduledir)
