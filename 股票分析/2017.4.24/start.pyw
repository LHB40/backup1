import threading
import Stock
import update

def a():
    a=Stock.inter()
def b():
    update.update('Stock.pyw')
def c():
    update.update('抬头型.py')
threading.Thread(target=a,).start()
threading.Thread(target=b,).start()
