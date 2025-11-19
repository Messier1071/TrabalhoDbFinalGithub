#pip install mysql-connector-python

import mysql.connector
from mysql.connector import errorcode

# Variáveis
# Valores para criação de tabelas do Banco de Dados
tables = {'RACA': (
    """CREATE TABLE `RACA` (
      `id_raca` integer PRIMARY KEY NOT NULL,
      `tipo_animal` varchar(10) NOT NULL,
      `descricao` varchar(50) NOT NULL,
      CHECK (`tipo_animal` in ('Cachorro','Gato'))
    ) ENGINE=InnoDB"""),
    'ANIMAL': (
        """CREATE TABLE `ANIMAL` (
            `cod_animal` integer PRIMARY KEY NOT NULL,
            `id_raca` integer NOT NULL,
            `nome` varchar(100) NOT NULL,
            `cor` varchar(20) NOT NULL,
            `peso_kg` numeric(4,2) NOT NULL,
            `porte` varchar(20) NOT NULL,
            `tipo_sangue` varchar(10),
            FOREIGN KEY(`id_raca`) REFERENCES `RACA` (`id_raca`),
            CHECK (`porte` in ('Pequeno','Médio', 'Grande'))
        ) ENGINE=InnoDB"""),
    'LOCAL': (
        """CREATE TABLE `LOCAL` (
        `id_local` integer PRIMARY KEY NOT NULL,
        `endereco` varchar(150) NOT NULL,
        `bairro` varchar(50) NOT NULL,
        `cep` varchar(10) NOT NULL,
        `cidade` varchar(150) NOT NULL,
        `uf` varchar(2) NOT NULL
        ) ENGINE=InnoDB"""),
    'ANIMAL_RESGATE': (
        """CREATE TABLE `ANIMAL_RESGATE` (
        `data_resgate` timestamp NOT NULL,
        `cod_animal` integer NOT NULL,
        `id_local` integer NOT NULL,
        `descricao` text NOT NULL,
        PRIMARY KEY(`data_resgate`,`cod_animal`,`id_local`),
        FOREIGN KEY(`cod_animal`) REFERENCES `ANIMAL` (`cod_animal`),
        FOREIGN KEY(`id_local`) REFERENCES `LOCAL` (`id_local`)
        ) ENGINE=InnoDB"""),
    'ADOTANTE': (
        """CREATE TABLE `ADOTANTE` (
        `cod_adotante` integer PRIMARY KEY NOT NULL,
        `documento` varchar(18) NOT NULL,
        `nome` varchar(100) NOT NULL,
        `email` varchar(100),
        `telefone` varchar(14) NOT NULL,
        `endereco` varchar(150) NOT NULL,
        `bairro` varchar(50) NOT NULL,
        `cep` varchar(10) NOT NULL,
        `cidade` varchar(150) NOT NULL,
        `uf` varchar(2) NOT NULL,
        UNIQUE(`documento`)
        ) ENGINE=InnoDB"""),
    'ADOCAO': (
        """CREATE TABLE `ADOCAO` (
        `cod_animal` integer NOT NULL,
        `cod_adotante` integer NOT NULL,
        `data_adocao` timestamp NOT NULL,
        PRIMARY KEY(`cod_animal`,`cod_adotante`),
        FOREIGN KEY(`cod_animal`) REFERENCES ANIMAL (`cod_animal`),
        FOREIGN KEY(`cod_adotante`) REFERENCES ADOTANTE (`cod_adotante`)
        ) ENGINE=InnoDB"""),
    'FISCAL': (
        """CREATE TABLE `FISCAL` (
        `cod_fiscal` integer PRIMARY KEY NOT NULL,
        `nome` varchar(100) NOT NULL
        ) ENGINE=InnoDB"""),
    'BO': (
        """CREATE TABLE `BO` (
        `id_bo` integer PRIMARY KEY NOT NULL,
        `data_bo` timestamp NOT NULL,
        `descricao` text NOT NULL
        ) ENGINE=InnoDB"""),
    'FISCALIZACAO': (
        """CREATE TABLE `FISCALIZACAO` (
        `id_bo` integer PRIMARY KEY NOT NULL,
        `cod_adotante` integer NOT NULL,
        `cod_fiscal` integer NOT NULL,
        FOREIGN KEY(`id_bo`) REFERENCES `BO` (`id_bo`),
        FOREIGN KEY(`cod_adotante`) REFERENCES `ADOTANTE` (`cod_adotante`),
        FOREIGN KEY(`cod_fiscal`) REFERENCES `FISCAL` (`cod_fiscal`)
        ) ENGINE=InnoDB"""),
    'RACAO': (
        """CREATE TABLE `RACAO` (
        `id_racao` integer PRIMARY KEY NOT NULL,
        `marca` varchar(50) NOT NULL,
        `tipo_animal` varchar(10) NOT NULL,
        `qtde_kg_estoque` integer NOT NULL,
        CHECK (`tipo_animal` in ('Cachorro','Gato'))
        ) ENGINE=InnoDB"""),
    'ANIMAL_RACAO': (
        """CREATE TABLE `ANIMAL_RACAO` (
        `cod_animal` integer NOT NULL,
        `id_racao` integer NOT NULL,
        `qtde_kg_mensal` numeric(5,2) NOT NULL,
        PRIMARY KEY(`cod_animal`,`id_racao`),
        FOREIGN KEY(`id_racao`) REFERENCES `RACAO` (`id_racao`),
        FOREIGN KEY(`cod_animal`) REFERENCES `ANIMAL` (`cod_animal`)
        ) ENGINE=InnoDB"""),
    'FORNECEDOR': (
        """CREATE TABLE `FORNECEDOR` (
        `cod_fornecedor` integer PRIMARY KEY NOT NULL,
        `nome` varchar(100) NOT NULL,
        `telefone` varchar(14) NOT NULL
        ) ENGINE=InnoDB"""),
    'DOACAO': (
        """CREATE TABLE `DOACAO` (
        `data_doacao` timestamp NOT NULL,
        `id_racao` integer NOT NULL,
        `cod_fornecedor` integer,
        `qtde_kg` integer NOT NULL,
        PRIMARY KEY(`data_doacao`,`id_racao`,`cod_fornecedor`),
        FOREIGN KEY(`id_racao`) REFERENCES `RACAO` (`id_racao`),
        FOREIGN KEY(`cod_fornecedor`) REFERENCES `FORNECEDOR` (cod_fornecedor)
        ) ENGINE=InnoDB"""),
    'CLINICA': (
        """CREATE TABLE `CLINICA` (
        `id_clinica` integer PRIMARY KEY NOT NULL,
        `nome` varchar(255) NOT NULL,
        `telefone` varchar(14) NOT NULL
        ) ENGINE=InnoDB"""),
    'CONSULTA': (
        """CREATE TABLE `CONSULTA` (
        `id_consulta` integer PRIMARY KEY NOT NULL,
        `cod_animal` integer NOT NULL,
        `id_clinica` integer NOT NULL,
        `data_ida` timestamp NOT NULL,
        `data_volta` timestamp,
        `valor` numeric(6,2),
        FOREIGN KEY(`cod_animal`) REFERENCES `ANIMAL` (`cod_animal`),
        FOREIGN KEY(`id_clinica`) REFERENCES `CLINICA` (`id_clinica`)
        ) ENGINE=InnoDB"""),
    'VACINA': (
        """CREATE TABLE `VACINA` (
        `cod_vacina` integer PRIMARY KEY NOT NULL,
        `descricao` varchar(100) NOT NULL
        ) ENGINE=InnoDB"""),
    'REGISTRO_VACINA': (
        """CREATE TABLE `REGISTRO_VACINA` (
        `id_consulta` integer NOT NULL,
        `cod_vacina` integer NOT NULL,
        PRIMARY KEY(`id_consulta`,`cod_vacina`),
        FOREIGN KEY(`id_consulta`) REFERENCES `CONSULTA` (`id_consulta`),
        FOREIGN KEY(`cod_vacina`) REFERENCES `VACINA` (`cod_vacina`)
        ) ENGINE=InnoDB"""),
}

