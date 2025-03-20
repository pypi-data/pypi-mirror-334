from setuptools import setup, find_packages

setup(
    name='openrouter_exception_handler',
    version='0.2.9',
    packages=find_packages(where='src'),  # ✅ Ahora encuentra el paquete correctamente
    package_dir={'': 'src'},  # ✅ Mapea el paquete a la carpeta `src`
    install_requires=['requests'],
)
