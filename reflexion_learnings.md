## Learnings

### 1. Robustheit durch Fehlerbehandlung

Eine der wichtigsten Erkenntnisse war die Bedeutung einer robusten Fehlerbehandlung. Fehler wie JSONDecodeError können dazu führen, dass die gesamte Anwendung abstürzt, wenn sie nicht korrekt behandelt werden. Eine präventive Fehlerbehandlung stellt sicher, dass die Anwendung auch bei unerwarteten Eingaben oder Dateizuständen stabil bleibt.

### 2. Sicherheit durch Passwort-Hashing

Die Implementierung von Passwort-Hashing ist ein wichtiger Schritt, um die Sicherheit der Benutzerdaten zu gewährleisten. Klartextpasswörter sollten niemals gespeichert werden, und das Hashing stellt sicher, dass selbst bei einem Datenleck die Passwörter geschützt sind.

### 3. Effiziente Bildverwaltung

Die Konvertierung von Bildern war ein effektiver Weg, um Bilder in einer JSON-Datei zu speichern. Dies ermöglichte eine einfache Speicherung und Abruf von Bilddaten zusammen mit den Charakterinformationen. Am Schluss haben wir jedoch gefunden es ist noch einfacher direkt einen Link input zu geben. 

### 4. Benutzerfreundliches Daten Management

Die Daten der User konnten mittels den richtigen Token-> my data repo richtig gespeichert und als Tabelle Angezeigt werden. Dabei haben nur die rechtmässigen Creators zugriff auf ihre Charaktere.  

### 5. Verwendung von Tokens

Die Verwendung von richtigen Tokens öffnet viele sichere Anwendungsgebiete für weitere Zukünftige Programme die wir erstellen werden/können. 



