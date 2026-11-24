Zajmując się tworzeniem automatyzacji i agentów AI, często spotykam osoby, które nie do końca rozumieją zasadę ich działania. Jedni uważają agenta za zwykłego chatbota, inni traktują go jak cyfrowego pracownika, któremu wystarczy przydzielić zadanie i poczekać na rezultat.

Spróbuję wyjaśnić, jak zbudowane są takie systemy, dlaczego popełniają błędy, od czego zależą koszty ich działania oraz kiedy firma rzeczywiście potrzebuje agenta AI.

Do zrozumienia tego artykułu nie jest potrzebna znajomość programowania.

## Czym jest agent AI?

Załóżmy, że prowadzisz sklep internetowy. Chcesz w każdy poniedziałek otrzymywać informacje o cenach pięciu głównych konkurentów w formie tabeli przesyłanej przez Telegram.

Możesz zlecić takie zadanie ChatGPT podczas rozmowy. Jednak do regularnego, automatycznego wykonywania tej pracy potrzebny będzie system, który ma dostęp do odpowiednich narzędzi, uruchamia się zgodnie z harmonogramem i przesyła wyniki.

Taki system może samodzielnie znaleźć strony konkurencji, przeanalizować ich oferty, zebrać informacje, porównać ceny, przygotować tabelę i wysłać ją użytkownikowi.

Sam model językowy nie otwiera jednak przeglądarki, nie zapisuje plików na dysku i nie loguje się do Telegrama. Operacje te wykonuje oprogramowanie, z którym model jest połączony.

Model językowy określa, co należy zrobić, a kod programu wykonuje odpowiednią operację.

## Z czego składa się agent AI?

W uproszczeniu agent składa się z kilku podstawowych elementów:

- Modelu językowego (LLM), na przykład GPT, Claude lub Gemini.
- Warstwy programowej zarządzającej działaniem modelu.
- Narzędzi do wykonywania konkretnych operacji.
- Mechanizmów przechowywania informacji.
- Reguł, ograniczeń i mechanizmów weryfikacji wyników.

Warstwę programową zarządzającą modelem programiści często określają jako Harness.

Przekazuje ona zadanie modelowi językowemu, odbiera żądania wykonania operacji, uruchamia odpowiednie narzędzia i zwraca wyniki.

Jeżeli agent potrzebuje aktualnej ceny produktu, model może wygenerować żądanie otwarcia odpowiedniej strony. Oprogramowanie pobiera jej zawartość i przekazuje ją modelowi.

Model analizuje otrzymane informacje i określa kolejny krok.

Proces ten może powtarzać się wielokrotnie w ramach jednego zadania.

## Jak agent korzysta z narzędzi?

Załóżmy, że tworzę agenta do analizy konkurencji.

Mogę udostępnić mu następujące narzędzia:

- Wyszukiwanie informacji w internecie.
- Pobieranie zawartości stron internetowych.
- Wykonywanie obliczeń.
- Tworzenie arkuszy kalkulacyjnych.
- Wysyłanie wiadomości przez Telegram.

Każde narzędzie ma określone przeznaczenie, opis i parametry potrzebne do jego uruchomienia.

Gdy model ustali, że należy znaleźć konkurentów, korzysta z narzędzia wyszukiwania. Po otrzymaniu listy stron może pobrać ich zawartość, a następnie przygotować tabelę.

Mechanizm ten nazywa się Tool Calling, czyli wywoływanie narzędzi.

Programista określa, z jakich narzędzi agent może korzystać. Model decyduje, kiedy i w jakim celu użyć dostępnych funkcji.

Jeżeli nie udostępnię agentowi poczty elektronicznej, nie będzie mógł odczytać moich wiadomości za pomocą odpowiedniego narzędzia. Jeżeli nie podłączę Telegrama, agent nie wyśle tam wiadomości.

Możliwości agenta w dużym stopniu zależą od sposobu jego zaprojektowania.

## Czym jest MCP i do czego służy?

