# make sure you have python 3.9.x
python3 --version | grep -q "Python 3.5" && echo "Using Python 3.9 :D :D :D " || { echo "Please use Python 3.9."; return; }

python3 -m venv venv 
source venv/bin/activate
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

mkdir tree-sitter
cd tree-sitter
git clone https://github.com/tree-sitter/tree-sitter-cpp.git
git clone https://github.com/tree-sitter/tree-sitter-java.git
git clone https://github.com/tree-sitter/tree-sitter-python.git
cd ..

cd codegen_sources/test_generation/
wget https://github.com/EvoSuite/evosuite/releases/download/v1.1.0/evosuite-1.1.0.jar
cd ../..


pip install six scikit-learn stringcase transformers ply slimit astunparse submitit cython pandas apex anytree
pip install sacrebleu=="1.2.11" javalang psutil fastBPE hydra-core --upgrade --pre black==19.10b0
pip install tree-sitter==0.21.3

# Nicad
cd NiCad
make
cd ..

#srcML -- important for gmn-srcml model
echo "It is preffered that you would install srcml manually instead of through this script"

wget http://131.123.42.38/lmcrs/v1.0.0/srcml-1.0.0-macOS-10.15.2.pkg
sudo installer -pkg srcml-1.0.0-macOS-10.15.2.pkg -target /
# required
pip install pylibsrcml