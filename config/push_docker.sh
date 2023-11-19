
docker pull rayproject/ray:2.8.0
#docker pull cschranz/gpu-jupyter:v1.5_cuda-11.6_ubuntu-20.04
#docker pull anyscale/aviary:latest

docker tag rayproject/ray:2.6.3 localhost:32000/ray:2.8.0
#docker tag cschranz/gpu-jupyter:v1.5_cuda-11.6_ubuntu-20.04 localhost:32000/gpu-jupyter:v1.5_cuda-11.6_ubuntu-20.04
#d#ocker tag anyscale/aviary:latest localhost:32000/aviary:latest

docker push localhost:32000/ray:2.8.0
#docker push localhost:32000/gpu-jupyter:v1.5_cuda-11.6_ubuntu-20.04
#docker push localhost:32000/aviary:latest