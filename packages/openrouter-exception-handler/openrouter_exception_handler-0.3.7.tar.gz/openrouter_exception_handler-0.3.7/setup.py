from setuptools import setup, find_packages

setup(
    name='openrouter_exception_handler',
    packages=find_packages(),  # ✅ Ahora encuentra el paquete correctamente
    package_dir={'': 'openrouter_exception_handler/openrouter_exception_handler/'},  # ✅ Mapea el paquete a la carpeta `src`
    install_requires=['requests'],
    include_package_data=True,

)