Podczas tworzenia agentów często trzeba połączyć ich z zewnętrznymi usługami. Mogą to być Google Drive, Gmail, CRM, GitHub, bazy danych lub wewnętrzne systemy przedsiębiorstwa.

W 2024 roku firma Anthropic przedstawiła otwarty protokół MCP (Model Context Protocol), który ułatwia takie integracje.

Można go porównać do uniwersalnego złącza USB-C.

Zamiast za każdym razem tworzyć osobny mechanizm komunikacji pomiędzy agentem a zewnętrznym systemem, programiści mogą korzystać ze standardowego protokołu.

Serwer MCP obsługujący pocztę może na przykład umożliwiać wyszukiwanie wiadomości, odczytywanie ich zawartości lub tworzenie wersji roboczych.

Agent otrzymuje informacje o dostępnych operacjach i może z nich korzystać podczas wykonywania zadań.

MCP nie zastępuje jednak autoryzacji, nie zwalnia z konieczności konfigurowania uprawnień i sam w sobie nie gwarantuje bezpieczeństwa.

Jest sposobem na standaryzację komunikacji pomiędzy systemem AI a zewnętrznymi narzędziami.

## Czym agent AI różni się od zwykłej automatyzacji?

Załóżmy, że na Twojej stronie znajduje się formularz kontaktowy. Po jego wypełnieniu dane klienta powinny trafić do CRM, a pracownik powinien otrzymać powiadomienie w Telegramie.

Do tego nie potrzeba sztucznej inteligencji.

W n8n można stworzyć prostą automatyzację, która odbierze dane, sprawdzi je, zapisze w CRM i wyśle wiadomość.

Kolejność operacji jest znana z góry. Wynik każdego kroku można sprawdzić zwykłym kodem.

Inaczej wygląda sytuacja, gdy trzeba przeanalizować treść zapytania klienta, określić jego potrzeby, znaleźć odpowiednią usługę, przygotować spersonalizowaną odpowiedź i zdecydować, któremu specjaliście przekazać zgłoszenie.

W takim przypadku zastosowanie modelu językowego może być uzasadnione.

Jeżeli system ma samodzielnie wybierać źródła informacji, narzędzia i kolejność działań zależnie od sytuacji, możemy mówić o podejściu agentowym.

W swojej pracy preferuję łączenie zwykłej automatyzacji ze sztuczną inteligencją.

Tam, gdzie wynik można uzyskać za pomocą kodu, nie ma sensu zużywać zasobów modelu językowego.

## Praktyczny przykład: poranny asystent poczty elektronicznej

Załóżmy, że każdego dnia zaczynasz pracę od przeglądania poczty. W nocy przychodzą wiadomości od klientów, reklamy, faktury, powiadomienia z różnych usług i zwykły spam.

Zamiast codziennie rano przeglądać wszystkie wiadomości, można zautomatyzować ich wstępną analizę.

Każdego dnia o siódmej rano system łączy się ze skrzynką pocztową, pobiera nowe wiadomości z określonego okresu nocnego, analizuje ich treść, przypisuje je do kategorii i przygotowuje raport przesyłany przez Telegram.

Do stworzenia takiego rozwiązania wystarczy n8n, dostęp do poczty elektronicznej, model językowy i bot Telegrama.

### Jak wygląda workflow w n8n?

[INSERT_IMAGE_N8N_WORKFLOW]

Alt: Schemat automatyzacji n8n do porannej analizy poczty elektronicznej i wysyłania raportu przez Telegram.

Figcaption: Uproszczony schemat działania asystenta poczty w n8n. Opisy na ilustracji są w języku ukraińskim.

Pierwszy węzeł uruchamia automatyzację codziennie o 07:00. Kolejny pobiera nowe wiadomości z Gmaila. Model językowy analizuje ich treść, określa kategorię i ważność. Kod zlicza wyniki, przygotowuje raport, a bot Telegrama przesyła go użytkownikowi.

