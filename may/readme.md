# Virtual Environment

### `venv`
```{python}
### venv
!python -m venv NAME
!NAME\Scripts\activate
!pip install -r requirements.txt

# 주피터 노트북에서 가상환경 사용하려면, 주피터 노트북 내부에 가상환경을 설치해야 함.
!pip install jupyter
!pip install ipykernel
!python -m ipykernel install --user --name NAME --display-name "출력될 커널 이름"

# requirements.txt 생성
!dir /B Lib\site-packages
!pip freeze > requirements.txt

!deactivate
```
### `conda`
```{python}
### conda
!conda create --name NAME
!conda create --name NAME python=VERSION
# conda는 venv와는 달리 가상 환경을 현재 폴더에 생성하지 않고 아나콘다 설치 폴더의 envs 안에 생성함.
!activate NAME
!conda install PACKAGE.NAME
!conda search PACKAGE.NAME

# requirements.txt 생성
!conda list --export > package-list.txt
!conda install --file package-list.txt
```

# Github

git 