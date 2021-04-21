# Odstranjevanje šuma s postopkom SEGAN (ang. Speech Enhancement Generative Adversarial Network)

## Namestitev

Programska implementacija se opira na kodo iz [repozitorija SEGAN](https://github.com/santi-pdp/segan), prvotnih avtorjev tega postopka, zato je potrebna namestitev tega repozitorija. Namestitev ostalih paketov se izvede z ukazom ```pip install -r requirements.txt```.

## SEGAN na posameznem posnetku

Odstranitev šuma na posemeznem posnetku se izvede z zagonom skripte ```clean_wav.sh``` iz repozitorija SEGAN.

## Procesiranje množice posnetkov

Izvedba postopka na vseh posnetkih v določenem direktoriju in poddirektorijih se izvede s ```python run_segan.py --init_noise_std 0. --save_path segan_v1.1 --batch_size 100 --g_nl prelu --weights SEGAN-41700 --preemph 0.95 --bias_deconv True --bias_downconv True --bias_D_conv True --in_dir pot/do/posnetkov --save_clean_path pot/do/razsumljenih/posnetkov```. Pred zagonom je potrebno datoteko run_segan.py najprej kopirati v direktorij repozitorija SEGAN.