# Valores para serem inseridos no Banco de Dados
inserts = {'RACA': (
    """insert into RACA (id_raca, tipo_animal, descricao) values 
        (1000, 'Cachorro', 'Vira-Lata'),
        (2000, 'Gato', 'Vira-Lata'),
        (1001, 'Cachorro', 'Akita'),
        (1002, 'Cachorro', 'Basset hound'),
        (1003, 'Cachorro', 'Beagle'),
        (1004, 'Cachorro', 'Bichon frisé'),
        (1005, 'Cachorro', 'Boiadeiro australiano'),
        (1006, 'Cachorro', 'Border collie'),
        (1007, 'Cachorro', 'Boston terrier'),
        (1008, 'Cachorro', 'Boxer'),
        (1009, 'Cachorro', 'Buldogue francês'),
        (1010, 'Cachorro', 'Buldogue inglês'),
        (1011, 'Cachorro', 'Bull terrier'),
        (1012, 'Cachorro', 'Cane corso'),
        (1013, 'Cachorro', 'Cavalier king charles spaniel'),
        (1014, 'Cachorro', 'Chihuahua'),
        (1015, 'Cachorro', 'Chow chow'),
        (1016, 'Cachorro', 'Cocker spaniel inglês'),
        (1017, 'Cachorro', 'Dachshund'),
        (1018, 'Cachorro', 'Dálmata'),
        (1019, 'Cachorro', 'Doberman'),
        (1020, 'Cachorro', 'Dogo argentino'),
        (1021, 'Cachorro', 'Dogue alemão'),
        (1022, 'Cachorro', 'Fila brasileiro'),
        (1023, 'Cachorro', 'Golden retriever'),
        (1024, 'Cachorro', 'Husky siberiano'),
        (1025, 'Cachorro', 'Jack russell terrier'),
        (1026, 'Cachorro', 'Labrador retriever'),
        (1027, 'Cachorro', 'Lhasa apso'),
        (1028, 'Cachorro', 'Lulu da pomerânia'),
        (1029, 'Cachorro', 'Maltês'),
        (1030, 'Cachorro', 'Mastiff inglês'),
        (1031, 'Cachorro', 'Mastim tibetano'),
        (1032, 'Cachorro', 'Pastor alemão'),
        (1033, 'Cachorro', 'Pastor australiano'),
        (1034, 'Cachorro', 'Pastor de Shetland'),
        (1035, 'Cachorro', 'Pequinês'),
        (1036, 'Cachorro', 'Pinscher'),
        (1037, 'Cachorro', 'Pit bull'),
        (1038, 'Cachorro', 'Poodle'),
        (1039, 'Cachorro', 'Pug'),
        (1040, 'Cachorro', 'Rottweiler'),
        (1041, 'Cachorro', 'Schnauzer'),
        (1042, 'Cachorro', 'Shar-pei'),
        (1043, 'Cachorro', 'Shiba'),
        (1044, 'Cachorro', 'Shih tzu'),
        (1045, 'Cachorro', 'Staffordshire bull terrier'),
        (1046, 'Cachorro', 'Weimaraner'),
        (1047, 'Cachorro', 'Yorkshire'),
        (2001, 'Gato', 'Abissínio'),
        (2002, 'Gato', 'American Bobtail'),
        (2003, 'Gato', 'American Curl'),
        (2004, 'Gato', 'American Shorthair'),
        (2005, 'Gato', 'American Wirehair'),
        (2006, 'Gato', 'Asiático'),
        (2007, 'Gato', 'Australian Mist'),
        (2008, 'Gato', 'Bombaim'),
        (2009, 'Gato', 'British Shorthair'),
        (2010, 'Gato', 'Burmês'),
        (2011, 'Gato', 'Burmilla'),
        (2012, 'Gato', 'Cornish Rex'),
        (2013, 'Gato', 'Devon Rex'),
        (2014, 'Gato', 'Don Sphynx'),
        (2015, 'Gato', 'German Rex'),
        (2016, 'Gato', 'Havana'),
        (2017, 'Gato', 'Khao Manee'),
        (2018, 'Gato', 'Korat'),
        (2019, 'Gato', 'Kurilian Bobtail'),
        (2020, 'Gato', 'Manx'),
        (2021, 'Gato', 'Mau Egípcio'),
        (2022, 'Gato', 'Munchkin'),
        (2023, 'Gato', 'Ocicat'),
        (2024, 'Gato', 'Oriental'),
        (2025, 'Gato', 'Peterbald'),
        (2026, 'Gato', 'Pixiebob'),
        (2027, 'Gato', 'Russo'),
        (2028, 'Gato', 'Seychellois'),
        (2029, 'Gato', 'Siamês'),
        (2030, 'Gato', 'Singapura'),
        (2031, 'Gato', 'Snowshoe'),
        (2032, 'Gato', 'Sokoke'),
        (2033, 'Gato', 'Tonquinês'),
        (2034, 'Gato', 'LaPerm'),
        (2035, 'Gato', 'Maine Coon'),
        (2036, 'Gato', 'Neva Masquerade'),
        (2037, 'Gato', 'Norueguês da Floresta'),
        (2038, 'Gato', 'Ragamuffin'),
        (2039, 'Gato', 'Ragdoll'),
        (2040, 'Gato', 'Sagrado da Birmânia'),
        (2041, 'Gato', 'Scottish Fold'),
        (2042, 'Gato', 'Scottish Straight'),
        (2043, 'Gato', 'Selkirk Rex'),
        (2044, 'Gato', 'Siberiano'),
        (2045, 'Gato', 'Somali'),
        (2046, 'Gato', 'Van Turco'),
        (2047, 'Gato', 'Vankedisi'),
        (2048, 'Gato', 'Angorá'),
        (2049, 'Gato', 'Bobtail Japonês'),
        (2050, 'Gato', 'Chartreux'),
        (2051, 'Gato', 'Cymric'),
        (2052, 'Gato', 'Balinês'),
        (2053, 'Gato', 'British Longhair'),
        (2054, 'Gato', 'Persa')"""),
    'ANIMAL': (
        """insert into ANIMAL (cod_animal, id_raca, nome, cor, peso_kg, porte, tipo_sangue) values
        (1, '1000', 'Babalu', 'Bege', 6.5, 'Pequeno', null),
        (2, '2009', 'Mingau', 'Cinza', 4.9, 'Pequeno', null),
        (3, '1036', 'Fiona', 'Bege', 2.1, 'Pequeno', null),
        (4, '1018', 'Meg', 'Preto', 18.45, 'Grande', null),
        (5, '2010', 'Mel', 'Branco', 4.3, 'Pequeno', null),
        (6, '1001', 'Bolt', 'Bege', 13.6, 'Médio', null),
        (7, '2039', 'Jujuba', 'Branco e Cinza', 7.5, 'Pequeno', 'AB'),
        (8, '2035', 'Acerola', 'Cinza', 16.8, 'Grande', null),
        (9, '2000', 'Pudim', 'Alaranjado', 3.5, 'Pequeno', null),
        (10, '1040', 'Thor', 'Preto e Amarelo', 21.3, 'Grande', null)"""),
    'LOCAL': (
        """insert into LOCAL (id_local, endereco, bairro, cep, cidade, uf) values
        (0001, 'Rua Ernesto Alves', 'Jardim Felicidade', '15052-363', 'São José do Rio Preto', 'SP'),
        (0002, 'Rua General Glicério', 'Centro', '15051-400', 'São José do Rio Preto', 'SP'),
        (0003, 'Rua  7 de Setembro', 'Jardim São José', '15130-250', 'Mirassol', 'SP'),
        (0004, 'Rua  Miguel Râmia', 'Boa Vista', '15047-205', 'São José do Rio Preto', 'SP'),
        (0005, 'Rua Abraão Thomé', 'Vila Moreira', '15132-020', 'Mirassol', 'SP')"""),
    'ANIMAL_RESGATE': (
        """insert into ANIMAL_RESGATE (data_resgate, cod_animal, id_local, descricao) values ('2022-03-29', 1, 0002, 
        'Resgatado sozinho em um terreno baldio. Com muita fome mas sem lesões'), ('2022-04-07', 2, 0001, 'Resgatado 
        ainda filhote, sozinho em um mercearia abandonada. Sem presença de lesões'), ('2022-04-13', 3, 0003, 
        'Encontrado junto com outro cachorro perto ao estacionamento do supermercado atacadão. Sem presença de 
        lesões, porém com muita fome'), ('2022-04-13', 4, 0003, 'Encontrado junto com outro cachorro perto ao 
        estacionamento do supermercado atacadão. Com bastante fome e apresentanco alguns arranhados de briga com 
        outro animal'), ('2022-05-17', 5, 0005, 'Estava presente em um terreno baldio, fugindo de fogos de 
        artifício'), ('2022-05-24', 6, 0005, 'Resgatado de uma casa abandonada, estava preso a uma coleira e com 
        bastante fome.'), ('2022-05-28', 7, 0003, 'Resgatado próxima a estrada de terra, vítima de ataque de 
        cachorro. Muitas lesões'), ('2022-06-03', 8, 0004, 'Encontrado dentro do bueiro perto da casa número 59. Sem 
        lesões'), ('2022-06-10', 9, 0002, 'Filhote encontrado perto da praça Albuquerque. Sem lesões'), 
        ('2022-06-12', 10, 0004, 'Encontrado em uma chácara, vítima de mals tratos pelos donos')"""),
    'ADOTANTE': (
        """insert into ADOTANTE (cod_adotante, documento, nome, email, telefone, endereco, bairro, cep, cidade, 
        uf) values (1, '111.222.333-44', 'Adotante 1', 'adotante1@gmail.com', '(17)99887-7665', 
        'Rua Ernesto Alves, 890', 'Jardim Felicidade', '15052-363', 'São José do Rio Preto', 'SP'), (2, 
        '123.456.789-09', 'Adotante 2', 'adotante2@gmail.com', '(17)99774-4321', 'Alameda Rio de Janeiro, 
        230', 'Residecial das Faculdades', '15042-660', 'Mirassol', 'SP'), (3, '987.654.321-00', 'Adotante 3', 'adotante3@gmail.com', '(17)98143-4356', 'Rua Amerildo Rossinante, 59', 
        'Vila Orquídea', '15230-440', 'São José do Rio Preto', 'SP'), (4, '112.233.445-56', 'Adotante 4', 
        'adotante4@gmail.com', '(17)99723-4458', 'Rua 15 de Setembro', 'Centro', '66502-789', 'São José do Rio 
        Preto', 'SP')"""),
    'ADOCAO': (
        """insert into ADOCAO (cod_animal, cod_adotante, data_adocao) values
        (1, 4, '2022-05-08'),
        (2, 1, '2022-06-26'),
        (8, 3, '2022-07-16'),
        (7, 2, '2022-07-17'),
        (10, 2, '2022-07-17')"""),
    'FISCAL': (
        """insert into FISCAL (cod_fiscal, nome) values
        (01, 'Valentino Souza Soares'),
        (02, 'Amanda Vasconcelos Almeida'),
        (03, 'Carolina Dantes da Silva')"""),
    'BO': (
        """insert into BO (id_bo, data_bo, descricao) values
        (0001, '2022-07-17', 'Adotante advertido por manter o animal adotado em um espaço muito pequeno')"""),
    'FICALIZACAO': (
        """insert into FISCALIZACAO (id_bo, cod_adotante, cod_fiscal) values
        (0001, 4, 3)"""),
    'RACAO': (
        """insert into RACAO (id_racao, marca, tipo_animal, qtde_kg_estoque) values
        (1001, 'Foster Premium', 'Cachorro', 30),
        (1002, 'GranPlus', 'Cachorro', 48),
        (2001, 'Whiskas', 'Gato', 54),
        (2002, 'GranPlus', 'Gato', 33)"""),
    'ANIMAL_RACAO': (
        """insert into ANIMAL_RACAO (cod_animal, id_racao, qtde_kg_mensal) values
        (1, 1001, 3),
        (2, 2001, 1.5),
        (3, 1001, 3),
        (4, 1001, 1.5),
        (5, 2001, 4),
        (6, 1001, 3.8),
        (7, 2001, 3),
        (8, 2001, 5),
        (9, 2001, 3),
        (10, 1001, 6),
        (1, 1002, 2),
        (3, 1002, 1.5),
        (5, 2002, 2.5),
        (7, 2002, 2.5),
        (9, 2002, 2.5)"""),
    'FORNECEDOR': (
        """insert into FORNECEDOR (cod_fornecedor, nome, telefone) values
        (1, 'Helder Henrique da Silva', '(17)99887-7665'),
        (2, 'Raphaela Cristina Camilo Santana', '(17)98143-4356'),
        (3, 'Jorge Larcerda de Ramos', '(18)99987-4587')"""),
    'DOACAO': (
        """insert into DOACAO (data_doacao, id_racao, cod_fornecedor, qtde_kg) values
        ('2022-05-05', 1001, 1, 10),
        ('2022-06-05', 1002, 1, 10),
        ('2022-07-05', 2002, 1, 10),
        ('2022-06-15', 2001, 2, 25),
        ('2022-07-17', 1001, 3, 8)"""),
    'CLINICA': (
        """insert into CLINICA (id_clinica, nome, telefone) values
        (001, 'Amicão', '(17)3225-1063'),
        (002, 'Cida Veterinária', '(17)3225-3838'),
        (004, 'Amigato', '(17)3253-4488')"""),
    'CONSULTA': (
        """insert into CONSULTA (id_consulta, cod_animal, id_clinica, data_ida, data_volta, valor) values
        (1, 1, 001, '2022-04-01', '2022-04-05', '600'),
        (2, 2, 004, '2022-04-08', '2022-04-14', '250'),
        (3, 3, 002, '2022-04-14', '2022-04-18', '150'),
        (4, 4, 002, '2022-04-14', '2022-04-18', '150'),
        (5, 5, 004, '2022-05-18', '2022-05-24', '400'),
        (6, 6, 001, '2022-05-25', '2022-05-30', '900'),
        (7, 7, 002, '2022-05-29', '2022-06-04', '350'),
        (8, 8, 004, '2022-06-04', '2022-06-08', '1100'),
        (9, 9, 002, '2022-06-11', '2022-06-17', '270'),
        (10, 10, 002, '2022-06-13', '2022-06-20', '580')"""),
    'VACINA': (
        """insert into VACINA (cod_vacina, descricao) values
        (101, 'V8'),
        (102, 'V10'),
        (103, 'Leishmaniose'),
        (104, 'Gripe Canina'),
        (105, 'Giárdia'),
        (201, 'V3'),
        (202, 'V4'),
        (203, 'V5'),
        (301, 'Antirrábica')"""),
    'REGISTRO_VACINA': (
        """insert into REGISTRO_VACINA (id_consulta, cod_vacina) values
        (1, 102),
        (1, 103),
        (1, 105),
        (1, 301),
        (2, 203),
        (2, 301),
        (3, 102),
        (4, 102),
        (5, 202),
        (5, 301),
        (6, 101),
        (6, 103),
        (6, 104),
        (6, 105),
        (6, 301),
        (7, 202),
        (7, 301),
        (8, 102),
        (8, 301),
        (9, 202),
        (10, 102),
        (10, 103),
        (10, 105),
        (10, 301)""")
}