Węzeł AI Agent na schemacie reprezentuje komponent analizujący wiadomości. W rzeczywistej konfiguracji należy podłączyć do niego model językowy. Jeżeli samodzielny wybór narzędzi nie jest potrzebny, wystarczy zwykły węzeł LLM lub klasyfikator tekstu.

### Co otrzymuje użytkownik?

Po przebudzeniu bierzesz telefon i widzisz informację, że w nocy przyszły 24 nowe wiadomości. Jedenaście z nich dotyczy pracy, osiem zostało sklasyfikowanych jako spam, a pięć należy do subskrypcji i newsletterów.

Oprócz statystyk system wyróżnia ważne wiadomości: potwierdzone spotkanie z klientem, fakturę ze zbliżającym się terminem płatności oraz nowe zapytanie ze strony internetowej.

[INSERT_IMAGE_TELEGRAM_REPORT]

Alt: Przykładowy poranny raport asystenta AI w Telegramie zawierający wyniki analizy 24 wiadomości e-mail.

Figcaption: Demonstracyjny przykład porannego raportu w Telegramie. Treść ilustracji jest w języku ukraińskim.

Zwykła automatyzacja odpowiada za uruchamianie procesu według harmonogramu, pobieranie wiadomości, ich zliczanie oraz wysyłanie raportu. Model językowy analizuje treść wiadomości i określa ich kategorię oraz ważność.

Systemowi wystarczy dostęp do odczytu poczty. Nie trzeba pozwalać mu na usuwanie wiadomości ani odpowiadanie w imieniu użytkownika.

W razie potrzeby funkcjonalność można rozszerzyć. Asystent może przygotowywać wersje robocze odpowiedzi, wyszukiwać faktury, identyfikować terminy wykonania zadań lub proponować dodanie spotkania do kalendarza.

Jeżeli model samodzielnie wybiera odpowiednie narzędzia zależnie od treści wiadomości, taka automatyzacja nabiera cech pełnoprawnego agenta AI.

Jest to stosunkowo prosty system, który nie wymaga skomplikowanej architektury, a może codziennie oszczędzać czas.

## Dlaczego agent AI nie zawsze potrafi odczytać stronę internetową?

Jako programista stron internetowych i specjalista SEO uważam ten temat za szczególnie istotny.

Kiedy człowiek otwiera stronę internetową, widzi zdjęcia, ceny, przyciski, parametry produktów i pozostałe elementy.

Agent może otrzymać zupełnie inne informacje.

Część współczesnych stron pobiera dane za pomocą JavaScript już po otwarciu strony. Jeżeli narzędzie agenta pobiera wyłącznie początkowy kod HTML, potrzebnych informacji może w nim nie być.

Człowiek widzi cenę produktu, a agent otrzymuje pusty kontener.

Do takich zadań można wykorzystać pełnoprawną przeglądarkę, na przykład Chromium sterowaną przez Playwright.

Istnieje również technologia Computer Use, która pozwala modelowi analizować obraz ekranu i generować polecenia klikania przycisków, wpisywania tekstu lub przewijania strony.

Takie operacje wymagają jednak więcej czasu i zasobów obliczeniowych.

Podczas projektowania agenta warto wybrać odpowiednią metodę pobierania informacji. Jeżeli dane można uzyskać przez API lub zwykłe żądanie HTTP, uruchamianie przeglądarki nie jest konieczne.

## Dlaczego agenci AI zapominają o zadaniu?

Jeżeli przez dłuższy czas korzystasz z ChatGPT lub innego modelu językowego w ramach jednej rozmowy, możesz zauważyć, że z czasem zaczyna on ignorować wcześniejsze ustalenia.

Wyjaśniłeś już określone wymaganie, ale model ponownie popełnia ten sam błąd.

Jedna z przyczyn wynika ze sposobu działania okna kontekstowego.

Okno kontekstowe zawiera informacje przekazywane modelowi w celu wykonania aktualnego zadania. Mogą to być instrukcje, wiadomości użytkownika, kod, wyniki wyszukiwania, zawartość plików i odpowiedzi zewnętrznych narzędzi.

