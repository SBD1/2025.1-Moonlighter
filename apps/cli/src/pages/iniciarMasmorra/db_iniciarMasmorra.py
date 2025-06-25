from setup.database import connect_to_db
from colorama import Fore

def salvarMasmorra(nickname, seedMasmorra, NomeMasmorra, matriz):
    maxLinhas = len(matriz)
    maxColunas = len(matriz[0])

    connection = connect_to_db();
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()

    cursor.execute('''
                  SELECT 'seedMundo' FROM 'mundo'
                    WHERE "nickname" = %s;
                  ''', (nickname,)
                  )

    seedMundo = cursor.fetchone();

    cursor.execute('''
                  INSERT INTO 'inst_masmorra'
                    VALUES
                    (%s, %s, %s, TRUE);
                  ''', (seedMundo, seedMasmorra, NomeMasmorra, )
                  )
    
    seedSalasPercorrida = []
    recursaoSalvarSalas(matriz)
            
    def recursaoSalvarSalas(matriz, x = 7, y = 7):
        if matriz[x, y] == 0 or (x == maxLinhas or x == 0) or (y == maxColunas or y == 0):
            return
        if matriz[x, y] in seedSalasPercorrida:
            return
        else:
          seedSalasPercorrida.pop(matriz[x, y])
          cursor.execute('''
                        INSERT INTO 'sala'
                          VALUES 
                          (%s, %s, %s, 'Teste', %s, %s, %s)
                        ''', (matriz[x, y], x, y, seedMundo, NomeMasmorra,)
                        )
          recursaoSalvarSalas(matriz, x+1, y)
          recursaoSalvarSalas(matriz, x-1, y)
          recursaoSalvarSalas(matriz, x, y+1)
          recursaoSalvarSalas(matriz, x, y-1)