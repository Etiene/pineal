from pineal.parser import parse

def generate_config():
    config = parse()
    with open('pineal/config.py','w') as f:
        for k,v in config.items():
            printable = '\''+v+'\'' if isinstance(v,basestring) else str(v)
            f.write(k + ' = ' + printable + '\n')

def main():
    generate_config()

    from pineal.config import MODULES
    classes = [
        __import__(m.lower(), globals(), locals(), [m], -1).__dict__[m]
        for m in MODULES
    ]
    procs = [Cl() for Cl in classes]

    for p in procs:
        p.start()

    try:
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        print
        procs.reverse()
        for p in procs:
            p.stop()
            p.join()