# Valores para deletar as tabelas
drop = {'REGISTRO_VACINA': (
    "drop table REGISTRO_VACINA"),
    'VACINA': (
        "drop table VACINA"),
    'CONSULTA': (
        "drop table CONSULTA"),
    'CLINICA': (
        "drop table CLINICA"),
    'DOACAO': (
        "drop table DOACAO"),
    'FORNECEDOR': (
        "drop table FORNECEDOR"),
    'ANIMAL_RACAO': (
        "drop table ANIMAL_RACAO"),
    'RACAO': (
        "drop table RACAO"),
    'FICALIZACAO': (
        "drop table FISCALIZACAO"),
    'BO': (
        "drop table BO"),
    'FISCAL': (
        "drop table FISCAL"),
    'ADOCAO': (
        "drop table ADOCAO"),
    'ADOTANTE': (
        "drop table ADOTANTE"),
    'ANIMAL_RESGATE': (
        "drop table ANIMAL_RESGATE"),
    'LOCAL': (
        "drop table LOCAL"),
    'ANIMAL': (
        "drop table ANIMAL"),
    'RACA': (
        "drop table RACA")
}

# Valores para teste de update
update = {'ADOTANTE': (
    """update ADOTANTE
        SET endereco ='Rua Joana Pereira Nazario, 289',
        bairro = 'Coloninha',
        cep = '88906-660',
        cidade = 'Ararangua',
        uf = 'SC'
        where cod_adotante = 1"""),
    'ANIMAL': (
        """update ANIMAL
        SET tipo_sangue = 'A'
        where cod_animal = 8"""),
    'ANIMAL_RACAO': (
        """update ANIMAL_RACAO
        SET qtde_kg_mensal = 5.25
        where cod_animal = 5 and id_racao = 2002"""),
    'CONSULTA': (
        """update CONSULTA
        SET valor = 550.25
        where cod_animal = 5"""),
}

