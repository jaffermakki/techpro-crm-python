from decimal import Decimal

PROVINCES = {
    'AB': {'taxType':'GST', 'gst':5, 'pst':0, 'hst':0},
    'BC': {'taxType':'GST+PST', 'gst':5, 'pst':7, 'hst':0},
    'MB': {'taxType':'GST+PST', 'gst':5, 'pst':7, 'hst':0},
    'NB': {'taxType':'HST', 'gst':0, 'pst':0, 'hst':15},
    'NL': {'taxType':'HST', 'gst':0, 'pst':0, 'hst':15},
    'NS': {'taxType':'HST', 'gst':0, 'pst':0, 'hst':15},
    'NT': {'taxType':'GST', 'gst':5, 'pst':0, 'hst':0},
    'NU': {'taxType':'GST', 'gst':5, 'pst':0, 'hst':0},
    'ON': {'taxType':'HST', 'gst':0, 'pst':0, 'hst':13},
    'PE': {'taxType':'HST', 'gst':0, 'pst':0, 'hst':15},
    'QC': {'taxType':'GST+QST', 'gst':5, 'pst':9.975, 'hst':0},
    'SK': {'taxType':'GST+PST', 'gst':5, 'pst':6, 'hst':0},
    'YT': {'taxType':'GST', 'gst':5, 'pst':0, 'hst':0},
}

def calc_canadian_tax(amount, province_code):
    p = PROVINCES.get(province_code, PROVINCES['ON'])
    amount = Decimal(amount)
    if p['taxType'] == 'HST':
        hst = round(amount * Decimal(p['hst'] / 100), 2)
        return {'gst':0, 'pst':0, 'hst':hst, 'total': amount + hst,
                'lines': [{'label':f'HST {p["hst"]}%', 'amount':hst}]}
    elif p['taxType'] == 'GST+PST':
        gst = round(amount * Decimal(p['gst'] / 100), 2)
        pst = round(amount * Decimal(p['pst'] / 100), 2)
        return {'gst':gst, 'pst':pst, 'hst':0, 'total': amount+gst+pst,
                'lines': [{'label':f'GST {p["gst"]}%', 'amount':gst},
                          {'label':f'PST {p["pst"]}%', 'amount':pst}]}
    else:  # GST only
        gst = round(amount * Decimal(p['gst'] / 100), 2)
        return {'gst':gst, 'pst':0, 'hst':0, 'total': amount+gst,
                'lines': [{'label':f'GST {p["gst"]}%', 'amount':gst}]}
