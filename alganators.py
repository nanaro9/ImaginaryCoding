# Programmas autors - Aleksis Počs
# Izstrādāta 5. tēmas ietvaros

SN_LIKME = 0.105 # Konstanta Sociālā nodokļa likme 10.5%
IIN_LIKME = 0.2 # Konstanta Iedzīvotāja ienākuma nodokļa likme 20%
IIN_LIKME2 = 0.23 # Konstanta Iedzīvotāja ienākuma nodokļa likme 23%
DD_SN_LIKME = 0.2359 # Konstanta Darba devēja sociālā nodokļa likme 23.59%
APGADAJAMO_LIKME = 250 # Likme par katru apgādājamo personu 250 eiro
ALGAS_LIKME = 1667 # Likme pēc kuras pienākas papildus nodoklis

def algas_formula(bruto_alga,bernu_sk):
    if bruto_alga <= ALGAS_LIKME:
        sn = bruto_alga * SN_LIKME
        atvieglojums = bernu_sk * APGADAJAMO_LIKME
        iin_baze = bruto_alga - sn - atvieglojums
        iin = iin_baze * IIN_LIKME
        neto_alga = bruto_alga - sn - iin
        return neto_alga
    else:
        sn = bruto_alga * SN_LIKME
        atvieglojums = bernu_sk * APGADAJAMO_LIKME
        iin_baze = ALGAS_LIKME - sn - atvieglojums
        iin = iin_baze * IIN_LIKME
        parpalikums = bruto_alga - ALGAS_LIKME
        iin2 = parpalikums * IIN_LIKME2
        neto_alga = bruto_alga - sn - iin - iin2
        return neto_alga
    
print(algas_formula(2000,2))