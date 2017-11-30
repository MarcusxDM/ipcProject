# -*- coding: utf8 -*-

'''
Created on 24/11/2017

@author: Marcus Vinicius
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ipcProject.settings'
import django
import csv
django.setup()
from ncmxpof.models import Ncm, Pof

# Alphabet:
chars = set('abcdefghijklmnopqrstuvxwyz')

# Filter Lists:
arrozFilter        = ['QUEBRADO', 'SEMEADURA', '1006', 'BAÚS', 'MALAS']

mulatinhoFilter    = ['SEMEADURA', 'UNGUICULATA', 'ADZUKI',
                      'ANGULARIS', 'CAJANUS', 'CAJAN', 'GUANDO'
                      'SUBTERRANEA', 'VOANDZEIA']

farinhaArrozFilter = ['MILHO']

macarraoFilter     = ['CUSCUZ"']

flocosMilhoFilter  = ['AVEIA"']

batataInglesFilter = ['OUTROS"', 'MANGARITOS', 'TAROS', 'DIOSCOREA', 'MANDIOCA"']

inhameFilter       = ['OUTROS"', 'MANGARITOS', 'TAROS', 'BATATASDOCES"', 'MANDIOCA"']

mandiocaFilter     = ['OUTROS"', 'MANGARITOS', 'TAROS', 'BATATASDOCES"', 'DIOSCOREA']

tomateFilter       = ['SUCOS']

cebolaFilter       = ['SEMEADURA']

ovoFilter          = ['INCUBA\xc3\xa7\xc3\xa3O']

condensadoFilter   = ['DESNATADO', 'INTEGRAL']


def csvNcmParser(csv_fileUrl, ncm_descript):
    '''
    Recieves a csv URL, extracts code and description
    :param csv_fileUrl:
    :return ncm_list:
    '''
    ncm_list = []
    ncm      = Ncm()
    with open(csv_fileUrl) as csv_file:
        spamreader = csv.reader(csv_file, delimiter=';')
        # Going from row to row in the csv_file
        for row in spamreader:
            ncm.cod = int(row[0])
            del row[0]
            fullDescript = ''
            for collumn in row:
                # checking for collumns with more description info
                # adding to @fullDescript
                if any((c in chars) for c in collumn):
                    fullDescript = fullDescript+''+collumn
                else:
                    break
                ncm.descript = fullDescript

            if ncm_descript in ncm.descript.upper():
                new_ncm = ncmRefresher(ncm)
                ncm_list.append(new_ncm)

    return ncm_list

def queryToList(querySet):
    list_a = []
    for object in querySet:
        list_a.append(object['ncm__cod'])
    return list_a

def pofFinder(pof_descript, filter_list, ncm_descript):
    '''
    Finds its NCM correlative and saves it
    :param pof_descript filter_list:
    :return:
    '''

    pofs = Pof.objects.filter(descript=pof_descript)
    ncm_list = csvNcmParser("ncmtable/Tabela_NCM.csv", ncm_descript.upper())
    print ncm_list
    print "\n"

    for pof in pofs:
        print "#######################\nPOF: ", pof.cod, pof.descript
        for ncm in ncm_list:
            ncm_query = Pof.objects.filter(ncm__cod=ncm.cod, cod=pof.cod).values('ncm__cod')
            ncm_query = queryToList(ncm_query)
            print "NCM: ", ncm.cod, ncm.descript
            if ncm.cod in ncm_query:
                print ncm_query
                print "NCM already linked to POF\n"
                break
            else:
                ncm_normalized_descript = normalizer(ncm.descript)
                print "\nNCM KEY WORDS:"
                print ncm_normalized_descript
                if any(word in ncm_normalized_descript for word in filter_list):
                    print "didn't passed\n"
                else:
                    print "passed\n"
                    new_ncm     = ncmRefresher(ncm)
                    new_ncm.pof = pof
                    new_ncm.save()

def normalizer(string):
    string = string.upper().replace('(', ' ').replace(')', ' ').replace(':', '')
    string_list = string.replace(',', '').replace('-', '').replace('.', '').split()
    return string_list

def ncmRefresher(ncm):
    '''
    Clones a NCM to another to avoid memory garbage
    :param  ncm:
    :return new_ncm:
    '''
    new_ncm          = Ncm()
    new_ncm.cod      = ncm.cod
    new_ncm.descript = ncm.descript
    return new_ncm

if __name__ == '__main__':

    # pofFinder("Arroz", arrozFilter, "Arroz")
    # pofFinder("Feijão - mulatinho", mulatinhoFilter, "feijão")
    # pofFinder("Feijão - macassar (Fradinho)", [], "fradinho")
    # pofFinder("Feijão - carioca (rajado) ", mulatinhoFilter, "feijão")
    # pofFinder("farinha de arroz", farinhaArrozFilter, "Farinhas de cereais, exceto de trigo ou de "
                                                      #"mistura de trigo com centeio (méteil)")

    # pofFinder("macarrão", macarraoFilter, "Massas alimentícias, mesmo cozidas")

    # pofFinder("fubá de milho ", [], "Farinhas de cereais, exceto de trigo ou de mistura"
                                    #" de trigo com centeio (méteil).- Farinha de milho")

    # pofFinder("flocos de milho", flocosMilhoFilter, "Grãos de cereais trabalhados de outro modo "
                                                    #"(por exemplo, descascados, esmagados, em flocos, "
                                                    #"em pérolas, cortados ou partidos), com exclusão do"
                                                    #" arroz da posição 10.06")

    # pofFinder("farinha de mandioca", [], "Farinhas, sêmolas e pós, dos legumes de vagem,"
    #                                      " secos, da posição 07.13, de sagu ou das raízes"
    #                                      " ou tubérculos da posição 07.14 e dos produtos "
    #                                      "do Capítulo 8.- De sagu ou das raízes ou tubérculos,"
    #                                      " da posição 07.14")


    # pofFinder("Batata-inglesa", batataInglesFilter, "Raízes de mandioca, de araruta e de salepo, tupinambos,"
    #                                                 " batatas-doces e raízes ou tubérculos semelhantes,")


    # pofFinder("Inhame", inhameFilter, "Raízes de mandioca, de araruta e de salepo, tupinambos,"
    #                                         " batatas-doces e raízes ou tubérculos semelhantes,"    )

    # pofFinder("mandioca (aipim)", mandiocaFilter,"Raízes de mandioca, de araruta e de salepo, tupinambos,"
    #                                              " batatas-doces e raízes ou tubérculos semelhantes,"    )

    # pofFinder("Tomate", tomateFilter, "Tomates")

    # pofFinder("Cebola", cebolaFilter, "Cebolas")

    # Açúcares:
    # pofFinder("Açúcar cristal", [], "Açúcares de cana ou de beterraba e sacarose quimicamente pura,
    #                                 " no estado sólido.- Outros:-- Outros")

    # BomBom
    # pofFinder("chocolate em barra e bombom ", [], "Chocolate e outras preparações alimentícias que contenham cacau."
    #                                               "- Outros, em tabletes, barras e paus:-- Recheados - Chocolate")
    # Barra
    # pofFinder("chocolate em barra e bombom ", [], "Chocolate e outras preparações alimentícias que contenham cacau."
    #                                               "- Outros, em tabletes, barras e paus:-- Não recheados - Chocolate")

    # pofFinder("Sorvete ", [], "Sorvetes")

    # pofFinder("Chocolate e achocolatado em pó", [], "Chocolate e outras preparações alimentícias que contenham cacau."
    #                                                 "- Cacau em pó")

    # Hortaliças e Verduras:
    # pofFinder("Alface", [], "Alfaces")

    # pofFinder("Coentro", [], "Outros produtos hortícolas, frescos ou refrigerados.-"
    #                          " Outros:-- Outros - Outros") # needs deeper verification

    # Frutas:

    # pofFinder("banana - da - terra ", [], "Bananas, incluindo as bananas-da-terra, frescas ou secas."
    #                                       "- Bananas-da-terra")

    # pofFinder("abacaxi", [], "Tâmaras, figos, abacaxis (ananases), abacates, goiabas, mangas e mangostões,"
    #                          " frescos ou secos.- Abacaxis (ananases)")

    # pofFinder("banana - prata", [], "Bananas, incluindo as bananas-da-terra, frescas ou secas.- Outras")

    # pofFinder("maçã", [], "Maçãs, peras e marmelos, frescos.- Maçãs")

    # pofFinder("mamão", [], "Melões, melancias e mamões (papaias), frescos."
    #                        "- Mamões (papaias)")

    # pofFinder("manga", [], "Tâmaras, figos, abacaxis (ananases), abacates, goiabas, mangas e mangostões,"
    #                        " frescos ou secos.- Goiabas, mangas e mangostões - Mangas")

    # pofFinder("melancia", [], "Melões, melancias e mamões (papaias), frescos.- Melões e melancias:-- Melancias")

    # pofFinder("uva", [], "Uvas frescas ou secas (passas).- Frescas")

    # pofFinder("laranja - pera", [], "Frutos cítricos, frescos ou secos.- Laranjas") #needs deeper verification

    # Carnes:
    # Fígado Bovino
    # pofFinder("fígado", [], "Miudezas comestíveis de animais das espécies bovina, suína, ovina, caprina, cavalar,"
    #                         " asinina e muar, frescas, refrigeradas ou congeladas.- Da espécie bovina, congeladas:"
    #                         "-- Fígados")
    # Fígado Suíno:
    # pofFinder("fígado", [], "Miudezas comestíveis de animais das espécies bovina, suína, ovina, caprina, cavalar,"
    #                         " asinina e muar, frescas, refrigeradas ou congeladas.-Outros- Da espécie suína,"
    #                         " congeladas:-- Fígados")


    # pofFinder("cupim", [], "Carnes de animais da espécie bovina, congeladas."
    #                        " - Desossadas") # needs deeper verification
    # pofFinder("cupim", [], "Carnes de animais da espécie bovina, frescas ou refrigeradas."
    #                        " - Desossadas") # needs deeper verification

    # pofFinder("contrafilé", [], "Carnes de animais da espécie bovina, frescas ou refrigeradas."
    #                             " - Desossadas") # needs deeper verification
    # pofFinder("contrafilé", [], "Carnes de animais da espécie bovina, congeladas. - Desossadas")

    # pofFinder("chã de dentro", [], "Carnes de animais da espécie bovina, frescas ou refrigeradas."
    #                                " - Desossadas") # needs deeper verification
    # pofFinder("chã de dentro", [], "Carnes de animais da espécie bovina, congeladas. - Desossadas")

    # pofFinder("alcatra", [], "Carnes de animais da espécie bovina, frescas ou refrigeradas."
    #                          " - Desossadas") # needs deeper verification
    # pofFinder("alcatra", [], "Carnes de animais da espécie bovina, congeladas. - Desossadas")


    # pofFinder("patinho", [], "Carnes de animais da espécie bovina, frescas ou refrigeradas."
    #                          " - Desossadas") # needs deeper verification
    # pofFinder("patinho", [], "Carnes de animais da espécie bovina, congeladas."
    #                          " - Desossadas")# needs deeper verification

    # pofFinder("músculo", [], "Carnes de animais da espécie bovina, frescas ou refrigeradas."
    #                          " - Desossadas")  # needs deeper verification
    # pofFinder("músculo", [], "Carnes de animais da espécie bovina, congeladas."
    #                          " - Desossadas")  # needs deeper verification

    # pofFinder("pá", [], "Carnes de animais da espécie bovina, frescas ou refrigeradas."
    #                     " - Desossadas")  # needs deeper verification
    # pofFinder("pá", [], "Carnes de animais da espécie bovina, congeladas."
    #                     " - Desossadas")  # needs deeper verification

    # pofFinder("acém", [], "Carnes de animais da espécie bovina, frescas ou refrigeradas."
    #                       " - Desossadas")  # needs deeper verification
    # pofFinder("acém", [], "Carnes de animais da espécie bovina, congeladas."
    #                       " - Desossadas")  # needs deeper verification

    # pofFinder("costela", [], "-- Toucinhos entremeados e seus pedaços"
    #                          "-- Outras") # needs deeper verification

    # pofFinder("costela", [], "Carnes de animais da espécie bovina, congeladas."
    #                          " - Congeladas:-- Outras") # needs deeper verification


    # Pescados:

    # pofFinder("corvina", [], "Corvina")

    # pofFinder("cavalinha", [], " -- Cavalinhas (Scomber scombrus, Scomber australasicus,"
    #                            " Scomber japonicus)")

    # pofFinder("sardinha", [], "03.04. -- Sardinhas (Sardina pilchardus, Sardinops spp., Sardinella spp.), anchoveta (Sprattus sprattus)")

    # pofFinder("camarão", [], "Camarões")

    # pofFinder("merluza", [], "Merluza")

    # pofFinder("pescada", [], "Pescadas")

    # pofFinder("castanha", [], "- Outros peixes, exceto fígados, ovas e sêmen:Outros")

    # Tilápias
    # pofFinder("tilápia", [], "-- Tilápias (Oreochromis spp.)")
    # pofFinder("tilápia", [], "Tilápias (Tilapia spp., Sarotherodon spp., Danakilia spp.")


    # Carnes e peixes industrializados:

    # pofFinder("salsicha", [], 'Enchidos e produtos semelhantes, de carne,'
    #                           ' de miudezas ou de sangue') # needs deeper verification

    # pofFinder("linguiça ", [], 'Enchidos e produtos semelhantes, de carne,'
    #                            ' de miudezas ou de sangue') # needs deeper verification

    # pofFinder("mortadela", [], 'Enchidos e produtos semelhantes, de carne,'
    #                            ' de miudezas ou de sangue') # needs deeper verification

    # pofFinder("carne seca e de sol ", [], " farinhas e pós, comestíveis, de carnes ou de "
    #                                       "miudezas.- Carnes da"
    #                                       " espécie bovina")  # needs deeper verification

    # # hambuger de frango:
    # pofFinder("hambúrguer", [], "- De aves da posição 01.05:"
    #                             "-- De galos e de galinhas - Outras") # needs deeper verification
    # hamburguer de boi:
    # pofFinder("hambúrguer", [], "Outras preparações e conservas de carne, de miudezas ou de sangue."
    #                            "- Da espécie bovina") # needs deeper verification

    # Aves e ovos:

    # pofFinder("frango inteiro", [], " das aves da posição 01.05.- De galos e de galinhas:"
    #                                 "-- Não cortadas em pedaços")
    # pofFinder("frango em pedaços", [], "das aves da posição 01.05.- De galos e de galinhas:"
    #                                    "-- Pedaços e miudezas")

    # pofFinder("ovo de galinha", ovoFilter, "Ovos de aves, com casca, frescos, conservados ou cozidos.")


    # Leite e derivados:
    # pofFinder("leite longa vida", [], "Leite e creme de leite, não concentrados nem adicionados de açúcar"
    #                                   " ou de outros edulcorantes.Leite UHT (Ultra High Temperature)")

    # pofFinder("leite condensado", condensadoFilter, "Leite e creme de leite, concentrados ou adicionados de açúcar"
    #                                                 " ou de outros edulcorantes. -- Outros") # needs deeper verification

    # pofFinder("leite em pó", [], "Leite e creme de leite, concentrados ou adicionados de açúcar ou de outros"
    #                              " edulcorantes. Leite integral")

    # pofFinder("queijo", [], "Queijos e requeijão.- Queijos frescos (não curados), incluindo o queijo de"
    #                         " soro de leite, e o requeijão")

    # pofFinder("iogurte e bebidas lácteas", [], " açúcar ou de outros edulcorantes, ou aromatizados ou "
    #                                            "adicionados de frutas ou de cacau.")

    # pofFinder("manteiga", [], " - Manteiga")

    # pofFinder("leite com sabor", [], "Leite e creme de leite, não concentrados nem adicionados de açúcar"
    #                                  " ou de outros edulcorantes.Outros") # needs deeper verification

    # Panificados:

    # pofFinder("biscoito", [], " e produtos semelhantes.- Bolachas e biscoitos, adicionados de edulcorante")

    # pofFinder("pão francês", [], "amido ou fécula, em folhas, e produtos semelhantes.- Outros - Outros")

    # pofFinder("bolo", [], "amido ou fécula, em folhas, e produtos semelhantes.- Outros - Outros")

    # Óleos e gorduras:

    # pofFinder("óleo de soja", [], "quimicamente modificados.- Outros - Em recipientes com capacidade "
    #                               "inferior ou igual a 5 litros")

    # pofFinder("margarina", [], "óleos alimentícios e respectivas frações da posição 15.16."
    #                            "- Margarina, exceto a margarina líquida")

    # Bebidas e infusões:
    # pofFinder("suco de frutas", [], "Suco (sumo)")

    # pofFinder("café moído", [], "cascas e películas de café")

    # pofFinder("café solúvel", [], "-- Extratos, essências e concentrados"
    #                               " - Café solúvel, mesmo descafeinado")

    # pofFinder("refrigerante e água mineral", [], "- Águas, incluindo as águas minerais e as "
    #                                              "águas gaseificadas, adicionadas de açúcar"
    #                                              " ou de outros edulcorantes ou aromatizadas") # needs deeper verification

    # pofFinder("cerveja", [], "Cervejas de malte.")

    # "outras bebidas alcoólicas"
    # pofFinder("outras bebidas alcoólicas", [], "misturas de bebidas fermentadas com bebidas não alcoólicas,"
    #                                            " não especificadas nem compreendidas noutras posições.")
    #
    # pofFinder("outras bebidas alcoólicas", [], "Álcool etílico não desnaturado, com um teor alcoólico, em volume")
    #
    # pofFinder("outras bebidas alcoólicas", [], "vinhos")

    # Enlatados e conservas:
    # pofFinder("sardinha em conserva", [], "-- Sardinhas e anchoveta - Sardinhas")

    # pofFinder("salsicha em conserva", [], "Enchidos e produtos semelhantes, de carne,"
    #                                       " de miudezas ou de sangue") # needs deeper verification

    # pofFinder("carne em conserva", [], "de carne, de miudezas ou de sangue.- Da espécie bovina")

    # pofFinder("milho-verde em conserva", [], "Milho doce (Zea mays var. saccharata)")

    # Sal e condimentos:
    # pofFinder("atomatado", [], "exceto em vinagre ou em ácido acético.- Tomates inteiros ou em pedaços")

    # pofFinder("alho", [], ' misturas de produtos hortícolas - Alho em pó')

    # pofFinder("maionese", [], "condimentos e temperos compostos")

    # pofFinder("vinagre", [], "Vinagres e seus sucedâneos obtidos a partir do ácido acético,"
    #                          " para usos alimentares")

    # pofFinder("caldo concentrado", [], "caldos e sopas preparados")

    # pofFinder("tempero misto", [], "condimentos e temperos compostos")

    # "Alimentação fora do domicílio"
    # "Alimentação fora do domicílio"
    # "refeição"
    # "lanche"
    # "café da manhã"
    # "refrigerante e água mineral" # done
    # "cerveja" # done
    # "outras bebidas alcoólicas" # done
    # "doces"
    # "Habitação"
    # "Encargos e manutenção"
    # "Aluguel e taxas"
    # "aluguel residencial"
    # "condomínio"
    # "taxa de água e esgoto"
    # "Reparos"
    # "tinta"
    # "revestimento de piso e parede"
    # "cimento"
    # "tijolo"
    # "material hidráulico"
    # "mão de obra"
    # "areia"
    # "Artigos de limpeza"
    # "água sanitária"
    # "detergente"
    # "sabão em pó"
    # "sabão em barra"
    # "esponja de limpeza"
    # "Combustíveis e energia"
    # "Combustíveis (domésticos)"
    # "gás de botijão"
    # "Energia elétrica residencial"
    # "Energia elétrica residencial"
    # "Artigos de residência"
    # "Móveis e utensílios"
    # "Mobiliário"
    # "Móvel para sala"
    # "Móvel para quarto"
    # "Móvel para copa e cozinha"
    # "Móvel infantil"
    # "Colchão"
    # "Utensílios e enfeites"
    # "tapete"
    # "cortina"
    # "utensílios de metal"
    # "utensílios de vidro e louça"
    # "utensílios de plástico"
    # "utensílios diversos"
    # "Cama, mesa e banho"
    # "roupa de cama"
    # "roupa de banho"
    # "Aparelhos eletroeletrônicos"
    # "Eletrodomésticos e equipamentos"
    # "refrigerador"
    # "máquina de lavar roupa"
    # "liquidificador"
    # "ventilador"
    # "fogão"
    # "TV, som e informática"
    # "televisor"
    # "aparelho de som"
    # "aparelho de DVD"
    # "antena"
    # "microcomputador"
    # "Consertos e manutenção"
    # "Consertos e manutenção"
    # "conserto de refrigerador"
    # "conserto de televisor"
    # "conserto de aparelho de som"
    # "reforma de estofado"
    # "Vestuário"
    # "Roupas"
    # "Roupa masculina"
    # "calça comprida masculina"
    # "short e bermuda masculina"
    # "cueca"
    # "camisa/camiseta masculina"
    # "roupa feminina"
    # "calça comprida feminina"
    # "saia"
    # "vestido"
    # "blusa"
    # "lingerie"
    # "bermuda e short feminino"
    # "Roupa infantil"
    # "calça comprida infantil"
    # "vestido infantil"
    # "bermuda e short infantil"
    # "camisa/camiseta infantil"
    # "conjunto infantil"
    # "Calçados e acessórios"
    # "Calçados e acessórios"
    # "sapato masculino"
    # "sapato feminino"
    # "sapato infantil"
    # "sandália/chinelo masculino"
    # "sandália/chinelo feminino"
    # "sandália/chinelo infantil"
    # "bolsa"
    # "tênis"
    # "Jóias e bijuterias"
    # "Jóias e bijuterias"
    # "bijuteria"
    # "jóia "
    # "relógio de pulso"
    # "Tecidos e armarinho"
    # "Tecidos e armarinho"
    # "tecido "
    # "artigos de armarinho"
    # "Transportes"
    # "Transportes"
    # "Transporte público"
    # "ônibus urbano"
    # "táxi"
    # "ônibus intermunicipal"
    # "ônibus intererstadual"
    # "passagem aérea"
    # "Veículo próprio"
    # "automóvel novo"
    # "emplacamento e licença"
    # "óleo lubrificante"
    # "acessórios e peças"
    # "pneu"
    # "conserto de automóvel"
    # "automóvel usado"
    # "motocicleta"
    # "Combustíveis (veículos)"
    # "gasolina"
    # "etanol"
    # "gás veicular"
    # "Saúde e cuidados pessoais"
    # "Produtos farmacêuticos e óticos"
    # "Produtos farmacêuticos  "
    # "anti-infeccioso e antibiótico"
    # "analgésico e antitérmico"
    # "anti-inflamatório e antirreumático"
    # "antigripal e antitussígeno"
    # "dermatológico"
    # "antialérgico e broncodilatador"
    # "gastroprotetor"
    # "vitamina e fortificante"
    # "hormônio"
    # "psicotrópico e anorexígeno"
    # "hipotensor e hipocolesterolêmico"
    # "oftalmológico"
    # "Produtos óticos"
    # "óculos sem grau"
    # "lentes de óculos e de contato"
    # "Serviços de saúde"
    # "Serviços médicos e dentários"
    # "médico"
    # "dentista"
    # "aparelho ortodôntico"
    # "Serviços laboratoriais e hospitalares"
    # "exame de laboratório"
    # "hospitalização e cirurgia"
    # "exame de imagem"
    # "Plano de saúde"
    # "plano de saúde"
    # "Cuidados pessoais"
    # "Higiene pessoal"
    # "produto para cabelo"
    # "fralda descartável"
    # "produto para pele"
    # "produto para higiene bucal"
    # "produto para unha"
    # "perfume"
    # "desodorante"
    # "absorvente higiênico"
    # "sabonete"
    # "papel higiênico"
    # "artigos de maquiagem"
    # "Despesas pessoais"
    # "Serviços pessoais"
    # "Serviços pessoais"
    # "costureira"
    # "manicure"
    # "cabelereiro"
    # "empregado doméstico"
    # "cartório"
    # "serviço bancário"
    # "Recreação, fumo e fotografia"
    # "Recreação  "
    # "cinema"
    # "CD e DVD"
    # "tratamento de animais"
    # "bicicleta"
    # "alimento para animais"
    # "brinquedo"
    # "locação de DVD"
    # "festas diversas"
    # "jogos de azar"
    # "hotel"
    # "Fumo"
    # "cigarro"
    # "Fotografia e filmagem"
    # "máquina fotográfica"
    # "revelação e cópia"
    # "Educação"
    # "Cursos, leitura e papelaria"
    # "Cursos regulares"
    # "creche"
    # "educação infantil"
    # "ensino fundamental"
    # "ensino médio"
    # "ensino superior"
    # "pós-graduação"
    # "Leitura"
    # "revista"
    # "livro"
    # "Papelaria"
    # "caderno"
    # "fotocópia"
    # "artigos de papelaria"
    # "Cursos diversos"
    # "curso preparatório"
    # "curso de informática"
    # "atividades físicas"
    # "Comunicação"
    # "Comunicação"
    # "Comunicação"
    # "telefone fixo"
    # "telefone celular"
    # "acesso à internet"
    # "aparelho telefônico"
    # "telefone com internet - pacote"







