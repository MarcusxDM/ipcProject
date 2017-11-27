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
arrozFilter     = ['QUEBRADO', 'SEMEADURA', '1006', 'BAÚS', 'MALAS']
mulatinhoFilter = ['SEMEADURA', 'UNGUICULATA', 'CAJANUS', 'GUANDO']



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

def pofFinder(pof_descript, filter_list, ncm_descript):
    '''
    Finds its NCM correlative and saves it
    :param pof_descript filter_list:
    :return:
    '''

    pof = Pof.objects.get(descript=pof_descript)
    ncm_list = csvNcmParser("ncmtable/Tabela_NCM.csv", ncm_descript.upper())
    print ncm_list

    for ncm in ncm_list:
         ncm_normalized_descript = normalizer(ncm.descript)
         print "\nessa porra:"
         print ncm_normalized_descript
         if any(word in ncm_normalized_descript for word in filter_list):
            print "nao passou"
         else:
            print "passou"
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

    pofFinder("Arroz", arrozFilter, "Arroz")
    pofFinder("Feijão - mulatinho", mulatinhoFilter, "feijão")









