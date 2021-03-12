# Introduction to Geo Programming

This space is reserved to class notes for Introduction to Geo Programming.

## Git Repository

Some commands to create and push files to git repository.

 - **Step 1**: Create a git user profile and click on the repositories tab, then click on `New`;
 - **Step 2**: Create an empty repository with a name and description, add `license` and ` .gitignore` after the first files;
 - **Step 3**: Create a folder with the same name that you put in the repository and move your files there;
 - **Step 4**: With a [`Git Command Line Interface`] installation (https://git-scm.com/downloads), open the` terminal` or `CMD` (The terminal must be opened in the folder of your choice);
 - **Step 5**: First command to initialize the git repository and add its files:
~~~shell
git init
git add .
~~~
 - **Step 6**: Add remote origin for upload files, you need to put the named url as your repository created before:
~~~shell
git remote add -f origin https://github.com/AbnerErnaniADSFatec/in-prog-geo
~~~
 - **Step 7**: Add a global user name and an e-mail to optimize future commits:
~~~shell
git config --global user.name "<my user>"
git config --global user.email "<my e-mail>"
~~~
 - **Step 8**: Commit your files. A commit is proof that you are an active user, is an update that you did. Every commit needs a description or message like "fix problem" or "fix bug" and your name will be marked in this update.
~~~shell
git commit -m "First notes for geo program" .
~~~
 - **Step 9**: Finally, send/send your files to the remote repository.
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

> **Obs.:** The notebook may not be able to recognize the kernel installed by conda, to fix it you must change the kernel manually in `kernel >> Change Kernel >> in-prog-geo`.