import pymysql.cursors
from ambiente import Hash, jovem1, pares

connection = pymysql.connect(host=jovem1.host, user=jovem1.user, password=jovem1.password, db="samu",cursorclass=pymysql.cursors.DictCursor)

class Unidade:
    def __init__(self,nome,vermelha,verde,ortopedista,cirurgiao,radiografia):
        self.nome = nome
        self.vermelha = vermelha
        self.verde = verde
        self.ortopedista = ortopedista
        self.cirurgiao = cirurgiao
        self.radiografia = radiografia



nome = input("Nome da unidade:")
vermelha = input("Restricao da unidade:")
verde = input("Atende verdes:")
ortopedista = input("Tem ortopedista?")
cirurgiao = input("Tem cirurgião?")
radiografia = input("Rx funcionando?")


with connection:
    with connection.cursor() as cursor:
        
        sql = f"INSERT INTO samu.unidades(idunidades,unidade,restricao,verde,ortopedista,cirurgiao,rx) VALUES (DEFAULT,'{nome}','{vermelha}','{verde}','{ortopedista}','{cirurgiao}','{radiografia}')"
        cursor.execute(sql)

        
    connection.commit()
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `samu`.`unidades`"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)