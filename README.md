# tensealstat
A library for homomorphic statistics using tenseal


# install: 

pip install git+https://github.com/kozzion/tensealstat@0.1.0

To update:

pip install git+https://github.com/kozzion/tensealstat@0.1.0 --upgrade

To update with latest repo code:

pip install git+https://github.com/kozzion/tensealstat@0.1.0 --upgrade --force-reinstall

# usage

The basic idea of this library is to a group of data holders to compute common statistics over their data without sharing any infomation on individual cases. 
There are three types of party involved: data holders, an agregator (which can also be a data holder) and a key holder.

Computation proceeds in 4 steps

1. The key holder creates a public/ private key pair and publishes the public key
2. The data holders encrypt their data using the public key and send it to the agregator
3. The agregator uses the public key and the encrypted data to compute encrypted statistics and sends those to the key holder 
4. The key holder uses the private key to decrypt the statistics and publishes these to the data owners

