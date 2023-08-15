import requests
import json


def infos_cep(cep):
    req = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    infos = json.loads(req.text)
    return infos

def print_infos(cep):
    cep_info = infos_cep(cep)

    keys = ['logradouro', 'bairro', 'localidade', 'uf']
    ref = ['Rua', 'Bairo', 'Cidade', 'Estado']

    print('Confirme se as informações estão corretas:\n')
    # for k, j in zip(keys, ref):
    #     print(f'{j:<{6}}: {cep_info[k]}')
    a=''
    for k, j in zip(keys, ref):
        
        print(f'{j+":":<{7}} {cep_info[k]}')  




if __name__ == '__main__':

    cep='13086061'
    print_infos(cep)