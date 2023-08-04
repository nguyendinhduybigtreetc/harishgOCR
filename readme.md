wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb

sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb

sudo apt-get update && apt-get install -y python3-opencv (root
)
https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/windows-pip.html
python -m pip install paddlepaddle-gpu==2.5.1.post120 -f https://www.paddlepaddle.org.cn/whl/windows/mkl/avx/stable.html
pip install "paddleocr>=2.0.1" --upgrade PyMuPDF==1.21.1 numpy==1.23.0