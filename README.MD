# Aplicatie de budgetare 
Aplicatie consta intr-un program scris in python, care cu ajutorul lui mysql ofera peristenta datelor. Utilizatorii pot sa seteze in cate zile este perioada de budgetare, cati bani au in fiecare zi ssmd.
Instructiuni de folosire:
- Set budget duration : ii se da numarul de zile si o sa se afiseze numarul de bari aferent
- Convert : Se schimba unitatea sumei in moneda precizata optiunile sunt Leu ,Dollar, Euro
- Add a note: Primul lucru este numarul zilei, si dupaia vine mesajul
- Add repated purchase i,j,k: incepand de la ziua i la fiecare j zile platesc costul k
- Set money left for a day: primul lucru este ziua (numar) si dupaia cat bani mai ai in acea zi (numar real)
- Display trend i j: se afiseaza o best fit line pentru zilele i,j , pentru a prezice daca te vei incadra in targetul de budgetare

### Screenshot cu UI

![alt text](image-1.png)

## [Demo offline](/demo/2024-06-11%2020-19-33.mkv)
### Backlogul cu user stories:
https://trello.com/b/xGQJSRWC/proiect-gestionare-buget

### Diagrama UML
![alt text](<Untitled Diagram.drawio-1.png>)


### Diagrama Bazei de date
![alt text](image.png)

### Prompt engineering 
Prompt:
![alt text](image-3.png)

Resultat (codul a fost modificat putin ca sa se incadreze in aplicatie):
![alt text](image-4.png)

### Teste automate

(implementat in metoda test_update_value in new.py)

### Rapoarte bug

(vezi backlog pentru descrierea bugului)
Comiturile care le rezolva:
Bugul 1 -> https://github.com/FIRCALiviu/MDS/commit/522a7e770f3db7d73dadef29e06be44192093d24
Bugul 2 -> https://github.com/FIRCALiviu/MDS/commit/87d51cd9212e2f9092f1a7eeaf797ada65b05373
Bugul 3 -> https://github.com/FIRCALiviu/MDS/commit/fe19ba626bd2d80936c976bcc66f09a365a83712
Bugul 4 -> https://github.com/FIRCALiviu/MDS/commit/7a799729a702652b307d5b1bdcea57c59e6e05d1
### Refactoring

Before:
![alt text](<Screenshot from 2024-06-11 16-20-45.png>)

After:
![alt text](image-6.png)