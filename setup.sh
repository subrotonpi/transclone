# python3 -m venv venv
# source venv/bin/activate
#use CUDA version if you have GPU
# pip3 install torch==1.13.0  torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
# pip3 install pyg-lib torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-1.13.0+cu116.html
#--extra-index-url https://download.pytorch.org/whl/cpu #for cpu
pip install torch==1.13.0+cpu torchvision==0.14.0+cpu torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cpu
pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-1.13.0+cpu.html

cd storage
# wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/translator_transcoder_size_from_DOBF.pth -P pretrained/
# wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/TransCoder_model_1.pth -P pretrained/
# wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/TransCoder_model_2.pth -P pretrained/
cd ..
cd codegen_sources/model/tools
git clone https://github.com/glample/fastBPE.git

cd fastBPE
g++ -std=c++11 -pthread -O3 fastBPE/main.cc -IfastBPE -o fast
python setup.py install
cd ../../../../

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
pip install sacrebleu=="1.2.11" javalang tree_sitter psutil fastBPE hydra-core --upgrade --pre black==19.10b0
