import threading
import random

DIM_BUFFER = 7
N_PRODUTTORI = 4
N_CONSUMATORI = 3
N_RICHIESTE = 4

buffer = [None] * DIM_BUFFER
metti = 0
togli = 0

vuoto = threading.Semaphore(DIM_BUFFER)
pieno = threading.Semaphore(0)
mutexP = threading.Semaphore(1)
mutexC = threading.Semaphore(1)


def genera_drone():
    return f"DRN-{random.randint(100, 999)}"


class ProduttoreThread(threading.Thread):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx

    def run(self):
        global metti
        while(True):
            vuoto.acquire()
            mutexP.acquire()
            i_metti = metti
            metti=(metti + 1) % DIM_BUFFER
            mutexP.release()
            buffer[i_metti] = self.dato
            print(f"DRN-{self.idx} segnala {genera_drone()} in buffer {i_metti}")
            self.dato += 1
            
            pieno.release()



class ConsumatoreThread(threading.Thread):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx

    # DA IMPLEMENTARE (run)
    def run(self):
        global togli
        while(True):
            if(dato==None):
                print(f"sentinella di terminazione")
                continue
            else:
                pieno.acquire()
                mutexC.acquire()
                i_togli = togli
                togli = (togli + 1) % DIM_BUFFER
                mutexC.release()
                dato = buffer[i_togli]
                print(f"DRN-{self.idx} autorizza atterraggio {genera_drone()}")
                
                vuoto.release()

def main():
    global metti

    produttori = [ProduttoreThread(i + 1) for i in range(N_PRODUTTORI)]
    consumatori = [ConsumatoreThread(i + 1) for i in range(N_CONSUMATORI)]

    # DA IMPLEMENTARE: start dei thread produttori e consumatori
    for c in consumatori:
        c.start()
    for p in produttori:
        p.start()
    # DA IMPLEMENTARE: join di tutti i produttori
    for p in produttori:
        p.join()
    print("Tutti i sensori hanno terminato. Chiusura piste...")

    # Invia una sentinella None per ogni pista attiva.
    for _ in range(N_CONSUMATORI):
        # DA IMPLEMENTARE: inserire None nel buffer
        vuoto.acquire()
        buffer[metti] = None
        metti = (metti + 1) % DIM_BUFFER
        pieno.release()  
        pass
    # DA IMPLEMENTARE: join di tutti i consumatori
    for c in consumatori:
            c.join
    print("Torre operativa chiusa.")
   
if __name__ == "__main__":
    main()
