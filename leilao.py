from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Sample data - a list of items
items = [{"id": 0, 'name': "Colar", 'preco_produto': 10, 'status':' '},
         {"id":1, "name": "Anel", "preco_produto": 150, 'status':' '},
         {"id":2, "name": "Tornozeleira", "preco_produto": 50, 'status':' '},
         {"id":3, "name": "Brinco", "preco_produto": 30, 'status':' '},
         {"id":4, "name": "Óculos", "preco_produto": 60, 'status':' '},
         {"id":5, "name": "Pulseira", "preco_produto": 35, 'status':' '},
         {"id":6, "name": "Bracelete", "preco_produto": 40, 'status':' '}
         ]

# GET request to retrieve all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

# POST request to add a new item
@app.route('/items', methods=['POST'])
def add_item():
    #Pegando os valores que estou passando no thunder
    data = request.get_json()
    if 'name' in data:
        item = {'id':data['id'], 'name': data['name'], 'preco_produto':data['preco_produto']}
        items.append(item)
        return jsonify({'message': 'Item added successfully'}), 201
    else:
        return jsonify({'message': 'Invalid request data'}), 400


# PUT request to update an item by its index
@app.route('/items', methods=['PUT'])
def update_item():
        ##Carrega o valor que o usuario inserir
        payload = request.get_json()
        novo_preco = payload.get('preco_produto', 'erro')
        if novo_preco != 'erro':
            cont = 0
            for i in items:
                    if i["id"]==payload["id"]:
                        items[cont]['preco_produto'] = novo_preco
                        return jsonify({'message': 'Item added successfully'})

                    else:
                        cont+=1;
        return jsonify({'message': 'Invalid request data'}), 400
                
        

# DELETE request to remove an item by its index
@app.route('/items', methods=['DELETE'])
def delete_item():
    cont = 0
    data = request.get_json()
    # novo_preco = data.get('id', 'erro')
    # print("oi")
    for i in items:
        if i["id"]==data["id"]:
            items.pop(cont)
            return jsonify({'message': 'Item deleted successfully'})
        cont+=1
  
@app.route('/procura', methods=['GET'])
def achar_item():
    result = []
    payload = request.args['name']
    # return jsonify(request.args)
    for i in items:
        if payload in i['name']:
              result.append(i)
    return jsonify(result)

@app.route('/<index:int>/status', methods=['PUT'])
def status_item():
    cont = 0
    status = request.get_json()
    for i in items:
       if i["id"]==status["id"]:
              items[cont].append(status["status"])
       cont=+1


@app.route('/total', methods=['GET'])
def total_itens():
    soma = 0
    cont = 0
    for i in items:
        if i['status'] == 'encerrado':
              soma += i['preco_produto']
        cont+=1
        
        return soma

openai.api_key = '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'

@app.route('/Sinonimos', methods=['GET'])
def Sinonimos():
    user_input = request.args.get('termo')  # Recebe o termo do usuário
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Sinônimos de {user_input}:",
        max_tokens=5
    )
    sinonimos = response.choices[0].text.strip().split("\n")  # Extrai sinônimos da resposta da OpenAI

    # Comparar sinônimos com a lista de itens
    matching_items = []
    for item in items:
        for sinonimo in sinonimos:
            if sinonimo.lower() in item['name'].lower():
                matching_items.append(item)

    return jsonify({'items': matching_items})

if __name__ == '__main__':
    app.run(debug=True)