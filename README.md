# Shelved
## Opis projekta
Shelved služi kao TBR (To Be Read) lista. Na popis knjiga koje korisnik želi pročitati knjige će se moći dodavati, uređivati i brisati. Također, popis će se moći sortirati po želji i filtrirati po žanru. Preko search bara bit će omogućeno pretraživanje prema ključnoj riječi. Korisnik će preko pie charta moći pregledavati statistiku dodanih žanrova na popis.

## Funkcionalnosti
- prikaz svih knjiga na TBR listi
- sortiranje knjiga prema: naslovu, autoru, žanru, izdavaču, godini izdanja i broju stranica
- filtriranje prema žanru
- gumb za poništavanje sortiranja/filtera
- pretraživanje preko trake za pretraživanje
- forma za dodavanje knjiga
- uređivanje i brisanje knjiga s popisa
- pregled statistike žanrova dodanih knjiga

## Pokretanje aplikacije
### Preuzimanje aplikacije s GitHub-a
```
cd ~/Downloads
git clone https://github.com/msol0/Shelved
cd shelved
```

### Docker - pokretanje
```
docker build --tag shelved:3.1 .
docker run -p 5000:5000 shelved:3.1
```
### Kako lokalno pokrenuti aplikaciju?
1. u preglednik upisati http://localhost:5000
2. u terminalu otvoriti link koji se prikaže prilikom pokretanja
3. u Docker Desktopu otvoriti link containera u kojem se aplikacija izvodi
