# Homework 6


## Intro
I trained BERT in a jupyter notebook to classify toxic comments. I ran the notebook on a V100 VM and a P100 VM 

## Steps

### P100 instance

Notebook: BERT_classifying_toxicity_p100.ipynb
```
ibmcloud sl vs create --datacenter=wdc07 --hostname=p100a --domain=apik.com --image=<image_number> --billing=hourly  --network 1000 --key=1687688 --flavor AC1_8X60X100 --san

ibmcloud sl vs list
ssh root@<public_id>
git clone https://github.com/apikzorian/v2.git

cd v2/week06/hw/
nvidia-docker run --rm --name hw06 -p 8888:8888 -v "$PWD":/HW06 -d w251/hw06:x86-64
docker logs <containerid>
```

### V100 instance
Notebook: BERT_classifying_toxicity_v100.ipynb
```
ibmcloud sl vs create --datacenter=wdc07 --hostname=v100a --domain=apik.com --image=<image_number> --billing=hourly  --network 1000 --key=1687688 --flavor AC2_8X60X100 --san

ibmcloud sl vs list
ssh root@<public_id>
git clone https://github.com/apikzorian/v2.git

cd v2/week06/hw/
nvidia-docker run --rm --name hw06 -p 8888:8888 -v "$PWD":/HW06 -d w251/hw06:x86-64
docker logs <containerid>
```

### Results
Training on the V100 took about 1.5 hours, while it took 6h on the P100 (4x!). The AUC was 0.97 in both cases.
