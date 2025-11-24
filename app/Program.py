# pip install mysql-connector-python
import os
import mysql.connector
from mysql.connector import errorcode
from google.genai import Client

from dotenv import load_dotenv

load_dotenv()

# Variáveis
# Valores para criação de tabelas do Banco de Dados
tables = {
    "User": (
        """CREATE TABLE IF NOT EXISTS `signal`.`User` (
  `CPF` VARCHAR(11) NOT NULL,
  `Name` VARCHAR(45) NOT NULL,
  `Address` VARCHAR(45) NOT NULL,
  `DateOfBirth` DATE NOT NULL,
  `UserType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`CPF`),
  UNIQUE INDEX `CPF_UNIQUE` (`CPF` ASC) VISIBLE)
ENGINE = InnoDB;"""
    ),
    "Department": (
        """CREATE TABLE IF NOT EXISTS `signal`.`Department` (
  `DepartmentCode` VARCHAR(45) NOT NULL,
  `Name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`DepartmentCode`),
  UNIQUE INDEX `DepartmentCode_UNIQUE` (`DepartmentCode` ASC) VISIBLE)
ENGINE = InnoDB;"""
    ),
    "Team": (
        """CREATE TABLE IF NOT EXISTS `signal`.`Team` (
        `idTeam` INT NOT NULL AUTO_INCREMENT,
        `Name` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`idTeam`))
        ENGINE = InnoDB;"""
    ),
    "Employee": (
        """CREATE TABLE IF NOT EXISTS `signal`.`Employee` (
  `idEmployee` INT NOT NULL AUTO_INCREMENT,
  `Department_DepartmentCode` VARCHAR(45) NOT NULL,
  `Role` VARCHAR(45) NOT NULL,
  `Team_idTeam` INT NOT NULL,
  `User_CPF` VARCHAR(11) NOT NULL,
  PRIMARY KEY (`Department_DepartmentCode`, `Team_idTeam`, `User_CPF`),
  UNIQUE INDEX `idEmployee_UNIQUE` (`idEmployee` ASC) VISIBLE,
  INDEX `fk_Employee_Department1_idx` (`Department_DepartmentCode` ASC) VISIBLE,
  INDEX `fk_Employee_Team1_idx` (`Team_idTeam` ASC) VISIBLE,
  INDEX `fk_Employee_User1_idx` (`User_CPF` ASC) VISIBLE,
  CONSTRAINT `fk_Employee_Department1`
    FOREIGN KEY (`Department_DepartmentCode`)
    REFERENCES `signal`.`Department` (`DepartmentCode`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Employee_Team1`
    FOREIGN KEY (`Team_idTeam`)
    REFERENCES `signal`.`Team` (`idTeam`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Employee_User1`
    FOREIGN KEY (`User_CPF`)
    REFERENCES `signal`.`User` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
"""
    ),
    "Location": (
        """CREATE TABLE IF NOT EXISTS `signal`.`Location` (
  `idLocation` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `Latitude` DECIMAL(9,6) NOT NULL,
  `Longitude` DECIMAL(9,6) NOT NULL,
  PRIMARY KEY (`idLocation`))
ENGINE = InnoDB;"""
    ),
    "Mission": (
        """CREATE TABLE IF NOT EXISTS `signal`.`Mission` (
  `idMission` INT NOT NULL AUTO_INCREMENT,
  `ExtraInstructions` VARCHAR(100) NULL,
  `User_CPF` VARCHAR(11) NOT NULL,
  `Team_idTeam` INT NOT NULL,
  `Location_idLocation` INT NOT NULL,
  `completed` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`idMission`, `User_CPF`, `Team_idTeam`, `Location_idLocation`),
  INDEX `fk_Mission_User1_idx` (`User_CPF` ASC) VISIBLE,
  INDEX `fk_Mission_Team1_idx` (`Team_idTeam` ASC) VISIBLE,
  INDEX `fk_Mission_Location1_idx` (`Location_idLocation` ASC) VISIBLE,
  CONSTRAINT `fk_Mission_User1`
    FOREIGN KEY (`User_CPF`)
    REFERENCES `signal`.`User` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Mission_Team1`
    FOREIGN KEY (`Team_idTeam`)
    REFERENCES `signal`.`Team` (`idTeam`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Mission_Location1`
    FOREIGN KEY (`Location_idLocation`)
    REFERENCES `signal`.`Location` (`idLocation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
"""
    ),
    "Equipment": (
        """CREATE TABLE IF NOT EXISTS `signal`.`Equipment` (
  `idEquipment` INT NOT NULL,
  `Type` VARCHAR(45) NOT NULL,
  `Desctiption` VARCHAR(45) NOT NULL,
  `Last_maintenance` DATE NOT NULL,
  `Team_idTeam` INT NOT NULL,
  PRIMARY KEY (`idEquipment`, `Team_idTeam`),
  INDEX `fk_Equipment_Team1_idx` (`Team_idTeam` ASC) VISIBLE,
  CONSTRAINT `fk_Equipment_Team1`
    FOREIGN KEY (`Team_idTeam`)
    REFERENCES `signal`.`Team` (`idTeam`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;"""
    ),
    "Clients": (
        """CREATE TABLE IF NOT EXISTS `signal`.`Clients` (
  `idClients` INT NOT NULL AUTO_INCREMENT,
  `ContactInfo` VARCHAR(45) NOT NULL,
  `User_CPF` VARCHAR(11) NOT NULL,
  PRIMARY KEY (`idClients`, `User_CPF`),
  UNIQUE INDEX `idClients_UNIQUE` (`idClients` ASC) VISIBLE,
  INDEX `fk_Clients_User_idx` (`User_CPF` ASC) VISIBLE,
  CONSTRAINT `fk_Clients_User`
    FOREIGN KEY (`User_CPF`)
    REFERENCES `signal`.`User` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;"""
    ),
}