Podczas pracy agenta ilość tych informacji stale rośnie.

Agent otworzył jedną stronę, następnie drugą, przeczytał dokumentację, wykonał kilka poleceń, otrzymał błędy i próbował je naprawić. Wszystkie te informacje mogą gromadzić się w kontekście.

Wraz ze wzrostem ilości danych modelowi może być trudniej odnaleźć istotne szczegóły i konsekwentnie przestrzegać początkowych wymagań.

Zjawisko to często określa się jako Context Rot.

Do obsługi dużych zadań programiści wykorzystują różne mechanizmy zarządzania kontekstem.

Jeden z nich nosi nazwę Compaction. System tworzy skrócony opis dotychczasowej pracy, aby zwolnić miejsce na nowe informacje.

Agent może również zapisywać wyniki pośrednie w osobnych plikach, bazach danych lub notatkach roboczych.

Instrukcje dotyczące konkretnych rodzajów zadań można przechowywać osobno i ładować tylko wtedy, gdy są potrzebne. Takie podejście wykorzystuje między innymi mechanizm Skills.

Podczas skracania kontekstu mogą zostać utracone ważne szczegóły. Dlatego najważniejsze reguły działania agenta nie powinny istnieć wyłącznie w postaci instrukcji tekstowych.

## Dlaczego nie powierzam bezpieczeństwa agenta jednemu promptowi?

Załóżmy, że tworzę agenta do obsługi poczty elektronicznej.

Jego zadaniem jest wyszukiwanie niepotrzebnych wiadomości i przygotowywanie listy e-maili, które użytkownik może usunąć.

Mogę zapisać w instrukcji systemowej, że agentowi nie wolno samodzielnie usuwać wiadomości.

Jeżeli jednak jego zadanie polega wyłącznie na analizie poczty, po co w ogóle udostępniać mu narzędzie do usuwania?

Z punktu widzenia programisty znacznie bezpieczniej jest ograniczyć uprawnienia na poziomie oprogramowania.

Jeżeli agent ma wyłącznie dostęp do odczytu, błąd modelu językowego nie spowoduje usunięcia wiadomości za pomocą tego narzędzia.

Jeżeli usuwanie jest potrzebną funkcją, można wdrożyć osobny mechanizm potwierdzania. Agent przygotowuje listę wiadomości, a użytkownik sam zatwierdza operację.

Dotyczy to również plików, operacji finansowych, baz danych, publikowania treści na stronach i innych ważnych zasobów.

Prompt określa pożądane zachowanie modelu. Kod programu wyznacza granice jego możliwości.

## Czym jest Prompt Injection?

Kolejny problem pojawia się, gdy agent pobiera informacje ze źródeł zewnętrznych.

Załóżmy, że analizuje stronę konkurencji. Na stronie może znajdować się tekst, który zamiast informacji o produktach zawiera instrukcje skierowane bezpośrednio do modelu językowego.

Jeżeli system nieprawidłowo przetwarza takie dane, model może potraktować je jako część otrzymanego zadania.

Ten rodzaj ataku nazywa się Prompt Injection.

Szczególnie niebezpieczna jest sytuacja, w której agent ma jednocześnie dostęp do poufnych informacji, odczytuje niezaufane źródła zewnętrzne i może wysyłać dane poza system.

Badacz Simon Willison określa takie połączenie jako Lethal Trifecta.

Ryzyko można ograniczać poprzez odpowiednie uprawnienia, izolowanie narzędzi, kontrolowanie zewnętrznych żądań i zatwierdzanie niebezpiecznych operacji przez człowieka.

Jeżeli tworzę agenta do monitorowania cen konkurencji, nie potrzebuje on dostępu do mojej prywatnej poczty, dokumentów finansowych ani wewnętrznej korespondencji firmy.

Im mniej zbędnych możliwości ma system, tym łatwiej kontrolować jego działanie.

