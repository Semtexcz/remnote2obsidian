# Dokumentace JSON exportu RemNote

Tento dokument popisuje obsah JSON souborů ve složce exportu `RemNoteExport_Semtex_json_2026-04-22_11-35`.
Popis vychází z reálně nalezených dat v této složce, ne z obecného popisu formátu.

## Přehled exportu

Export obsahuje 8 JSON souborů:

- `rem.json`
- `cards.json`
- `user_data.json`
- `knowledge_base_data.json`
- `knowledgebase_local_stored_data.json`
- `local_stored_data.json`
- `spaced_repetition_scheduler.json`
- `metadata.json`

Velikostí a významem se soubory dělí na dvě skupiny:

- `rem.json` je hlavní databázový export znalostní báze. Obsahuje `72 679` záznamů.
- Ostatní soubory obsahují pomocná nebo specializovaná data: karty, uživatelské preference, lokální stav, konfiguraci scheduleru a metadata exportu.

## Společný obal většiny souborů

Většina JSON souborů má stejnou vrchní strukturu:

```json
{
  "userId": "...",
  "knowledgebaseId": "...",
  "name": "...",
  "exportDate": "...",
  "exportVersion": 2,
  "docs": [...]
}
```

Tento obal používají:

- `rem.json`
- `cards.json`
- `user_data.json`
- `knowledge_base_data.json`
- `knowledgebase_local_stored_data.json`
- `local_stored_data.json`
- `spaced_repetition_scheduler.json`

Význam polí:

- `userId`: identifikátor uživatele.
- `knowledgebaseId`: identifikátor znalostní báze.
- `name`: název exportu nebo báze.
- `exportDate`: datum vytvoření exportu.
- `exportVersion`: verze exportního formátu.
- `docs`: vlastní datové záznamy.

`metadata.json` je výjimka. Neobsahuje `docs`, ale metadata o exportu, synchronizaci, zařízení a uživateli.

## Společné rysy záznamů v `docs`

Napříč soubory se opakují některá technická pole:

- `_id`: interní identifikátor dokumentu.
- `owner`: vlastník dokumentu, obvykle ID uživatele nebo lokální owner typu `browser`.
- `createdAt`: čas vytvoření.
- `m`: čas poslední změny nebo interní modifikační timestamp.
- `o`, `u`, `y`, `z`: interní synchronizační a verzovací metadata.

U mnoha polí se vyskytují i dvojice typu `field,u` nebo `field,o`. Z dat je vidět, že jde o doprovodná metadata ke konkrétnímu poli, nejspíš čas synchronizace, pořadí operace nebo merge metadata. Přesný význam nelze bez interní dokumentace RemNote potvrdit, ale pro běžné čtení exportu je lze obvykle ignorovat.

## Soubory

## `metadata.json`

Účel:

- metadata o vytvoření exportu
- stav synchronizace Rem a karet
- informace o zařízení a uživateli

Top-level klíče:

- `version`
- `remSync`
- `cardSync`
- `time`
- `date`
- `device`
- `user`

Co obsahuje:

- verzi aplikace, zde `1.25.19`
- poslední časy synchronizace pro Rem data a karty
- informace o zařízení, např. `userAgent`, `platform`, `deviceName`
- profil uživatele, včetně `username`, `email`, `createdAt`

Poznámka:

- tento soubor je citlivý, protože obsahuje osobní údaje a identifikátory účtu

## `rem.json`

Účel:

- hlavní export obsahu znalostní báze
- strom remů, bloků, definic, portálů, vyhledávání a dalších interních objektů

Struktura:

- obal s `docs`
- `docs` obsahuje `72 679` záznamů

Nejdůležitější pole, která se často objevují:

- `_id`: ID remu nebo interního objektu
- `parent`: rodičovský rem
- `key`: obsah titulku nebo klíčové strany remu
- `value`: obsah hodnoty, odpovědi nebo druhé strany
- `children`, `subBlocks`: vazby na podřízené bloky
- `references`, `portalsIn`, `searchResults`: různé referenční vazby
- `type`: interní kategorie objektu
- `k`: textový složený klíč, často ve formátu `parentId.text`
- `x`: pořadí nebo interní index v databázi

