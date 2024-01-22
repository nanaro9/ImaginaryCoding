# Programmas autors - Aleksis Počs
# Izstrādāta 5. tēmas ietvaros

SN_LIKME = 0.105
IIN_LIKME = 0.2
IIN_LIKME2 = 0.23
DD_SN_LIKME = 0.2359
APGADAJAMO_LIKME = 250
ALGAS_LIKME = 1667

def formula(bruto_alga,bernu_sk):
    if bruto_alga < ALGAS_LIKME:
        sn = bruto_alga * SN_LIKME
        Atvieglojums = bernu_sk * APGADAJAMO_LIKME
        iin = (Atvieglojums - sn) * IIN_LIKME
        neto_alga = bruto_alga - sn - iin
        return neto_alga
    else:
        sn = bruto_alga * SN_LIKME
        Atvieglojums = bernu_sk * APGADAJAMO_LIKME
        iin_baze = (Atvieglojums - sn)
        return sn
    
print(formula(2000,2))