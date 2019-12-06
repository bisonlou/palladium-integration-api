import sys
from api import app
from flask import jsonify, abort, request
from api.database import (
    get_department_totals, get_gratuity_totals, get_advace_totals)


@app.route('/')
def index():
    if not request.json:
        abort(400, "json data required")

    month = request.json.get('month', None)
    year = request.json.get('year', None)
    journal_date = request.json.get('journal_date', None)

    error = False
    try:
        GOUS = get_department_totals('GOU', 'Support', month, year)
        GOUR = get_department_totals('GOU', 'Research', month, year)
        gratuity = get_gratuity_totals(month, year)
        GOURadvances = get_advace_totals('GOU', 'Research', month, year)
        GOUSadvances = get_advace_totals('GOU', 'Support', month, year)

        # Net donor wise
        with open('NetPay.txt', 'w') as net_file:
            net_file.write(
                journal_date + ',"7","PAYE For December ' + year + '"\n')

            # GOU Support NET
            net_file.write('92000000,' + str(-GOUS[0][0]) + '\n')
            net_file.write('24000005,' + str(GOUS[0][0]) + '\n')

            # GOU Research PAYE
            net_file.write('92000000,' + str(-GOUR[0][0]) + '\n')
            net_file.write('24000005,' + str(GOUR[0][0]))

        with open('PAYE.txt', 'w') as paye_file:
            paye_file.write(
                journal_date + ',"7","PAYE For December ' + year + '"\n')

            # GOU Support PAYE
            paye_file.write('93000001,' + str(-GOUS[0][3]) + '\n')
            paye_file.write('20000005,' + str(GOUS[0][3]) + '\n')

            # GOU Research PAYE
            paye_file.write('93000001,' + str(-GOUR[0][3]) + '\n')
            paye_file.write('20000005,' + str(GOUR[0][3]))

        with open('NSSF.txt', 'w') as paye_file:
            paye_file.write(
                journal_date + ',"7","NSSF For December ' + year + '"\n')

            # GOU Support NSSF 10%
            paye_file.write('93000002,' + str(-GOUS[0][1]) + '\n')
            paye_file.write('20000005,' + str(GOUS[0][1]) + '\n')

            # GOU Support NSSF 5%
            paye_file.write('93000002,' + str(-GOUS[0][2]) + '\n')
            paye_file.write('20000007,' + str(GOUS[0][2]) + '\n')

            # GOU Research NSSF 10%
            paye_file.write('93000002,' + str(-GOUR[0][1]) + '\n')
            paye_file.write('20000005,' + str(GOUR[0][1]) + '\n')

            # GOU Research NSSF 5%
            paye_file.write('93000002,' + str(-GOUR[0][2]) + '\n')
            paye_file.write('20000007,' + str(GOUR[0][2]))

        with open('LST.txt', 'w') as lst_file:
            lst_file.write(
                journal_date + ',"7","LST For December ' + year + '"\n')

            # GOU Support LST
            lst_file.write('93000003,' + str(-GOUS[0][4]) + '\n')
            lst_file.write('20000005,' + str(GOUS[0][4]) + '\n')

            # GOU Research LST
            lst_file.write('93000003,' + str(-GOUR[0][4]) + '\n')
            lst_file.write('20000005,' + str(GOUR[0][4]))

        with open('Gratuity.txt', 'w') as gratuity_file:
            gratuity_file.write(
                journal_date + ',"7","Gratuity For December ' + year + '"\n')

            # Gratuity
            gratuity_file.write('94000000,' + str(-gratuity[0][0]) + '\n')
            gratuity_file.write('24000010,' + str(gratuity[0][0]))

        with open('Advances.txt', 'w') as advances_file:
            advances_file.write(
                journal_date + ',"7","Gratuity For December ' + year + '"\n')

            # individual GOU Support advances
            GOUSadvances_total = 0
            for advance in GOUSadvances:
                advances_file.write('94000000,' + str(-advance[1]) + '\n')
                GOUSadvances_total += advance[1]

            # print GOU Support total
            advances_file.write('24000010,' + str(GOUSadvances_total) + '\n')

            # individual GOU Research advances
            GOURadvances_total = 0
            for advance in GOURadvances:
                advances_file.write('94000000,' + str(-advance[1]) + '\n')
                GOURadvances_total += advance[1]

            # print GOU Research total
            advances_file.write('24000010,' + str(GOURadvances_total))

    except Exception:
        error = True
        print(sys.exc_info())
    finally:
        net_file.close()

    if not error:
        return jsonify({
            'success': True,
            'month': month,
            'year': year,
        }), 200

    return jsonify({
        'success': False,
        'month': month,
        'year': year,
    }), 422