Pozorování k poli `key` a `value`:

- někdy jde o prosté pole řetězců, např. `["Vlastnosti m-árních vyhledávacích stromů"]`
- jindy obsahují strukturované fragmenty, např. odkazy na jiné remy:

```json
[
  {
    "i": "q",
    "_id": "..."
  }
]
```

To znamená, že text v exportu nemusí být vždy čistý string. Při parsování je potřeba počítat s bohatým interním formátem.

### Kategorie záznamů podle `type`

V `rem.json` se vyskytují čtyři hlavní skupiny:

- bez `type`: `53 873` záznamů
- `type = 1`: `1 549` záznamů
- `type = 2`: `13 307` záznamů
- `type = 6`: `3 950` záznamů

Význam typů není v exportu přímo popsán. Z dat lze ale rozumně odhadnout:

- záznamy bez `type` jsou běžné remy nebo bloky stromu
- `type = 1` vypadá jako remy se speciálním významem ve vyhledávání nebo type systému
- `type = 2` často obsahuje `value`, `forget` a odkazy v `key`; působí jako kartové nebo relation objekty
- `type = 6` často obsahuje `portalType`, `searchResults`, `embeddedSearchId` nebo `t`; působí jako portály, embedded search nebo interní pomocné objekty

Tyto interpretace jsou odhadnuté z dat, ne potvrzené oficiální specifikací.

### Praktická interpretace `rem.json`

Pro většinu analytických úloh je vhodné číst `rem.json` jako graf:

- uzel identifikuje `_id`
- stromovou vazbu nese `parent`
- obsah bývá v `key` a případně `value`
- boční vazby jsou v `references`, `portalsIn`, `typeParents`, `searchResults`

Pokud chceš rekonstruovat běžný obsah poznámek, je `rem.json` nejdůležitější soubor.

### Obrázky a soubory v `rem.json`

V exportu jsou přítomné i přílohy a obrázky. Z dat jsou přímo vidět dvě reprezentace:

- lokální placeholdery typu `%LOCAL_FILE%...`
- přímé URL na assety typu `https://remnote-user-data.s3.amazonaws.com/...`

To znamená:

- některé remy nebo jejich embedded struktury odkazují na soubory přes dočasný nebo lokální identifikátor
- jiné už obsahují finální URL na uložený soubor

Příklady pozorované v datech:

```text
%LOCAL_FILE%Y8nQ45-x1qtH3pl9Q4hULJy6A18AbC7X65CrHrIyGMQHpPabBIGRYSgmKRrMT-Ry6Vg_TD3CyK1Ka0WGEga7KKIbuFIi7Y0cyAgmd9Rg_Rw5vLNzCFP37TfX94AEuQVT.pdf
https://remnote-user-data.s3.amazonaws.com/u78TiRBjup5DbzEL-ufd3SKPddCFDipgSUhXNZDqny8C8ylE94Z8UtsZBh_zebkac80hbSLqFCnYqg7Id4oB-kv5UpriG-Xdn7ORJzIg68MU-ypufAShy2nqQhstCSke.pdf
https://remnote-user-data.s3.amazonaws.com/VB4pnpqbqS9zdX41Aq1FjF5wXHzWTDIw13CG4G9xnuPHiyogC7bUG0TGPO8Zim3GsRUu8HPY3TPqE24SafhLEGKiDS2wJse2xF5Qs3EW8fgqmMHwW3_fER7y6V-7VsvI.png
```

V některých záznamech je obrázek uložen i jako vnořená struktura s polem `imageUrl`, například:

```json
{
  "content": {
    "imageBlob": {},
    "imageUrl": "https://remnote-user-data.s3.amazonaws.com/..."
  }
}
```

Z tohoto exportu tedy lze potvrdit:

- obrázky a soubory nejsou jen mimo export, ale jejich reference jsou uložené přímo v `rem.json`
- finální odkazy směřují na bucket `remnote-user-data.s3.amazonaws.com`
- v exportu se vyskytují soubory typu `png`, `jpeg`, `svg`, `pdf` a také alespoň jeden `html` soubor

K otázce CDN:

- z exportu lze přímo potvrdit uložení na S3, protože URL vedou na `remnote-user-data.s3.amazonaws.com`
- z tohoto exportu nelze spolehlivě potvrdit, že se při běžném provozu používá ještě další CDN vrstva
- jinými slovy: v exportu je jistá S3 adresa, nikoli explicitně CDN hostname

## `cards.json`

Účel:

- export stavů spaced repetition karet

Počet záznamů:

- `3 652`

Typická pole:

- `_id`: ID karty
- `rId`: ID remu, ke kterému karta patří
- `c`: interní stav karty
- `ml`: textový learning stage
- `createdAt`: vytvoření karty
- `st`: další naplánovaný čas
- `e`, `n`, `p`, `u`, `m`, `o`, `y`, `z`: interní scheduling a sync metadata

Pozorované hodnoty:

- `ml`:
  - `New`: `3 625`
  - `Growing`: `24`
  - `Acquiring`: `3`
- `c`:
  - `f`: `2 479`
  - `b`: `1 163`
  - několik ojedinělých numerických nebo textových hodnot po 1 výskytu

Vazba na `rem.json`:

- `rId` odkazuje na `_id` v `rem.json`
- `cards.json` obsahuje `2 494` unikátních `rId`
- jeden rem tedy může mít více karet

To dobře odpovídá tomu, že jeden obsahový rem může generovat více kartových reprezentací.

## `spaced_repetition_scheduler.json`

Účel:

- konfigurace schedulerů pro spaced repetition

Počet záznamů:

- `14`

Typická pole:

- `_id`: ID konkrétního scheduleru
- `st`: typ scheduleru, např. `default` nebo `sm2`
- `ift`, `eb`, `se`, `ei`, `lni`, `im`, `md`: numerické parametry scheduleru

Pozorování:

- většina záznamů má `st = "default"`
- alespoň jeden záznam má `st = "sm2"`
- v `knowledge_base_data.json` je klíč `spacedRepetitionSchedulerId`, který odkazuje na jeden z `_id` v tomto souboru

Z toho plyne:

- soubor neobsahuje jen jeden scheduler, ale více konfigurací
- znalostní báze z nich vybírá aktivní přes ID

## `user_data.json`

Účel:

- uživatelské preference, usage telemetry, lokální i cloudové pomocné stavy navázané na účet

Počet záznamů:

- `746`

Typická struktura záznamu:

```json
{
  "_id": "...",
  "key": "usage.tagFeature",
  "value": {
    "count": 80,
    "lastUsed": "2022-08-31T08:25:37.859Z"
  },
  "owner": "..."
}
```

Typy hodnot v `value`:

- `object`: `470`
- `null`: `142`
- `boolean`: `76`
- `number`: `29`
- `array`: `16`
- `string`: `13`

Příklady klíčů:

- `usage.*`: usage/telemetrie funkcí
- `sharedArticleSRSData`
- `deviceTrackerNested`
- `dailyBackup.syncDates`
- `activeMinutes2`
- `aiCallLogs`
- `aiChatModel`

Interpretace:

- nejde o obsah poznámek
- jde hlavně o účetní a provozní metadata uživatele

## `knowledge_base_data.json`

Účel:

- per-knowledge-base konfigurace sdílená na úrovni báze

Počet záznamů:

- `119`

Struktura:

- key-value dokumenty

Typická pole:

- `_id`
- `key`
- `value`
- `v`
- `owner`

Příklady klíčů:

- `spacedRepetitionSchedulerId`
- `migradeDarkModeToDropdown`
- mnoho položek `hasMigratedAccountV...`

Interpretace:

- migrační příznaky databáze
- nastavení nebo feature flags svázané se znalostní bází
- odkazy na další konfigurační entity, zejména scheduler

## `knowledgebase_local_stored_data.json`

Účel:

- lokální key-value data svázaná s konkrétní knowledge base

Počet záznamů:

- `7`

Příklady klíčů:

- `finishedSignUpFirstLoad`
- `lastSearch`
- `legacyRemMigrationsCompleted`
- `filesWaitingToUpload`
- `filesWaitingToUploadRoutesDict`
- `consumerJobStartPoint.<userId>.ExistingRem`
- `consumerJobStartPoint.<userId>.DeletedRem`

Interpretace:

- přechodový lokální stav UI a synchronizace
- evidence souborů čekajících na upload
- checkpointy background jobů

Pozor:

- `filesWaitingToUploadRoutesDict` obsahuje velké mapy lokálních názvů souborů a rout typu `upload`, `upload_pdf`, `upload_import`
- tento soubor je důležitý i pro pochopení příloh, protože mapuje lokální placeholdery `%LOCAL_FILE%...` na upload workflow

## `local_stored_data.json`

Účel:

- obecná lokální data zařízení nebo klienta

Počet záznamů:

- `17`

Příklady klíčů:

- `deviceId`
- `lastSeenTime`
- `lastUpdatedDesktopApp`
- `newDarkMode`
- `learningPageOpenEditorId`
- `clipboardRems`
- `clipboardPortalId`

Interpretace:

- nastavení a stav konkrétní instalace nebo browser session
- data, která nemusejí být sdílená mezi zařízeními

Zajímavost:

- owner bývá `browser`, nikoli uživatelské ID

## Vazby mezi soubory

### 1. `cards.json` -> `rem.json`

- `cards.docs[].rId` odpovídá `rem.docs[]._id`
- karta tedy neobsahuje plný obsah sama o sobě, ale odkazuje na hlavní rem

### 2. `knowledge_base_data.json` -> `spaced_repetition_scheduler.json`

- klíč `spacedRepetitionSchedulerId` obsahuje ID aktivního scheduleru
- toto ID odpovídá některému `_id` v `spaced_repetition_scheduler.json`

### 3. `metadata.json` -> ostatní soubory

- obsahuje kontext exportu, verzi klienta, synchronizaci a identitu uživatele
- je vhodný jako vstupní bod pro validaci, kdy a čím byl export pořízen

## Doporučené pořadí při analýze

Pokud chceš data dál zpracovávat programově, dává smysl tento postup:

1. Načíst `metadata.json` a získat kontext exportu.
2. Načíst `rem.json` jako hlavní zdroj obsahu.
3. Připojit `cards.json` přes `rId -> _id`.
4. Připojit `spaced_repetition_scheduler.json` přes `spacedRepetitionSchedulerId`.
5. `user_data.json`, `local_stored_data.json` a `knowledgebase_local_stored_data.json` používat až jako doplňková metadata.

## Co je jisté a co je odhad

Jisté z dat:

- názvy souborů, jejich počty záznamů a vrchní struktura
- existence vazby `cards.rId -> rem._id`
- existence vazby `knowledge_base_data.spacedRepetitionSchedulerId -> spaced_repetition_scheduler._id`
- to, že `metadata.json` obsahuje sync a device metadata
- to, že přílohy a obrázky jsou v exportu reprezentované přes `%LOCAL_FILE%...` placeholdery a přes přímé URL na `remnote-user-data.s3.amazonaws.com`

Odhadnuté z obsahu:

- přesný význam mnoha krátkých interních polí jako `o`, `u`, `y`, `z`, `x`, `p`
- přesná semantika `type = 1`, `2`, `6`
- přesný význam stavového pole `c` v `cards.json`
- zda je nad S3 v běžném provozu nasazená ještě samostatná CDN vrstva; z exportu to samo o sobě potvrdit nelze

Tyto body by šlo potvrdit jen proti interní dokumentaci RemNote nebo zdrojovým kódům aplikace.
