
# Folkloro ansamblio valdymo sistema
## Sistemos paskirtis
Sistema skirta palengvinti folkloro ansamblio narių bei vadovų kasdienius organizacinius darbus t.y. koncertų, vakaronių veiklų planavimą, šokių, dainų saugojimą, koncertinių ar vakaronių programų dalinimasi, bendravimą

Taikomosios srities objektai: Padalinys -> Ansamblis -> Narys

## Funkciniai reikalavimai
### 1. Naudotojų valdymas:
- Prisijungimas ir atsijungimas naudojant OAuth2 autentifikaciją.
- Rolės: Administratorius, Vadovas (Moderator), Naudotojas.
### 2. Padalinių valdymas:
- CRUD funkcionalumas (sukurti, peržiūrėti, atnaujinti, ištrinti) prieinamas administratoriams ir moderatoriams.
- Naudotojai gali tik peržiūrėti padalinių sąrašą.
### 3. Ansamblių valdymas:
- CRUD funkcionalumas prieinamas tik administratoriui.
- Moderatoriai ir naudotojai gali peržiūrėti ansamblių sąrašą.
### 4. Narių valdymas:
- CRUD funkcionalumas prieinamas tik administratoriui.
- Moderatoriai gali peržiūrėti narių sąrašą.
### 5. Pagrindinis puslapis:
- Pritaikytas funkcionalumas pagal naudotojo rolę.
- Patogus valdymas naudojant navigacijos mygtukus ir animuotus perėjimus.


### Papildomai (bus pildoma):
1. Laiko valdymas t.y. vadovai gali suvesti koncertų datas
2. Naudotojai gali koncerto laiką persikelti į Google Calendar ar Outlook calendar
3. Šokiai turi būti suskirstyti pagal požymius
4. Vadovai gali išsitraukti šokių pagal požymius ataskaitą
   

## Pasirinktų technologijų aprašymas
Python su Django karkasu ir PostgreSQL
YAML failas - projekte
Host'inimas ir deploy'inimas: Azure
Šiuo metu projektas pasiekiamas: [folklore.azurewebsites.net](https://folklore.azurewebsites.net)

## Projekto paleidimas
Norėdami paleisti sistemą vietiniame serveryje:
`git clone https://github.com/Whyytas/Folklore-Management-System.git`
`cd FolkloreManagementSystem`
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py runserver`
Pasiekite sistemą adresu: `http://127.0.0.1:8000` arba `http://localhost:8000`

## Diegimo diagrama
![Model](https://github.com/user-attachments/assets/aec81acb-0418-49ed-9fcf-cfde3581e21c)

## API specifikacija
- Lokaliai http://localhost:8000/swagger/
- .yaml failas projekte

## Naudotojo sąsaja
https://www.figma.com/design/t4uqSTTv1HeBZqXIYHUpqX/Folklore?node-id=0-1&t=RRy9pcdLJH0IqnWO-1

## Išvados:
-   Sistema sėkmingai realizuota su **Django** framework'u.
-   **OAuth2** autentifikacijos dėka užtikrintas saugus prisijungimas ir vartotojų rolės valdymas.
-   Naudotojo sąsaja yra pritaikyta **mobiliesiems įrenginiams** ir optimizuota patogiam valdymui.
-   Administratorius turi pilną prieigą prie duomenų valdymo, o naudotojams ir moderatoriams suteikti riboti leidimai.
-   Sukurtas lengvai plečiamas ir palaikomas projektas.
