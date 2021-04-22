# Akustična normalizacija govornih posnetkov

## Odstranjevanje šuma s pomočjo spektralnega razločevanja (ang. Noise Reduction using Spectral Gating, NRSG)

Postopek temelji na algoritmu iz programa [Audacity](https://wiki.audacityteam.org/wiki/How_Audacity_Noise_Reduction_Works) oziroma njegovi reimplementaciji iz repozitorija [noisereduce](https://github.com/timsainb/noisereduce).

### Namestitev

Namestitev zahtevanih paketov lahko izvedemo z ukazom ```pip install -r requirements.txt```.

### Odstranitev šuma na posameznem posnetku

Odstranitev šuma na posemeznem posnetku se izvede z ukazom ```python nrsg.py -i vhodni/posnetek.wav -o razšumljeni/posnetek.wav```. Postopek uporabi del posnetka, ki ne vsebuje govora, za izračun moči šuma. Predpostavlja se, da obstaja začetni in končni premor v katerem ni govora. Privzeta dolžina obeh premorov je 0.5 sekunde, lahko pa ju poljubno nastavimo z argumentom ```-b``` (npr. 0.3 s začetnega in 0.4 s končnega premora dobimo z ```python nrsg.py -i vhodni/posnetek.wav -o razsumljeni/posnetek.wav -b 0.3 0.4```. Podrobnejši opis vhodnih argumentov dobimo z ```python nrsg.py -h```.

### Procesiranje množice posnetkov

Izvedba postopka na posnetkih v danem direktoriju se izvede z ```python nrsg.py -i dir/originalni/ -o dir/razsumljeni/```. Podrobnejši opis vhodnih argumentov skripte dobimo s ```python nrsg.py -h```.



## Odstranjevanje šuma s postopkom DFL (ang. deep feature losses)

Programska koda temelji na repozitoriju [SpeechDenoisingWithDeepFeatureLosses](https://github.com/francoisgermain/SpeechDenoisingWithDeepFeatureLosses).

### Namestitev

Za namestitev zahtevanih paketov glej poglavje [setup](https://github.com/francoisgermain/SpeechDenoisingWithDeepFeatureLosses#setup).

### Uporaba

Odstranitev šuma iz posnetkov v danem direktoriju se izvede s pomočjo ukaza ```python dfl.py -i /mapa/z/vhodnimi/posnetki/ -o /mapa/z/razsumljenimi/posnetki/ -m /mapa/z/modelom/SEnet/```.



## Odstranjevanje šuma s postopkom SEGAN (ang. Speech Enhancement Generative Adversarial Network)

### Namestitev

Programska implementacija se opira na kodo iz repozitorija [santi-pdp/segan](https://github.com/santi-pdp/segan), prvotnih avtorjev tega postopka, zato je potrebna namestitev tega repozitorija. Namestitev ostalih paketov se izvede z ukazom ```pip install -r requirements.txt```.

### SEGAN na posameznem posnetku

Odstranitev šuma na posemeznem posnetku se izvede z zagonom skripte ```clean_wav.sh``` iz repozitorija santi-pdp/segan.

### Procesiranje množice posnetkov

Izvedba postopka na vseh posnetkih v določenem direktoriju in poddirektorijih se izvede s ```python segan.py --init_noise_std 0. --save_path pot/do/segan_v1.1 --batch_size 100 --g_nl prelu --weights SEGAN-41700 --preemph 0.95 --bias_deconv True --bias_downconv True --bias_D_conv True --in_dir pot/do/posnetkov --save_clean_path pot/do/razsumljenih/posnetkov```. Pred zagonom je potrebno datoteko segan.py najprej kopirati v direktorij repozitorija santi-pdp/segan.




## Vrednotenje kakovosti govornih posnetkov

Pri izračunu kakovost zvočnih posnetkov, obdelanih po obravnavanih postopkih razšumljanja, se opiramo na programsko opremo iz repozitorija [Speechmetrics](https://github.com/aliutkus/speechmetrics). Postopek vrednotenja lahko izvedemo z ukazom ```python eval.py -i /mapa/z/vhodnimi/posnetki/ -o mere.csv```.
