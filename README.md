# monte-carlo-sim-python

<a href="#polish_lang">Polski<a/>
<a href="#english_lang">English<a/>

## Polski
<id="polish_lang">

Symulacja światła Metodą Monte Carlo w trójwymiarowej tkance skóry.

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

*Szybki start:* przegląd zacząć od klas RunAll.py and Sim.py

przykład

```shell
python RunAll.py
```

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
<id="english_lang">

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

*Quick start:* read classes RunAll.py and Sim.py

example

```shell
python RunAll.py
```

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