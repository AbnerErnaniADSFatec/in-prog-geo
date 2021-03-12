# Introduction to Geo Programming

This space is reserved to class notes for Introduction to Geo Programming.

## Git Repository

Some commands to create and push files to git repository.

 - **Step 1**: Create a git user profile and click in repositories tab, in following click in `New`;
 - **Step 2**: Create an empty repository with a name and description add `license` and `.gitignore` after the first files;
 - **Step 3**: Create a folder with the same name you put in repository and move your files to there;
 - **Step 4**: With a [`Git Command Line Interface`](https://git-scm.com/downloads) installation, open `terminal` or `CMD` (The terminal must be open on your choice folder);
 - **Step 5**: Fist command for initialize git repository and add your files:
~~~shell
git init
git add .
~~~
 - **Step 6**: Add remote origin for upload files, you get the url named as your repository created before:
~~~shell
git remote add -f origin https://github.com/AbnerErnaniADSFatec/in-prog-geo
~~~
 - **Step 7**: Add a global user name and an e-mail to optimize future commits:
~~~shell
git config --global user.name "<my user>"
git config --global user.email "<my e-mail>"
~~~
 - **Step 8**: Commit your files. A commit is a proof that you is active user, it is a update that you did. Every commit needs a description or message like "fix issue" or "fix bug" and your name will be marked in this update.
~~~shell
git commit -m "First notes for geo program" .
~~~
 - **Step 9**: Finally push your files to remote repository.
~~~shell
git push origin master
~~~

### Jupyter Environment

Some commands to use virtual environt [`Miniconda 3`](https://docs.conda.io/en/latest/miniconda.html).

 - **Step 1**: Create a virtual environment `Python 3+` with `conda` installation and activate this environment:
~~~shel
$ conda create --name in-prog-geo python=3.8
$ conda activate in-prog-geo
~~~
 - **Step 2**: Install `ipykernel` to manage kernels in jupyter notebook and link this python installation to kernels for jupyter:
~~~shell
(in-prog-geo) $ conda install notebook ipykernel
(in-prog-geo) $ ipython kernel install --user --name in-prog-geo
~~~
 - **Step 3**: Install environment dependencies for `Jupyter Lab`:
~~~shell
(in-prog-geo) $ python -m pip install jupyter
~~~
 - **Step 4**: Run Jupyter locally and start to create your Python notebooks for class:
~~~shell
(in-prog-geo) $ jupyter notebook
~~~

> **Obs.:** The notebook could not recognize the kernel installed by conda, to fix this you must change kernel manually in `kernel >> Change Kernel >> in-prog-geo`.