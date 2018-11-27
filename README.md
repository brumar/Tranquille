# Tranquille

## What is Tranquille?

Welcome to this [Transcrypt](https://github.com/QQuick/Transcrypt) + [Eel](https://github.com/ChrisKnott/Eel) boilerplate. 
Eel makes you write python-based **simple electron-like applications**. 
Transcrypt is a python -> js transpiler.
Tranquille means *"calm"* in French, because this repository aims to diminish the hair-pulling process of developing and distributing cross-platform GUIs with python. This may also refer to the relief of avoiding to deal with javascript.

## What's there

- A ready-to-use example that uses Transcrypt along Eel
- CI-CD test & build (windows and linux) with jenkins

![Screenshot](/screenshot.png?raw=true "Screenshot")


## Why Transcrypt is a good teammate to Eel ?

Eel exposing mechanism makes Transcrypt a very good choice to write the front end in python, here is why :
Eel does some adorable black magic (using bottle + websockets + parsing js files) to expose backend functions to the frontend **and reciprocally!**
```python
@eel.expose
def mypythonfunction:
	...
```
-> makes it accessible to javascript (as simple as `eel.mypythonfunction()`)

And symmetrically:
```js
eel.expose(myjavascriptfunction)
function myjavascriptfunction(){
	...
```
-> makes it accessible to python (as simple as `eel.myjavascriptfunction()`). I have not fully understood what was going on under hood to achieve that, but hell, that's sweet!

If instead of coding directly in javascript, you are using transcrypt, this makes the whole thing quite pleasant. 

During developpment, you can trick your IDE with fake imports like `if False: import backend as eel` and `if False: import frontendscrypt as eel` so that so that functions from the other side (and their signature, documentation etc...) are known by your IDE. This gives a pleasant (wrong) impression: Back-end and front-end talk to each others just as they were imported python modules.

From my understanding, Transcrypt is robust but incomplete (not the whole standard library is covered). This is a good fit here, because the core python tasks can be done on the back-end, while transcrypt is mainly dedicated to interact with the document. This is worth to mention that Transcrypt does not "lock you in", any javascript libaries can be imported and used seamlessly.

## The example in this repository

This example can be seen as a follow-up of the [tutorial on jenkins.io](https://jenkins.io/doc/tutorials/build-a-python-app-with-pyinstaller/), where an amazing CLI is built and tested via Jenkins. This CLI allows the user to add values. Eel provides you the graphical interface you need for this program. It also adds a diary feature, where all your previous computations is displayed on the web page. You need to install `requirements-dev.txt` with your preferred tool, just like (`pipenv install --python=3.6 -r requirements-dev.txt`). Then, you can run the example with 
```bash
cd sources
pipenv run python backend.py
```
Two other requirement files are in this repository, they are used by the Dockerfiles (`DF_...`) for distributing and testing the application.  

## CI-CD and cross-plateform builts

Eel repo suggests to use Pyinstaller to build cross-plateform GUI. The same is done here, except that built are done within docker containers controlled by Jenkins (itself running inside a docker container). The Jenkinsfile is largely based on a [good tutorial on jenkins.io](https://jenkins.io/doc/tutorials/build-a-python-app-with-pyinstaller/) showing how to use jenkins pipeline with pyinstaller. If you are not familiar with Jenkins Pipeline, I'd suggest to have a look on this tutorial. If you wish to work with jenkins installed locally, the script `runjenkins.sh` is taken from this tutorial, and should work on linux if the docker engine is installed, but you still have to configurate it to create a job which polls your git repository.

I have changed few steps and add few Dockerfiles, but the most part is taken from this tutorial. For the windows built I used this docker image : https://github.com/cdrx/docker-pyinstaller/tree/master/win32/py3 .
I kept the "addcalc" functions to integrate them into Eel. To practice integration tests, selenium has been added in the dependencies used by Jenkins when testing the application.

At the moment, the pipeline could be improved. Pipinstall should occur in the image building process to cache the result (and avoid this time consumming installation).

You can run Jenkins on docker with the bash script provided at the root (which is the same as in the tutorial). The weird 2>&1 | cat at each line for the stage "Deliver windows" is a fix for the error `Fatal Python error: Py_Initialize: can't initialize sys standard streams`. I do not know much more, but it seems to be related to the convolutions of running windows in wine in ubuntu...

**Warning** : The whole things will download Gigs of docker images, be sure to have enough bandwith and room on your computer.

## Why a fork of Eel is used in the requirements files?

The main reason is that I need eel to look inside some .py files to discover the front-end exposed functions. By the way, I picked this convention: to be found by eel, transcrypt files must end by `scrypt.py`. I have also added few features that I thought was relevant for the project. I hope some of my propositions will be integrated upstream. 

## Issues / Help? / Todos

- **Better discovering process** : In the future, as transcrypt is valid python code, one can totally think of an import strategy so that eel knows about exposed transcrypt functions without traversing and parsing the web directory (or maybe using [ast to find decorated functions](https://julien.danjou.info/python-ast-checking-method-declaration/)? 

- **Python3.7** That would be super awesome to use python3.7 so that the front-end and the backend could send dataclasses instances to each others. I made it work using gevent 1.3, but distributing the end result with pyinstaller got an obstacle it has issues with pyinstaller resulting in some "module not found" errors (https://github.com/ChrisKnott/Eel/issues/62, https://github.com/pyinstaller/pyinstaller/issues/3648, https://github.com/gevent/gevent/issues/1250). So gevent 1.2.2 is used, but the sad thing is that it won't be installed under python3.7 (https://github.com/gevent/gevent/issues/1019). If anyone finds something, that would be great.

- **Integration test for windows**. My pipeline does not test the `.exe` file generated. If someone know how to launch it so that it can be tested via selenium tests (preferably without installing a Jenkins Plugin), that would be awesome.

- **Leverage python type annotation**. There is probably nice things to do with type annotation so that backend and frontend communicates even more seamlessly. Do you have other ideas to take advantage of transcrypt python files?

- **Travis.CI**. I never used it, any nice PR is welcome, so that we could get a shiny "build pass" badge.

- **Consenting Adults Mode**. What if, instead using `eel.expose`, eel would directly expose functions that are imported at the top level of the module. Just like the "fake import trick" I mentioned, but this time, for real.
```python
#---backend.py---# 
from frontendscrypt import logthis, grabthat

logthis("hello)
infos = grabthat("infos")
```
and
```python
#---backendscrypt.py---# 
from backend import storethis, retrievethat

storethis("stuff")
infos = retrievethat("infos")
```
That seems theoretically possible right? Ok, maybe there might a problem of circular import that should be figured out, but if this is done, that would seriously raise the black magic of Eel to another level. 