# Valores para serem inseridos no Banco de Dados
inserts = {
    "USER": (
        """
INSERT INTO `signal`.`User` (CPF, Name, Address, DateOfBirth, UserType) VALUES
('11111111111', 'Alice Silva', 'Rua A, 10', '1990-01-05', 'Client'),
('13289573907', 'joaozinhi', 'Rua A, 10', '1990-01-05', 'Client'),
('22222222222', 'Bruno Costa', 'Rua B, 20', '1985-02-10', 'Client'),
('33333333333', 'Carla Souza', 'Rua C, 30', '1992-03-15', 'Client'),
('44444444444', 'Diego Ramos', 'Rua D, 40', '1988-04-20', 'Client'),
('55555555555', 'Elisa Moreira', 'Rua E, 50', '1995-05-25', 'Client'),
('66666666666', 'Fabio Santos', 'Rua F, 60', '1987-06-30', 'Client'),
('77777777777', 'Gabriela Lima', 'Rua G, 70', '1993-07-12', 'Client'),
('88888888888', 'Henrique Dias', 'Rua H, 80', '1991-08-18', 'Client'),
('99999999999', 'Isabela Rocha', 'Rua I, 90', '1989-09-22', 'Client'),
('10101010101', 'Joao Pedro', 'Rua J, 100', '1994-10-11', 'Client'),
('11112341234', 'Castorice', 'Rua A, 10', '1990-01-05', 'Employee'),
('13289484897', 'Anaxagoras', 'Rua A, 10', '1990-01-05', 'Employee'),
('24567456722', 'Mydei', 'Rua B, 20', '1985-02-10', 'Employee'),
('33753453453', 'Phainon', 'Rua C, 30', '1992-03-15', 'Employee'),
('44896845234', 'Cerydra', 'Rua D, 40', '1988-04-20', 'Employee'),
('12389678964', 'Hysiles', 'Rua E, 50', '1995-05-25', 'Employee'),
('45645312117', 'Aglaea', 'Rua F, 60', '1987-06-30', 'Employee'),
('77427896777', 'Cyoher', 'Rua G, 70', '1993-07-12', 'Employee'),
('88887944888', 'Hyacine', 'Rua H, 80', '1991-08-18', 'Employee'),
('99745427079', 'Mem', 'Rua I, 90', '1989-09-22', 'Employee'),
('10119871001', 'Firefly', 'Rua J, 100', '1994-10-11', 'Employee');


"""
    ),
    "DEPARTMENT": (
        """
INSERT INTO `signal`.`Department` (DepartmentCode, Name) VALUES
('DEP01', 'Operations'),
('DEP02', 'Logistics'),
('DEP03', 'Communications'),
('DEP04', 'Analysis'),
('DEP05', 'Field Support'),
('DEP06', 'Maintenance'),
('DEP07', 'Medical'),
('DEP08', 'Research'),
('DEP09', 'Security'),
('DEP10', 'IT');

"""
    ),
    "TEAM": (
        """
INSERT INTO `signal`.`Team` (Name) VALUES
('Team Alpha'),
('Team Bravo'),
('Team Charlie'),
('Team Delta'),
('Team Echo'),
('Team Foxtrot'),
('Team Golf'),
('Team Hotel'),
('Team India'),
('Team Juliet');

"""
    ),
    "EMPLOYEE": (
        """
INSERT INTO `signal`.`Employee`
(Department_DepartmentCode, Role, Team_idTeam, User_CPF) VALUES
('DEP01', 'Technician', 1, '11112341234'),
('DEP01', 'Technician', 1, '13289573907'),
('DEP02', 'Operator', 1, '24567456722'),
('DEP03', 'Analyst', 1, '33753453453'),
('DEP04', 'Field Agent', 2, '44896845234'),
('DEP05', 'Medic', 2, '12389678964'),
('DEP06', 'Mechanic', 2, '45645312117'),
('DEP07', 'Scientist', 3, '77427896777'),
('DEP08', 'Engineer', 4, '88887944888'),
('DEP09', 'Security Officer', 5, '99745427079'),
('DEP10', 'IT Technician', 6, '10119871001');

"""
    ),
    "LOCATION": (
        """
INSERT INTO `signal`.`Location` (Name, Latitude, Longitude) VALUES
('Sector A', -23.550520, -46.633308),
('Sector B', -22.908333, -43.196388),
('Sector C', -15.793889, -47.882778),
('Sector D', -3.119028, -60.021731),
('Sector E', -30.034647, -51.217658),
('Sector F', -25.428954, -49.273251),
('Sector G', -19.916681, -43.934493),
('Sector H', -7.119495, -34.845011),
('Sector I', -2.530247, -44.306656),
('Sector J', -8.047562, -34.876964);

"""
    ),
    "MISSION": (
        """
INSERT INTO `signal`.`Mission`
(idMission, ExtraInstructions, User_CPF, Team_idTeam, Location_idLocation) VALUES
(1001, 'Proceed with caution', '11111111111', 1, 1),
(1002, 'Night operation', '22222222222', 2, 2),
(1003, 'Stealth required', '33333333333', 3, 3),
(1004, 'Rescue mission', '44444444444', 4, 4),
(1005, 'High alert zone', '55555555555', 5, 5),
(1006, 'Support team incoming', '66666666666', 6, 6),
(1007, 'Supply delivery', '77777777777', 7, 7),
(1008, 'Secure perimeter', '88888888888', 8, 8),
(1009, 'Recon mission', '99999999999', 9, 9),
(1010, 'Drone assistance', '10101010101', 10, 10);

"""
    ),
    "EQUIPMENT": (
        """
INSERT INTO `signal`.`Equipment`
(idEquipment, Type, Desctiption, Last_maintenance, Team_idTeam) VALUES
(1, 'Radio', 'Long range radio', '2025-01-01', 1),
(2, 'Medical Kit', 'First aid kit', '2025-02-01', 2),
(3, 'Drone', 'Recon drone', '2025-03-01', 3),
(4, 'Vehicle', 'Armored truck', '2025-04-01', 4),
(5, 'Laptop', 'Analysis laptop', '2025-01-15', 5),
(6, 'Kit Tools', 'Mechanical tools', '2025-02-18', 6),
(7, 'Scanner', 'Biometric scanner', '2025-03-10', 7),
(8, 'Camera', 'Thermal camera', '2025-01-08', 8),
(9, 'Helmet', 'Ballistic helmet', '2025-02-16', 9),
(10, 'Satellite Phone', 'Encrypted phone', '2025-03-12', 10);

"""
    ),
    "CLIENTS": (
        """
INSERT INTO `signal`.`Clients`
(ContactInfo, User_CPF) VALUES
('client01@mail.com', 11111111111),
('client02@mail.com', 22222222222),
('client03@mail.com', 33333333333),
('client04@mail.com', 44444444444),
('client05@mail.com', 55555555555),
('client06@mail.com', 66666666666),
('client07@mail.com', 77777777777),
('client08@mail.com', 88888888888),
('client09@mail.com', 99999999999),
('client10@mail.com', 10101010101);

"""
    ),
}

