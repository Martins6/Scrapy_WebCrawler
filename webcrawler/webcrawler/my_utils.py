# Title: Utilities objects and functions
# Author: Adriel Martins

pt_month_abv = 'jan. fev. mar. abr. maio. jun. jul. ago. set. out. nov. dez. '
pt_month_abv = pt_month_abv.split('. ')[:-1]
print(pt_month_abv)

en_month_abv = 'Jan. Feb. Mar. Apr. May. Jun. Jul. Aug. Sep. Oct. Nov. Dec. '
en_month_abv = en_month_abv.split('. ')[:-1]
print(en_month_abv)

def month_pt_to_en(month_pt):
    index = pt_month_abv.index(month_pt)
    print(index)
    return en_month_abv[index]