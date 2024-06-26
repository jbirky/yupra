---
layout: default
title: Tasks
nav_order: 2
---

# To do items
{: .no_toc }

* * * 

Contents
{: .no_toc .text-delta }

- TOC
{:toc}


Recent Code fixes / Updates
{: .no_toc .text-delta }

<span>Update 06/21</span>{: .label .label-green }
Fixed the inpath issue and latex issue in [`tutorials/1_introduction_to_stellar.ipynb`](https://github.com/jbirky/yupra/blob/main/tutorials/1_introduction_to_stellar.ipynb). Infile templates have now been added to the project repo (in [`yupra/infiles`](https://github.com/jbirky/yupra/tree/main/infiles/stellar)) rather than pulling them from `vplanet_inference`.

* * *

### Week 2 

#### 06/24
{: .no_toc }

1. Sync your fork at `https://github.com/<username>/yupra/` with the main repo 

2. On your computer in terminal, go to your project folder and pull the latest version from your fork that you just synced:
    ```
    cd ~/research/yupra
    ```
    If you have uncommitted changes, make sure to commit those before pulling (replacing `<your username>` in the command):
    ```
    git add <your username>/
    git commit -m "add tutorial work"
    ```
    Then pull the new changes:
    ```
    git pull
    ```
    When you type `ls`, you should see some new folders have been added:
    ```
    /yupra
        /8-57am 
        /docs 
        /infiles 
        /jbirky 
        /JCruz001 
        /jgomez 
        /kari 
        /malachyc11 
        /Michelle161 
        /mmarquez 
        /README.md 
        /rory 
        /tutorials 
        /workshop 
        /.git 
        /.github 
        /.gitignore
    ```
3. Copy the file `/jbirky/stellar_johnstone.ipynb` to your own folder (replacing `<your username>` in the command):
    ```
    cp jbirky/stellar_johnstone.ipynb <your username>/
    ```

4. Open jupyter notebook and navigate to the file you just copied at `<your username>/stellar_johnstone.ipynb`

5. Once you've completed the notebook above (doing parameter sweeps for Trappist-1), play around with the parameters for other stars using the data here and see if you can find a "best fit": [https://jbirky.github.io/yupra/docs/datasets.html](https://jbirky.github.io/yupra/docs/datasets.html)


    | star | assignee |
    | --- | --- |
    | 55 Cnc | Karime |
    | GJ 1132 | Josue |
    | GJ 3470 | Malachy | 
    | HD 219134 | Julizza |
    | HD 97658 | Michelle |
    | Kepler-138 | Alex |
    | Kepler-18 | Rory |
    | Trappist-1 | Jess |


* * *

### Week 1 

#### 06/17
{: .no_toc }

- Set up [Git instructions](https://jbirky.github.io/yupra/docs/git_instructions.html)

- Complete [Tutorial 1](https://jbirky.github.io/yupra/docs/tutorials/1_introduction_to_stellar.html)

- Fill out [Week 1 survey](https://forms.gle/56krJtSQxdPoZgri8)

Some further videos you can check out

Stellar Evolution:

- [https://www.youtube.com/watch?v=wKxArKOxhsY](https://www.youtube.com/watch?v=wKxArKOxhsY)

- [https://www.youtube.com/watch?v=ye9vu_ozj44](https://www.youtube.com/watch?v=ye9vu_ozj44)

Git tutorials:

- [https://www.youtube.com/watch?v=USjZcfj8yxE](https://www.youtube.com/watch?v=USjZcfj8yxE)

- [https://www.youtube.com/watch?v=8JJ101D3knE](https://www.youtube.com/watch?v=8JJ101D3knE)