# Valores para deletar as tabelas
drop = {
    "USER": ("DROP TABLE IF EXISTS `signal`.`User`"),
    "DEPARTMENT": ("DROP TABLE IF EXISTS `signal`.`Department`"),
    "TEAM": ("DROP TABLE IF EXISTS `signal`.`Team`"),
    "EMPLOYEE": ("DROP TABLE IF EXISTS `signal`.`Employee`"),
    "LOCATION": ("DROP TABLE IF EXISTS `signal`.`Location`"),
    "MISSION": ("DROP TABLE IF EXISTS `signal`.`Mission`"),
    "EQUIPMENT": ("DROP TABLE IF EXISTS `signal`.`Equipment`"),
    "CLIENTS": ("DROP TABLE IF EXISTS `signal`.`Clients`"),
}

# Valores para teste de update
update = {
    "DEPARTMENT": (
        """
    UPDATE Department
    SET Name = 'Pedra'
    WHERE DepartmentCode = 'DEP01';
    """
    ),
    "TEAM": (
        """
    UPDATE team
    SET Name = 'Team Bella'
    WHERE idTeam = '2';"""
    ),
    "MISSIOn": (
        """
    UPDATE Mission
    SET completed = 1
    WHERE idMission = 1006;
    """
    )
}

# Valores para teste de delete
delete = {
    "MISSION": (
        """DELETE from Mission 
           where idMission = 1001; """
    ),
    "EQUIPMENT": (
        """
DELETE from EQUIPMENT
where idEquipment = 1;
"""
    ),
}


