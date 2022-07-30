import csv

def generate_csv_data():
    # generate addition data
    with open('data/addition.csv', 'w') as f:
        add = range(2, 101)
        id = 1
        f.write("addend1,addend2,sum\n")
        for m in add:
            for n in add:
                if n >= m:
                    f.write(f"{m},{n},{m + n}\n")
                    id += 1

    # generate multiplication data
    with open('data/multiplication.csv', 'w') as f:
        multiply = range(2, 16)
        id = 1
        f.write("multiplier,multiplicand,product\n")
        for m in multiply:
            for n in multiply:
                if n >= m:
                    f.write(f"{m},{n},{m * n}\n")
                    id += 1

    # generate subtraction data
    with open('data/addition.csv', 'r') as f:
        with open('subtraction.csv', 'w') as out:
            header = "minuend,subtrahend,difference\n"
            out.write(header)
            dr = csv.DictReader(f)
            for line in dr:
                data = f"{line['sum']},{line['addend2']},{line['addend1']}\n"
                out.write(data)

    # generate division data
    with open('data/multiplication.csv', 'r') as f:
        with open('division.csv', 'w') as out:
            header = "dividend,divisor,quotient\n"
            out.write(header)
            dr = csv.DictReader(f)
            for line in dr:
                data = f"{line['product']},{line['multiplicand']},{line['multiplier']}\n"
                out.write(data)

def generate_all_data():
    add = []
    mult = []
    result = []
    # generate addition data
    add_rng = range(1, 101)
    for m in add_rng:
        for n in add_rng:
            if n >= m:
                tmp = ('addition', m, n, m+n)
                add.append(tmp)
                result.append(tmp)

    # generate multiplication data
    mult_rng = range(1, 101)
    for m in mult_rng:
        for n in mult_rng:
            if n >= m:
                tmp = ('multiplication', m, n, m * n)
                mult.append(tmp)
                result.append(tmp)

    # generate subtraction data
    for item in add:
        tmp = ('subtraction',item[3], item[2], item[1])
        result.append(tmp)

    # generate division data
    for item in mult:
        tmp = ('division',item[3], item[2], item[1])
        result.append(tmp)
    return result

if __name__=='__main__':
    data = generate_all_data()
    print(f"type(data) = {type(data)}")
    print(f"len(data) = {len(data)}")