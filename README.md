# monte-carlo-sim-python

<p align="center"><img src="readme_img.jpg" alt="photon path visualization on epidermis tissue" align="center"><br/>
<i>wizualizacja ścieżki fotonów w tkance naskórka</i><br/>
<i>photon path visualization on epidermis tissue</i></p><br/>

<a href="#polish_lang">Polish<a/>
<a href="#english_lang">English<a/>

## Polish
<span id="polish_lang"></span>

Symulacja światła Metodą Monte Carlo w trójwymiarowej tkance skóry. \

#### Powiązane projekty
- [monte-carlo-sim-python](https://github.com/Mateuszq28/monte-carlo-sim-python) - symulacja światła, moduł wizualizacji ścieżki fotonów w 3D (za pomocą Vispy)
- [monte-carlo-sim-benchmark](https://github.com/Mateuszq28/monte-carlo-sim-benchmark) - dostosowane symulacje przykładowe z literatury (tiny, small, mc321), zapis do jednolitego formatu "CUBES.json", przetwarzanie końcowe i normalizacja, generowanie tabel porównawczych, wykresy, mapy ciepła, wizualizacje 3D ortogonalnych map ciepła
- [monte-carlo-sim-tables](https://github.com/Mateuszq28/monte-carlo-sim-tables) - tabele ze statystykami rozkładów transportu fotonów dla przeprowadzonych eksperymentów
- [CUBES](https://1drv.ms/f/c/7871da7edeb06dcc/Ei70d6guE4lBgMsf6FgGbJsBUcYmqrgZFZZxBHvQeMgqBQ) - wyniki najważniejszych eksperymentów zapisane w ujednoliconym formacie CUBE.json

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

### "U mnie działa"
Jeśli możesz uruchomić ten projekt, po pomyślnej instalacji dodaj pull request z zainstalowanym środowiskiem - zrzutem listy pakietów - do folderu requirements_that_worked. Pomoże to nam w utrzymywaniu projektu, a innym użytkownikom w instalacji.

### Statistics
number of python files: 31</br>
number of classes: 41</br>
lines of code: 9184</br>

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

## English
<span id="english_lang"></span>

Light simulation in 3D tissue using Monte Carlo method

### preparing the environment

```shell
conda install PyOpenGL tabulate opencv matplotlib pillow vispy scipy numpy pandas Geometry3D tqdm
```

If you have some problems with finding packages in Anaconda, try download conda-build from there: \
https://anaconda.org/anaconda/conda-build/files \
and then install (file for python 11):

```shell
conda install win-64/conda-build-3.26.1-py311haa95532_0.tar.bz2
```

*Quick start:* read classes RunAll.py and Sim.py \
and try an example:

```shell
python RunAll.py
```

### Requirements that worked
If you can run this project, after successful instalation, please add a pull request with your environment installed package list dump into requirements_that_worked folder. It will help us to maintain the project and the other users to run.

### Statistics
number of python files: 31</br>
number of classes: 41</br>
lines of code: 9184</br>

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
