from setuptools import setup, find_packages

setup(
    name='asm_to_bin_hex',
    version='0.1.0',
    description='Assembler RISC-V: de .asm a .bin y .hex',
    author='Tu Nombre',
    author_email='tuemail@example.com',
    packages=find_packages(),  # buscará automáticamente asm_to_bin_hex
    python_requires='>=3.7',
    install_requires=[
        'sly',  # lexer y parser
    ],
    entry_points={
        'console_scripts': [
            # esto crea un comando en consola:
            'assembler=assembler.main:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