# Funções
def connect_signal():
    cnx = mysql.connector.connect(
        host="localhost",
        database="signal",
        user="root",
        password="root",
    )
    if cnx.is_connected():
        db_info = cnx.get_server_info()
        print("Conectado ao servidor MySQL versão ", db_info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)
        cursor.close()
    return cnx


def drop_all_tables(connect):
    print("\n---DROP DB---")
    # Esvazia o Banco de Dados
    cursor = connect.cursor()
    for drop_name in drop:
        drop_description = drop[drop_name]
        try:
            print("Drop {}: ".format(drop_name), end="")
            cursor.execute(drop_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    # connect.commit()
    cursor.close()


def create_all_tables(connect):
    print("\n---CREATE ALL TABLES---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Criando tabela {}: ".format(table_name), end="")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Tabela já existe.")
            else:
                print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def show_table(connect):
    print("\n---SELECIONAR TABELA---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        select = "select * from " + name
        cursor.execute(select)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("TABELA {}".format(name))
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
    cursor.close()


def update_value(connect):
    print("\n---SELECIONAR TABELA PARA ATUALIZAÇÃO---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        for table_name in tables:
            table_description = tables[table_name]
            if table_name == name:
                print(
                    "Para criar a tabela: {}, foi utilizado o seguinte código {}".format(
                        table_name, table_description
                    )
                )
        atributo = input("Digite o atributo a ser alterado: ")
        valor = input("Digite o valor a ser atribuído: ")
        codigo_f = input("Digite a coluna da chave primária: ")
        codigo = input("Digite o valor numérico do campo da chave primária: ")
        query = [
            "UPDATE ",
            name,
            " SET ",
            atributo,
            " = ",
            valor,
            " WHERE ",
            codigo_f,
            "= ",
            codigo,
        ]
        sql = "".join(query)
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("Atributo atualizado")
    connect.commit()
    cursor.close()


def insert_test(connect):
    print("\n---INSERT TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for insert_name in inserts:
        insert_description = inserts[insert_name]
        try:
            print("Inserindo valores para {}: ".format(insert_name), end="")
            cursor.execute(insert_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def update_test(connect):
    print("\n---UPDATE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for update_name in update:
        update_description = update[update_name]
        try:
            print(
                "Teste de atualização de valores para {}: ".format(update_name), end=""
            )
            cursor.execute(update_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def delete_test(connect):
    print("\n---DELETE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for delete_name in delete:
        delete_description = delete[delete_name]
        try:
            print(
                "Teste de atualização de valores para {}: ".format(delete_name), end=""
            )
            cursor.execute(delete_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def consulta1(connect):
    select_query = """
    SELECT
    L.idLocation,
    L.Name AS LocationName,
    T.idTeam,
    T.Name AS TeamName,
    COUNT(M.idMission) AS MissionsByThisTeamHere
FROM Location L
JOIN Mission M 
    ON L.idLocation = M.Location_idLocation
JOIN Team T
    ON M.Team_idTeam = T.idTeam
GROUP BY 
    L.idLocation, L.Name,
    T.idTeam, T.Name
ORDER BY L.Name, MissionsByThisTeamHere DESC;


    """
    print(
        "Primeira Consulta: Lista os locais e quantas missões cada time realizou no mesmo "
        
    )
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def consulta2(connect):
    select_query = """
    SELECT 
    TipoUsuario,
    Quantidade,
    ROUND(Quantidade / TotalUsuarios * 100, 2) AS Percentual
FROM (
    -- calcula total de usuarios por categoria
    SELECT 
        CASE
            WHEN E.User_CPF IS NOT NULL AND C.User_CPF IS NOT NULL THEN 'Funcionario_e_Cliente'
            WHEN E.User_CPF IS NOT NULL THEN 'Funcionario'
            WHEN C.User_CPF IS NOT NULL THEN 'Cliente'
            ELSE 'Nenhuma_Associacao'
        END AS TipoUsuario,
        COUNT(*) AS Quantidade,
        (SELECT COUNT(*) FROM User) AS TotalUsuarios
    FROM User U
    LEFT JOIN Employee E ON U.CPF = E.User_CPf
    LEFT JOIN Clients  C ON U.CPF = C.User_CPF
    GROUP BY TipoUsuario
) AS estatisticas;

    """
    print(
        "\nSegunda Consulta: cria um relatorio dos funcionarios e qual a percentagem é cada tipo (funcionario vs cliente) "
    )
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def consulta3(connect):
    select_query = """
    SELECT
    D.DepartmentCode,
    D.Name AS DepartmentName,

    -- total equipment per department
    COUNT(DISTINCT EQ.idEquipment) AS TotalEquipments,

    -- teams belonging to this department
    GROUP_CONCAT(DISTINCT T.Name ORDER BY T.Name SEPARATOR ', ') AS TeamsInDepartment,

    -- missions associated with those teams
    GROUP_CONCAT(
        DISTINCT CONCAT('Mission ', M.idMission, ' (Team ', T.Name, ')')
        ORDER BY M.idMission SEPARATOR '; '
    ) AS MissionsAssigned

FROM Department D
LEFT JOIN Employee EM ON EM.Department_DepartmentCode = D.DepartmentCode
LEFT JOIN Team T ON T.idTeam = EM.Team_idTeam
LEFT JOIN Equipment EQ ON EQ.Team_idTeam = T.idTeam
LEFT JOIN Mission M ON M.Team_idTeam = T.idTeam

    GROUP BY D.DepartmentCode, D.Name
    ORDER BY TotalEquipments DESC;

    """
    print(
        "\nTerceira Consulta: lista os departamentos que mais tem equipamentos pendente devolução e sua missão ativa"
    )
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def exit_db(connect):
    print("\n---EXIT DB---")
    connect.close()
    print("Conexão com o banco de dados foi encerrada!")


def crud_signal(connect):
    drop_all_tables(connect)
    drop_all_tables(connect) # to make sure no foreignkeys got in the way, shouldnt cause an error since it's drop if exists
    create_all_tables(connect)
    insert_test(connect)

    print("\n---CONSULTAS BEFORE---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    

    update_test(connect)
    delete_test(connect)

    print("\n---CONSULTAS AFTER---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)

def AI_assistance(connect):
    select_query = """
    SELECT
    D.DepartmentCode,
    D.Name AS DepartmentName,

    -- total equipment per department
    COUNT(DISTINCT EQ.idEquipment) AS TotalEquipments,

    -- teams belonging to this department
    GROUP_CONCAT(DISTINCT T.Name ORDER BY T.Name SEPARATOR ', ') AS TeamsInDepartment,

    -- missions associated with those teams
    GROUP_CONCAT(
        DISTINCT CONCAT('Mission ', M.idMission, ' (Team ', T.Name, ')')
        ORDER BY M.idMission SEPARATOR '; '
    ) AS MissionsAssigned

FROM Department D
LEFT JOIN Employee EM ON EM.Department_DepartmentCode = D.DepartmentCode
LEFT JOIN Team T ON T.idTeam = EM.Team_idTeam
LEFT JOIN Equipment EQ ON EQ.Team_idTeam = T.idTeam
LEFT JOIN Mission M ON M.Team_idTeam = T.idTeam

    GROUP BY D.DepartmentCode, D.Name
    ORDER BY TotalEquipments DESC;

    """
    print(
        "\nTerceira Consulta: lista os departamentos que mais tem equipamentos pendente devolução e sua missão ativa"
    )
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    qstring = ", ".join(str(item) for item in myresult)
    AI_wrapper(qstring)

def AI_wrapper(data):
    
    client = Client(api_key=os.environ["GEMINI_API_KEY"])

    MissionDetails = input("detalhes: ")

    RequestString = "taking into accout the mission is:" +MissionDetails+ "select four candidates from the following list"+ data
    print(RequestString)
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=RequestString,
        )
        print(response)
    except Exception as e:
        print(f"\n\n\nAn unexpected error occurred: {e}")
   

# Main
try:
    # Estabelece Conexão com o DB
    con = connect_signal()

    power_up = 1
    while power_up == 1:
        interface = """\n       ---MENU---
        1.  CRUD signal
        2.  TESTE - Create all tables (works)
        3.  TESTE - Insert all values (works)
        4.  TESTE - Update (works)
        5.  TESTE - Delete (works)
        6.  CONSULTA 01
        7.  CONSULTA 02
        8.  CONSULTA 03
        9.  AI CONSULTANT
        10. CONSULTA TABELAS INDIVIDUAIS
        11. UPDATE VALUES 
        12. CLEAR ALL signal (works)
        0.  DISCONNECT DB\n """
        print(interface)

        choice = int(input("Opção: "))
        if choice < 0 or choice > 12:
            print("Erro tente novamente!")
            choice = int(input())

        if choice == 0:
            if con.is_connected():
                exit_db(con)
                print("Muito obrigada(o).")
                break
            else:
                break

        if choice == 1:
            crud_signal(con)

        if choice == 2:
            create_all_tables(con)

        if choice == 3:
            insert_test(con)

        if choice == 4:
            update_test(con)

        if choice == 5:
            delete_test(con)

        if choice == 6:
            consulta1(con)

        if choice == 7:
            consulta2(con)

        if choice == 8:
            consulta3(con)

        if choice == 9:
            AI_assistance(con)

        if choice == 10:
            show_table(con)

        if choice == 11:
            update_value(con)

        if choice == 12:
            drop_all_tables(con)

    con.close()

except mysql.connector.Error as err:
    print("Erro na conexão com o banco de dados!", err.msg)
