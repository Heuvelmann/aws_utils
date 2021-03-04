from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Pactia-AWS-Utils',
    url='https://github.com/Pactia/aws_utils',
    author='Pactia Team',
    author_email='',
    # Needed to actually package something
    packages=['aws-helpers'],
    # Needed for dependencies
    install_requires=['numpy', 'boto3', 'pandas', 'shareplum' ],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Algunas utilidades para usar AWS (S3, Athena) y Sharepoint',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)