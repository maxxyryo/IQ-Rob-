from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, date, timedelta
from dateutil import tz
import time, json

# função open config.json
def config():

    with open("config.json") as f:
        return json.load(f)

    return False

# tornar config GLOBAL
config = config()

# função converter time em data 
def timestamp_converter(x, retorno = 1):
	
    timestamp = datetime.fromtimestamp(x).strftime('%Y-%m-%d')

    return timestamp

API = IQ_Option(config['user_email'], config['password'])
    
# realizar conexão
API.connect()
API.change_balance(config['change_balance'])
    
# checar conexão e reconnectar caso não esteja logado
tentativas = 0
while not API.check_connect():
    if tentativas < config['max_reconnetion']:
        print("Conectando ao servidor IQ Option, tentativa "+str(tentativas))
        API.connect()
        tentativas = tentativas+1
    else:
        print("Erro ao realizr conexão, tentativas excedidas!")
        break

    time.sleep(1)

print("Usuário logada na API IQOptions com sucesso!")


def get_list_position():

    list_id_trader = []
    ranking = API.get_leader_board('Worldwide', 1, 100, 5)
    
    for i in ranking['result']['positional']:

        id = ranking['result']['positional'][i]['user_id']

        list_id_trader.append(id)

    return list_id_trader

# carregar list ranking
print("Carregando list do ranking")
list_ranking = get_list_position()

print(list_ranking)
print("======================================================")
print("Aguardando capturar traders ranking")
API.subscribe_live_deal(config['type_par'], config['par_change'], config['timeframe'], 10)

trader_old = 0
while True:
    traders = API.get_live_deal(config['type_par'], config['par_change'], config['timeframe'])

    if len(traders) > 0 and traders[0]['user_id'] != trader_old:

         #print(json.dumps(traders[0], indent=1))

         id = traders[0]['user_id']
         if id in list_ranking:
            print("O Trader "+str(traders[0]['name'])+" estar operando")

            status, id = API.buy(traders[0]['amount_enrolled'], config['par_change'], traders[0]['instrument_dir'], 1)
                 
            if status:
                print("[!] Ordem enviada com sucesso. Detalhes: DIR -> "+str(traders[0]['instrument_dir']))
         trader_old = traders[0]['user_id']


    time.sleep(1)