## Do czego służą subagenci?

Złożone zadania można rozdzielać pomiędzy kilku agentów.

Wróćmy do przykładu analizy pięciu konkurentów.

Zamiast analizować wszystkie strony za pomocą jednego modelu, można przydzielić osobne zadania pięciu subagentom.

Każdy pracuje z własnym źródłem informacji i przekazuje wyniki głównemu agentowi, który przygotowuje raport zbiorczy.

Takie podejście pozwala rozdzielić kontekst, wykonywać operacje równolegle i w niektórych przypadkach poprawić jakość wyników.

Stworzenie zespołu agentów nie gwarantuje jednak lepszego wykonania zadania.

Każdy subagent wykorzystuje zasoby modelu językowego. Trzeba również przekazywać zadania, odbierać wyniki, sprawdzać je i łączyć.

Jeżeli proste zadanie można wykonać jednym agentem lub zwykłym skryptem, tworzenie systemu wieloagentowego jedynie skomplikuje projekt i zwiększy koszty.

## Dlaczego działanie agentów AI może być kosztowne?

Podczas zwykłej rozmowy z modelem językowym użytkownik nie zawsze zastanawia się nad ilością przetwarzanych informacji.

Przy tworzeniu agentów jest to istotny element pracy.

Modele językowe przetwarzają informacje w postaci tokenów. W przypadku korzystania z API koszt zazwyczaj zależy od liczby tokenów wejściowych i wyjściowych oraz wybranego modelu.

Załóżmy, że agent otrzymał zadanie sprawdzenia pięciu podstron.

Zamiast przejść bezpośrednio do wskazanych stron, zaczyna analizować strukturę całego serwisu, pobiera dodatkowe dokumenty, przegląda zewnętrzne materiały, powtarza testy i poprawia własne błędy.

Użytkownik zlecił jedno zadanie, ale system wykonał dziesiątki operacji.

Czasami jest to uzasadnione. W innych przypadkach agent zużywa zasoby na działania, które nie są potrzebne do uzyskania wyniku.

Dlatego podczas projektowania należy przewidzieć ograniczenia liczby kroków, wielkości kontekstu, ponownych prób i dostępnych narzędzi.

Nie każda operacja wymaga również najdroższego modelu językowego.

Proste zadania można przekazywać tańszym modelom, a formalne kontrole wykonywać zwykłym kodem.

Koszt działania agenta zależy nie tylko od ceny modelu, lecz także od architektury całego systemu.

## Czy można całkowicie zaufać agentowi AI?

Załóżmy, że opracowany agent poprawnie wykonuje zadanie w 80% przypadków.

Na pierwszy rzut oka jest to całkiem dobry wynik.

Jeżeli jednak agent ma przygotowywać raport co tydzień, to przy założeniu niezależności kolejnych wykonań prawdopodobieństwo otrzymania czterech poprawnych raportów z rzędu wynosi około 41%.

Jest to hipotetyczny przykład matematyczny, a nie statystyka konkretnego agenta.

Jeżeli system potrafi wykrywać błędy i ponawiać wykonanie zadania, wynik może się poprawić.

Ponowne uruchomienie nie zawsze rozwiązuje jednak problem. Jeżeli agent korzysta z niewłaściwego źródła lub jego narzędzie działa nieprawidłowo, może powtarzać ten sam błąd.

Ważne jest więc nie tylko uzyskanie wyniku, lecz także możliwość sprawdzenia jego poprawności.

Wykorzystuje się do tego automatyczne testy, kontrole wykonywane przez kod, dodatkowe modele i nadzór człowieka.

W tworzeniu systemów AI takie metody oceny często określa się jako Evals.

Jeżeli agent ma zebrać ceny pięciu konkurentów, zwykły kod może sprawdzić liczbę rekordów, obecność wymaganych pól i poprawność formatu danych.

Sprawdzenie, czy znaleziona cena rzeczywiście dotyczy konkretnego produktu, może jednak wymagać dodatkowych mechanizmów kontroli.

