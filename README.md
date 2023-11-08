# dash-whales
Tentative d'ihm pour tracker des whales

First check if you have python or pip already installed by running

```
pip list
```
or 
```
python --version
```

If it's not installed I recommand this version :

https://www.python.org/downloads/release/python-3815/

Once you have pip and python installed in your machine

Open a terminal, go to the root of your cloned repository called dash-whales

```
cd dash-whales
```

Install dependencies : 

```
pip install -r requirements.txt
```

To scrap data and write it in output directory, run below command on terminal:
```
python scrap_data.py
```

To run the dash application, run below command on terminal:
```
python app.py
```

This is the first version to get transaction data on etherscan, but its working kinda ok.
There are few known bugs which i will fix as soon as possible.


Pour lancer l'API
```
uvicorn main:app --reload
```