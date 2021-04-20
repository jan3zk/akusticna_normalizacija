# Odstranjevanje šuma s pomočjo spektralnega razločevanja (ang. Noise Reduction using Spectral Gating, NRSG)

Postopek temelji na algoritmu iz programa [Audacity](https://wiki.audacityteam.org/wiki/How_Audacity_Noise_Reduction_Works) oziroma njegovi reimplementaciji iz repozitorija [noisereduce](https://github.com/timsainb/noisereduce).

## Namestitev

Namestitev zahtevanih paketov lahko izvedemo z ukazom ```pip install -r requirements.txt```.

## NRSG na posameznem posnetku

Odstranitev šuma na posemeznem posnetku se izvede z ukazom ```python nrsg.py -v -f pot/do/posnetka.wav```. Postopek uporabi del posnetka, ki ne vsebuje govora, za izračun moči šuma. Predpostavlja se, da obstaja začetni in končni premor v katerem ni govora. Privzeta dolžina obeh premorov je 0.5 sekunde, lahko pa ju poljubno nastavimo z argumentom ```-b``` (npr. 0.3 s začetnega in 0.4 s končnega premora dobimo z ```python nrsg.py -v -f pot/do/posnetka.wav -b 0.3 0.4```. Podrobnejši opis vhodnih argumentov dobimo z ```python nrsg.py -h```.

## Procesiranje množice posnetkov

Izvedba postopka na vseh posnetkih v določenem direktoriju in poddirektorijih se izvede z ```python run_nrsg.py -d dir/originali/ -o dir/razsumljeni/```. Podrobnejši opis vhodnih argumentov skripte dobimo s ```python run_nrsg.py -h```.
