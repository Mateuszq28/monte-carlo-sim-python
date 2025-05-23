<h1 align="center">monte-carlo-sim-python</h1>
<p align="center">
<i>Symulacja światła Metodą Monte Carlo w trójwymiarowej tkance skóry</i><br/>
własna implementacja<br/>
autor: Mateusz Miler<br/>
<a href="./README.md">Polish<a/>
<a href="./readme_eng.md">English<a/>
</p><br/>

<p align="center"><img src="readme_img/readme_img.jpg" alt="photon path visualization on epidermis tissue" align="center"><br/>
<i>Wizualizacja ścieżki ruchu 10 fotonów w tkance naskórka</i><br/>

### Powiązane projekty
- [monte-carlo-sim-python](https://github.com/Mateuszq28/monte-carlo-sim-python) - własna implementacja symulacji światła, moduł wizualizacji ścieżki przemieszczania się fotonów w 3D (za pomocą Vispy)
- [monte-carlo-sim-benchmark](https://github.com/Mateuszq28/monte-carlo-sim-benchmark) - przykładowe symulacje z literatury (tiny, small, mc321) oraz ich porównanie z własną symulacją, zapis do jednolitego formatu `CUBES.json`, przetwarzanie końcowe i normalizacja, generowanie tabel porównawczych, wykresy, mapy ciepła, wizualizacje 3D, mapy ciepła
- [monte-carlo-sim-tables](https://github.com/Mateuszq28/monte-carlo-sim-tables) - tabele ze statystykami rozkładów transportu fotonów dla przeprowadzonych eksperymentów
- [CUBES](https://drive.google.com/drive/folders/1w5mu88Oztn0OJCEOYhBU6R8CN_KE6HxM?usp=sharing) - wyniki przebiegu symulacji światła
metodą Monte Carlo w postaci trójwymiarowych tablic oddziaływania fotonów, dodatkowo w archiwum zamieszczono **tekst pracy magisterskiej**

### Przygotowanie środowiska

```shell
conda install PyOpenGL tabulate opencv matplotlib pillow vispy scipy numpy pandas Geometry3D tqdm
```

Jeśli występują problemy ze znalezieniem pakietów w Anacondzie można spróbować pobrać conda-build: \
https://anaconda.org/anaconda/conda-build/files \
a następnie zainstalować (plik dla python 11):

```shell
conda install win-64/conda-build-3.26.1-py311haa95532_0.tar.bz2
```

*Szybki start:* przegląd zacząć od klas RunAll.py and Sim.py \
i uruchomienia przykładu:

```shell
python RunAll.py
```

### Przetestowane środowisko uruchomieniowe
Jeśli możesz uruchomić ten projekt, po pomyślnej instalacji dodaj pull request z zainstalowanym środowiskiem - zrzutem listy pakietów - do folderu requirements_that_worked. Pomoże to nam w utrzymywaniu projektu, a innym użytkownikom w instalacji.

### Statystyki
liczba plików: 31</br>
liczba klas: 41</br>
liczba linijek kodu: 9184</br>

```shell
ls | grep \'.py^' |xargs wc -l
81 ArrowsDF.py
67 ByMatplotlib.py
358 ByVispy.py
703 ChartMaker.py
561 ColorPointDF.py
892 FeatureSampling.py
21 FillShapes.py
234 LightSource.py
167 Make.py
93 MakeMaterial.py
342 MarchingCubes.py
413 Material.py
217 Object3D.py
29 Photon.py
61 PlaneTriangles.py
302 Print.py
83 Projection.py
102 ProjectionArrowsDF.py
220 ProjectionResultRecordsDF.py
420 PropEnv.py
141 PropEnvVec.py
209 PropSetup.py
140 ResultEnvProcessing.py
128 RunAll.py
547 Sim.py
308 Slice.py
271 Space3dTools.py
113 SumProjection.py
1787 Test.py
157 test_wrapper.py
17 View.py
9184 total
```

<h2 align="center">Galeria</h1>

<p align="center"><img src="readme_img/diagram-drawio-sim.jpg" alt="Diagram klas" align="center"><br/>
<i>Diagram klas</i><br/>

<p align="center"><img src="readme_img/diagram-generatory.jpg" alt="Diagram interfejsu generatorów" align="center"><br/>
<i>Diagram interfejsu generatorów</i><br/>

<p align="center"><img src="readme_img/diagram-wizualizacja.jpg" alt="Diagram modułu wizualizacji" align="center"><br/>
<i>Diagram modułu wizualizacji</i><br/>

<p align="center"><img src="readme_img/photon_register_100.png" alt="100 fotonów" align="center"><br/>
<i>Wizualizacja ścieżki ruchu 100 fotonów</i><br/>

<p align="center"><img src="readme_img/multilayer_photon_register_100.png" alt="Naświetlanie tkanki z żyłą - 100 fotonów" align="center"><br/>
<i>Strumień 100 fotonów skierowany na tkankę z naczyniem krwionośnym</i><br/>
