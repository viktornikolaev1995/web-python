import requests
from decimal import Decimal
from currency import convert


correct = Decimal('3754.8057')
result = convert(Decimal("1000.1000"), 'RUR', 'JPY', "17/02/2005", requests)
if result == correct:
    print("Correct", f'result: {result}', f'correct: {correct}')
else:
    print("Incorrect: %s != %s" % (result, correct))


relative_unit_cur_from = Decimal(28.0016 / 1)
relative_unit_cur_to = Decimal(26.6352 / 100)
amount = Decimal(1000.1)
correct = Decimal(amount * relative_unit_cur_from / relative_unit_cur_to)
correct_quantize = correct.quantize(Decimal("1.0000"))
result = convert(Decimal("1000.1000"), 'USD', 'JPY', "17/02/2005", requests)
if result == correct_quantize:
    print("Correct", f'result: {result}', f'correct: {correct_quantize}')
else:
    print("Incorrect: %s != %s" % (result, correct_quantize))