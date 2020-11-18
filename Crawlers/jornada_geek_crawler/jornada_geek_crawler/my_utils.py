# Title: Utilities objects and functions
# Author: Adriel Martins

pt_month = 'janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro'
pt_month = pt_month.split(' ')

pt_month_abv = 'jan. fev. mar. abr. maio. jun. jul. ago. set. out. nov. dez. '
pt_month_abv = pt_month_abv.split('. ')[:-1]

en_month_abv = 'Jan. Feb. Mar. Apr. May. Jun. Jul. Aug. Sep. Oct. Nov. Dec. '
en_month_abv = en_month_abv.split('. ')[:-1]

def month_pt_to_en(month_pt, abv = True):
    if(abv == True):
        index = pt_month_abv.index(month_pt)
    else:
        index = pt_month.index(month_pt)

    return en_month_abv[index]

def delete_since(arg, obj):
    if type(obj) == str:
        index = obj.index(arg)
    else:
        where_arg_is = map(lambda x: arg in x, obj)
        index = list(where_arg_is).index(True)
    return obj[:index]