Poziom weryfikacji powinien odpowiadać konsekwencjom potencjalnego błędu.

Błąd w szkicu artykułu i błąd podczas operacji finansowej mają zupełnie inną cenę.

## Praktyczny przykład z mojej pracy: Raccoon SEO Scanner

Jednym z obszarów, którymi się zajmuję, jest automatyzacja technicznych audytów SEO.

Do realizacji takiego zadania można wykorzystać n8n, zwykły kod i model językowy.

W ramach rozwoju Raccoon SEO Scanner pracuję nad systemem, który otrzymuje adres strony internetowej i sprawdza:

- Status HTTP.
- Title i Meta Description.
- Nagłówki H1.
- Canonical.
- Dyrektywy Robots.
- Hreflang.
- Open Graph.
- Obrazy i ich opisy alternatywne.
- Linki wewnętrzne i zewnętrzne.

Do większości tych kontroli sztuczna inteligencja nie jest potrzebna.

Zwykły kod może ustalić, czy strona zawiera nagłówek H1, jaki adres znajduje się w Canonical i jaki status HTTP zwraca serwer.

Przekazywanie całego kodu HTML modelowi językowemu i zlecanie mu wykonania każdej kontroli byłoby niepotrzebnym zużywaniem zasobów.

Po zebraniu wyników można jednak wykorzystać model językowy do innego zadania.

Może on wyjaśnić właścicielowi strony, co oznaczają wykryte problemy, dlaczego są istotne, które należy usunąć w pierwszej kolejności i jakie działania podjąć.

Kod zbiera faktyczne dane, a sztuczna inteligencja pomaga je interpretować.

Moim zdaniem właśnie takie połączenia mają duży potencjał praktyczny dla przedsiębiorstw.

## Od czego zacząć automatyzację własnej firmy?

Nie polecałbym rozpoczynania od tworzenia uniwersalnego agenta AI, który ma potrafić wszystko.

Najpierw warto określić konkretny proces, który regularnie zabiera czas Tobie lub Twoim pracownikom.

Może to być obsługa zgłoszeń, przygotowywanie raportów, analiza dokumentów, monitorowanie konkurencji, klasyfikacja zapytań lub praca z bazą klientów.

Następnie trzeba ustalić, które operacje można zautomatyzować zwykłym kodem, a gdzie rzeczywiście potrzebny jest model językowy.

Do wielu zadań wystarczy n8n lub Make. Inne będą wymagały podłączenia modelu językowego przez API. Bardziej złożone procesy mogą potrzebować pełnoprawnego systemu agentowego.

Wybór technologii powinien zależeć od zadania, a nie od popularności konkretnego narzędzia.

## Moje wnioski

Traktuję agentów AI jako kolejne narzędzie programisty. Bardzo przydatne i perspektywiczne, ale mające własne ograniczenia.

Podoba mi się możliwość tworzenia systemów, które potrafią pracować z informacjami, analizować je i wykonywać operacje wymagające wcześniej wielu godzin ręcznej pracy.

Nie widzę jednak sensu włączania sztucznej inteligencji do każdego procesu tylko dlatego, że jest obecnie popularna.

Jeżeli zadanie można rozwiązać dziesięcioma liniami JavaScriptu, użyję dziesięciu linii JavaScriptu. Jeżeli trzeba przeanalizować dużą ilość nieustrukturyzowanych informacji, podłączę model językowy. Jeżeli system powinien samodzielnie wybierać narzędzia i planować działania, rozważę architekturę agentową.

Dla właściciela firmy nie ma większego znaczenia, ile modeli językowych, subagentów i narzędzi pracuje wewnątrz systemu.

Ważne jest, aby system prawidłowo wykonywał swoją pracę, oszczędzał czas, nie tworzył dodatkowych problemów i kosztował mniej niż proces, który zastępuje.

Moim zdaniem od tego należy zaczynać tworzenie każdej automatyzacji.
