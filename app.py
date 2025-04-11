from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_import_cost(cc, co2, fuel_type, euro_norm, purchase_price, is_new):
    # Insert your existing calculation code here
    global efk, tax
    # For simplicity, I'll use your previous example calculation
    # Replace with your original function logic as needed
    if fuel_type == 'petrol':
        if cc <= 1600:
            efk = 500
        elif cc <= 2000:
            efk = 1800
        else:
            efk = 2500
    elif fuel_type == 'diesel':
        if cc <= 1600:
            efk = 700
        elif cc <= 2000:
            efk = 2200
        else:
            efk = 3000
    elif fuel_type == 'petrol/electric':
        if cc < 2000 and co2 < 50:
            efk = 0
        elif cc < 2000 and co2 <= 122:
            efk = 950
        else:
            efk = 1500
    elif fuel_type == 'diesel/electric':
        if cc < 2000 and co2 < 50:
            efk = 950
        elif cc < 2000 and co2 <= 122:
            efk = 1100
        elif cc < 2500:
            efk = 2200
        else:
            efk = 3000
    else:
        efk = 0

    if fuel_type == 'petrol/electric' or fuel_type == 'diesel/electric':
        if cc < 2000:
            if co2 < 50:
                tax = 0
            elif co2 <= 122:
                tax = 1400
            else:
                tax = 3000
        elif cc < 2500:
            if co2 < 50:
                tax = 0
            elif co2 <= 122:
                tax = 1400
            elif co2 <= 140:
                tax = 2500
            else:
                tax = 3000
    else:
        if co2 <= 100:
            tax = 500
        elif co2 <= 120:
            tax = 1000
        elif co2 <= 140:
            tax = 2500
        elif co2 <= 160:
            tax = 4000
        else:
            tax = 5000

    # Calculate VAT and total cost
    if is_new:
        vat = 0.24 * (purchase_price + efk)
    else:
        vat = 0

    misc_fees = 250

    total = efk + tax + vat + misc_fees

    return {
        'ΕΦΚ': efk,
        'Τέλος Ταξινόμησης': tax,
        'ΦΠΑ': round(vat, 2),
        'Λοιπά Έξοδα': misc_fees,
        'Συνολικό Κόστος Εκτελωνισμού': round(total, 2)
    }

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    cc = int(request.form['cc'])
    co2 = int(request.form['co2'])
    fuel_type = request.form['fuel_type']
    euro_norm = request.form['euro_norm']
    purchase_price = float(request.form['purchase_price'])
    is_new = 'is_new' in request.form

    result = calculate_import_cost(cc, co2, fuel_type, euro_norm, purchase_price, is_new)

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
