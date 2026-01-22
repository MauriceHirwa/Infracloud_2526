N2 – Netmiko Config Commands Experiment
Doel van het experiment

In dit experiment heb ik Netmiko gebruikt om configuratiecommando’s automatisch uit te voeren op een netwerkdevice via SSH.
In tegenstelling tot N1 (enkel show commands), focust N2 op het pushen van configuraties.

Omgeving

Besturingssysteem: Linux VM

Programmeertaal: Python 3

Library: Netmiko

Netwerkdevice: Cisco IOS (via SSH bereikbaar vanuit de VM)

Uitgevoerde stappen

Voorbereiding van de VM

Gecontroleerd of Python 3 beschikbaar is

Netmiko geïnstalleerd met pip

Connectiviteit naar het netwerkdevice getest via SSH

Opzetten van de Netmiko-verbinding

In het Python-script werd een device dictionary aangemaakt met:

device type (cisco_ios)

IP-adres van het toestel

gebruikersnaam en wachtwoord

enable secret

Verbinding gemaakt met ConnectHandler

Overgeschakeld naar enable mode

Automatisch configuratie pushen (N2)

Met send_config_set() werden meerdere configuratiecommando’s uitgevoerd:

aanpassen van de hostname

aanmaken van een loopback interface

instellen van een IP-adres

toevoegen van een description

Deze commando’s werden automatisch in configuration mode uitgevoerd

Configuratie opslaan

De configuratie werd permanent opgeslagen met save_config()

Hierdoor blijft de configuratie behouden na een reboot

Verificatie van de configuratie

Met send_command() werden show commands uitgevoerd om te controleren of:

de hostname correct gewijzigd is

de loopback interface bestaat

het IP-adres correct ingesteld is

Verbinding afsluiten

Na de configuratie en verificatie werd de SSH-verbinding netjes afgesloten

Resultaat

De configuratie werd succesvol automatisch toegepast op het netwerkdevice.
De wijzigingen waren zichtbaar via show commands en bleven behouden na het opslaan van de configuratie.

Waarom is dit nuttig?

Geen manuele CLI-commando’s meer nodig

Sneller en minder foutgevoelig

Herhaalbaar en schaalbaar voor meerdere devices

Ideaal voor netwerkautomatisatie