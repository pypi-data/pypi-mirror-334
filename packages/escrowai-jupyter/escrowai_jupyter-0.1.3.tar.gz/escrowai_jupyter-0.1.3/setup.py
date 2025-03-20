from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

setup(
    name="escrowai-jupyter",
    version="0.1.3",
    description="A Jupyter extension that encrypts and uploads the working directory to EscrowAI.",
    author="Jacob Blum",
    author_email="jake.blum@beekeeperai.com",
    license="BSD-3-Clause",
    packages=find_packages(),
    install_requires=[
        "jupyterlab>=4.0.0,<5",
        "jupyter_server>=1.6",  # Ensure compatibility with Jupyter Server
        "jupyter-server-proxy>=4.0.0",  # Required for the extension to run via proxy
    ],
    zip_safe=False,

    # Include JavaScript assets for JupyterLab
    include_package_data=True,

    entry_points={
        "jupyter_serverproxy_servers": [
            "escrowai-jupyter = escrowai_jupyter:jupyter_serverproxy_servers"
        ]
    },

    # JupyterLab extension configuration
    classifiers=[
        "Framework :: Jupyter",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ],

    # Include JupyterLab extension in the package
    cmdclass={"build_py": build_py}
)