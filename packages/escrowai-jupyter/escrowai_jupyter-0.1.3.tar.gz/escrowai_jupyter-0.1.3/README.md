# escrowai_jupyter

[![Github Actions Status](https://github.com/BeeKeeperAI/escrowai-jupyter/workflows/Build/badge.svg)](https://github.com/BeeKeeperAI/escrowai-jupyter/actions/workflows/build.yml)
An extension to encrypt and upload the working directory to EscrowAI

## Requirements

- JupyterLab >= 4.0.0

## Install

To install the extension, execute:

```bash
pip install escrowai_jupyter
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall escrowai_jupyter
```

## Usage

To use the package, the following prerequisites must be met:

1. Working directory must be the algorithm to be uploaded to EscrowAI.

```bash
cd {algorithm_directory}
```

2. Variables `CONTENT_ENCRYPTION_KEY` and `PROJECT_PRIVATE_KEY` must be present in the environment and base64 encoded. The CEK must match an uploaded WCEK on the given project, and the Project Private Key must be an RSA-4096 private key matching a Project Public Access Key on the given project.

3. A `config.yaml` file must be present in the working directory, with the following format:

```yaml
BEEKEEPER_USERNAME: username
BEEKEEPER_PROJECT_ID: project_id
BEEKEEPER_ORGANIZATION_ID: organization_id
BEEKEEPER_ENVIRONMENT: dev | tst | stg | prod (default = prod)
ALGORITHM_TYPE: validation | training (default = validation)
ALGORITHM_NAME: name (default = Jupyter Algorithm)
ALGORITHM_DESCRIPTION: description (default = null)
VERSION_DESCRIPTION: version_description (default = null)
ENTRYPOINT: algorithm_executable (default = run.py)
```

Once prerequisites are met, open the JupyterLab command pallete and select "Upload to EscrowAI". The algorithm directory will then be automatically encrypted and uploaded to EscrowAI.

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the escrowai_jupyter directory
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
pip uninstall escrowai_jupyter
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `escrowai-jupyter` within that folder.

### Packaging the extension

See [RELEASE](RELEASE.md)
