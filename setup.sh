# make sure you have python 3.9.x
python3 --version | grep -q "Python 3.5" && echo "Using Python 3.9 :D :D :D " || { echo "Please use Python 3.9."; return; }

# python3 -m venv venv 
# source venv/bin/activate
# use CUDA version if you have GPU
# pip3 install torch==1.13.0  torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
# pip3 install pyg-lib torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-1.13.0+cu116.html
#--extra-index-url https://download.pytorch.org/whl/cpu 

# update 21 September 2024 -- CPU -- tested on macOS Monterey 12.4
pip install torch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cpu
pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-1.13.0.html

pip install pyg_lib
pip install 'numpy<2'

cd storage
wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/translator_transcoder_size_from_DOBF.pth -P pretrained/
wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/TransCoder_model_1.pth -P pretrained/
wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/TransCoder_model_2.pth -P pretrained/
cd ..

# cd codegen_sources/model/tools
# git clone https://github.com/glample/fastBPE.git

# cd fastBPE
# g++ -std=c++11 -pthread -O3 fastBPE/main.cc -IfastBPE -o fast
# python setup.py install
# cd ../../../../

mkdir tree-sitter
cd tree-sitter
git clone https://github.com/tree-sitter/tree-sitter-cpp.git
git clone https://github.com/tree-sitter/tree-sitter-java.git
git clone https://github.com/tree-sitter/tree-sitter-python.git
cd ..

cd codegen_sources/test_generation/
wget https://github.com/EvoSuite/evosuite/releases/download/v1.1.0/evosuite-1.1.0.jar
cd ../..

git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
cd ..
cd ..


pip install six scikit-learn stringcase transformers ply slimit astunparse submitit cython pandas apex anytree
pip install sacrebleu=="1.2.11" javalang psutil fastBPE hydra-core --upgrade --pre black==19.10b0
pip install tree-sitter==0.21.3

#transcoder setup : clang
cd /usr/lib/x86_64-linux-gnu/
sudo ln -s libclang-10.so.1 libclang-14.so

#srcML
sudo apt-get update -y
sudo apt-get remove -y --purge man-db
sudo apt-get install -y libc-bin

wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
sudo apt-get install -y mongodb-org
wget http://131.123.42.38/lmcrs/v1.0.0/srcml_1.0.0-1_ubuntu20.04.deb
sudo dpkg -i srcml_1.0.0-1_ubuntu20.04.deb
wget http://131.123.42.38/lmcrs/v1.0.0/srcml-dev_1.0.0-1_ubuntu20.04.deb
sudo dpkg -i srcml-dev_1.0.0-1_ubuntu20.04.deb

pip install pylibsrcml

cd NiCad
make
cd ..