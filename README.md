para executar o projeto é necessario apenas ter o python instalado.

ao clonar o projeto entrar na pasta do gateway e rodar:

pip install -r requirements.txt

após isso se faz necessario rodar cada um dos microserviços isoladamente com:

uvicorn catalog_service:app --host 0.0.0.0 --port 8001

uvicorn order_service:app --reload --port 8002

e assim sucessivamente 