# Valores para teste de delete
delete = {'ANIMAL_RACAO': (
    """delete from ANIMAL_RACAO
        where id_racao = 2002 or id_racao = 1002"""),
    'DOACAO': (
        """delete from DOACAO
        where id_racao = 2002 or id_racao = 1002"""),
    'RACAO': (
        """delete from RACAO
        where id_racao = 2002 or id_racao = 1002""")
}


# Funções
def connect_resgatocao():
    cnx = mysql.connector.connect(host='localhost', database='ong', user='root', password='master')
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
            print("Drop {}: ".format(drop_name), end='')
            cursor.execute(drop_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    #connect.commit()
    cursor.close()


def create_all_tables(connect):
    print("\n---CREATE ALL TABLES---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Criando tabela {}: ".format(table_name), end='')
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
                print("Para criar a tabela: {}, foi utilizado o seguinte código {}".format(table_name,
                                                                                           table_description))
        atributo = input("Digite o atributo a ser alterado: ")
        valor = input("Digite o valor a ser atribuído: ")
        codigo_f = input("Digite a coluna da chave primária: ")
        codigo = input("Digite o valor numérico do campo da chave primária: ")
        query = ['UPDATE ', name, ' SET ', atributo, ' = ', valor, ' WHERE ', codigo_f, '= ', codigo]
        sql = ''.join(query)
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
            print("Inserindo valores para {}: ".format(insert_name), end='')
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
            print("Teste de atualização de valores para {}: ".format(update_name), end='')
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
            print("Teste de atualização de valores para {}: ".format(delete_name), end='')
            cursor.execute(delete_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def consulta1(connect):
    select_query = """
    select vacina.mes, vacina.total_vacina, despesa.despesa_veterinario
    from (
	(select monthname(cons.data_volta) as mes, count(reg_vac.cod_vacina) as total_vacina
	from ANIMAL as ani, CONSULTA as cons, REGISTRO_VACINA as reg_vac
	where ani.cod_animal = cons.cod_animal and cons.id_consulta = reg_vac.id_consulta and ani.porte = 'Pequeno' and
		cons.data_volta between '2022-04-01' and '2022-06-30'
	group by mes) as vacina,
	(select monthname(cons.data_volta) as mes, sum(cons.valor) as despesa_veterinario
	from ANIMAL as ani, CONSULTA as cons
	where ani.cod_animal = cons.cod_animal and ani.porte = 'Pequeno' and
		cons.data_volta between '2022-04-01' and '2022-06-30'
	group by mes) as despesa)
    where vacina.mes = despesa.mes
    """
    print("Primeira Consulta: Projeta a quantidade de vacinas aplicadas nos animais pequenos de abril até junho, "
          "assim como o valor total de despesa nesses meses. A consulta deve projetar o mês, a quantidade de vacinas e "
          "a soma dos valores.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def consulta2(connect):
    select_query = """
    select extract(month from ani_res.data_resgate) as n_mes, monthname(ani_res.data_resgate) as mes_resgate_animal, 
	    count(adoc.cod_animal) as qtde_adocao
    from ADOCAO as adoc
        inner join ANIMAL as ani on adoc.cod_animal = ani.cod_animal
        inner join ANIMAL_RESGATE as ani_res on ani.cod_animal = ani_res.cod_animal
    where ani_res.data_resgate between '2022-03-01' and '2022-06-30'
    group by mes_resgate_animal, n_mes
    order by n_mes
    """
    print("\nSegunda Consulta: Projeta a quantidade de animais adotados que foram resgatados no segundo trimestre de "
          "2022.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def consulta3(connect):
    select_query = """
    select ani.cod_animal, ani.nome as animal, adot.nome as adotante, avg(ani_rac.qtde_kg_mensal) as consumo_medio
    from ANIMAL_RACAO as ani_rac, ANIMAL as ani, ADOCAO as adoc, ADOTANTE as adot
    where ani_rac.cod_animal = ani.cod_animal and
        ani.cod_animal = adoc.cod_animal and
        adoc.cod_adotante = adot.cod_adotante
    group by ani.cod_animal, ani.nome, adot.nome
    order by adot.nome, consumo_medio desc
    """
    print("\nTerceira Consulta: Apresenta a média de ração consumida pelos animais que foram adotados.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def consulta_extra(connect):
    select_query = """
    select vac.descricao as vacina, count(reg_vac.cod_vacina) as qtde_total_vacina
    from VACINA as vac
        inner join REGISTRO_VACINA as reg_vac on vac.cod_vacina = reg_vac.cod_vacina
        inner join CONSULTA as cons on reg_vac.id_consulta = cons.id_consulta
    where cons.data_volta between '2022-01-01' and '2022-07-18'
    group by vac.descricao
    order by vac.descricao
    """
    print("\nConsulta Extra: Apresenta a quantidade total de cada vacina aplicada no primeiro semestre de 2022.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def exit_db(connect):
    print("\n---EXIT DB---")
    connect.close()
    print("Conexão com o banco de dados foi encerrada!")


def crud_resgatocao(connect):
    drop_all_tables(connect)
    create_all_tables(connect)
    insert_test(connect)

    print("\n---CONSULTAS BEFORE---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    consulta_extra(connect)

    update_test(connect)
    delete_test(connect)

    print("\n---CONSULTAS AFTER---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    consulta_extra(connect)


# Main
try:
    # Estabelece Conexão com o DB
    con = connect_resgatocao()

    power_up = 1
    while power_up == 1:
        interface = """\n       ---MENU---
        1.  CRUD RESGATOCAO
        2.  TESTE - Create all tables
        3.  TESTE - Insert all values
        4.  TESTE - Update
        5.  TESTE - Delete
        6.  CONSULTA 01
        7.  CONSULTA 02
        8.  CONSULTA 03
        9.  CONSULTA EXTRA
        10. CONSULTA TABELAS INDIVIDUAIS
        11. UPDATE VALUES
        12. CLEAR ALL RESGATOCAO
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
            crud_resgatocao(con)

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
            consulta_extra(con)

        if choice == 10:
            show_table(con)

        if choice == 11:
            update_value(con)

        if choice == 12:
            drop_all_tables(con)

    con.close()

except mysql.connector.Error as err:
    print("Erro na conexão com o banco de dados!", err.msg)