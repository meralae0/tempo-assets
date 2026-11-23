=== Q1 ===
Utilisez la fonction SOMME.SI :

```
=SOMME.SI(A:A;"Courses";B:B)
```

- Premier argument : la plage où chercher le critère (colonne A).
- Deuxième argument : le critère ("Courses").
- Troisième argument : la plage à additionner (colonne B).

Quelques remarques :
- Dans une version anglaise d'Excel, la fonction s'appelle SUMIF et le séparateur est souvent la virgule : `=SUMIF(A:A,"Courses",B:B)`.
- La comparaison ne tient pas compte des majuscules, mais un espace en trop (« Courses ») fera échouer la correspondance. Si besoin, nettoyez avec SUPPRESPACE.
- Pour plusieurs critères (par exemple « Courses » et un mois précis), utilisez SOMME.SI.ENS : `=SOMME.SI.ENS(B:B;A:A;"Courses";C:C;"Janvier")`.
- Vous pouvez aussi mettre le critère dans une cellule (par exemple D1) : `=SOMME.SI(A:A;D1;B:B)`.

=== Q2 ===
Une décharge rapide après une mise à jour est fréquente et souvent temporaire. Voici quoi vérifier, dans l'ordre :

1. **Attendez 2 à 3 jours.** Après une mise à jour, le système réindexe les fichiers, optimise les applications et resynchronise les données. Cela consomme beaucoup pendant un ou deux jours, puis ça se calme.
2. **Regardez quelle application consomme.** Paramètres > Batterie > Utilisation de la batterie. Si une appli ressort anormalement (surtout en arrière-plan), mettez-la à jour, forcez son arrêt, videz son cache ou restreignez son activité en arrière-plan.
3. **Mettez à jour toutes les applications** depuis le Play Store : certaines ne sont pas encore adaptées à la nouvelle version d'Android.
4. **Redémarrez le téléphone.** Ça règle souvent un processus bloqué qui tourne en boucle.
5. **Vérifiez les réglages qui ont pu changer :** luminosité automatique, durée avant mise en veille, écran toujours allumé (Always On Display), taux de rafraîchissement élevé (120 Hz), localisation en haute précision, Bluetooth/Wi-Fi/NFC actifs en permanence.
6. **Vérifiez le réseau.** Une mauvaise couverture ou la 5G en zone faible vide vite la batterie. Essayez de passer en 4G pour comparer.
7. **Videz la partition cache** (sur certains modèles, via le mode recovery) si le problème persiste après quelques jours.
8. **Regardez l'état de la batterie** si votre téléphone le propose (Paramètres > Batterie > État de la batterie, ou Entretien de l'appareil sur Samsung). Une batterie usée supporte moins bien les changements.
9. **En dernier recours :** sauvegardez vos données et faites une réinitialisation d'usine. Cela règle la majorité des problèmes logiciels liés à une mise à jour.

Si rien n'y fait, consultez les forums de votre modèle : il arrive qu'une mise à jour ait un bug connu, corrigé par un correctif quelques semaines plus tard.

=== Q3 ===
**Taux fixe :** le taux d'intérêt est fixé à la signature et ne change jamais pendant toute la durée du prêt. Vos mensualités restent identiques du premier au dernier mois.
- Avantages : sécurité, visibilité totale sur le coût du crédit, budget facile à prévoir.
- Inconvénients : le taux de départ est généralement un peu plus élevé qu'un taux variable, et vous ne profitez pas d'une éventuelle baisse des taux (sauf à renégocier ou faire racheter le prêt, ce qui a un coût).

**Taux variable (ou révisable) :** le taux évolue dans le temps selon un indice de référence (par exemple l'Euribor en zone euro), plus une marge fixée par la banque. Il est révisé à intervalles réguliers (souvent une fois par an).
- Avantages : taux de départ souvent plus bas, et vous profitez des baisses de taux.
- Inconvénients : si les taux montent, vos mensualités (ou la durée du prêt) augmentent. Le coût total est incertain.

**Le compromis : le taux variable capé.** La variation est limitée par un plafond (par exemple +1 ou +2 points maximum). Vous gardez une partie de l'avantage en cas de baisse, avec un risque limité en cas de hausse.

**En résumé :**
- Taux fixe si vous voulez de la sécurité, avez un budget serré ou empruntez sur une longue durée.
- Taux variable (de préférence capé) si vous acceptez un peu de risque, pensez que les taux vont baisser, ou comptez rembourser ou revendre rapidement.

Comparez toujours le TAEG (taux annuel effectif global), qui inclut l'assurance et les frais, et pas seulement le taux nominal.

=== Q4 ===
La commande est :

```
rm -rf photos_2019
```

- `-r` : supprime le dossier et tout son contenu (récursif).
- `-f` : force la suppression sans demander de confirmation.

**Attention :** il n'y a pas de corbeille. Une fois supprimé, le dossier ne peut pas être récupéré facilement. Avant de lancer la commande :

1. Vérifiez que vous êtes au bon endroit avec `pwd`, et que le dossier contient bien ce que vous pensez avec `ls photos_2019`.
2. Si vous n'êtes pas dans le dossier parent, donnez le chemin complet : `rm -rf ~/Images/photos_2019`.
3. Si vous préférez une confirmation, utilisez `rm -ri photos_2019` (il vous demandera pour chaque fichier) ou `rm -rI photos_2019` (une seule confirmation globale).
4. Ne mettez jamais d'espace ou de joker par erreur (`rm -rf photos_2019 /*` ou `rm -rf /`), c'est la source des pires accidents.

Si le dossier appartient à root ou à un autre utilisateur, il faudra ajouter `sudo` devant, mais faites-le seulement si vous êtes sûr du chemin.

Note : « définitivement » veut dire que les fichiers ne passent pas par la corbeille. Pour un effacement réellement irrécupérable (même avec des outils de récupération), il faudrait utiliser `shred` sur les fichiers, et ce n'est pas totalement fiable sur un SSD.

=== Q5 ===
Une erreur 404 après un déplacement signifie que l'ancienne adresse n'existe plus, alors que des liens (internes, externes ou Google) pointent encore dessus. La bonne solution est une **redirection 301** (permanente) de l'ancienne URL vers la nouvelle.

**1. Mettre en place la redirection 301, selon votre site :**

- **Apache (fichier .htaccess à la racine) :**
  ```
  Redirect 301 /ancienne-page.html /nouvelle-page.html
  ```
- **Nginx (dans le bloc server) :**
  ```
  location = /ancienne-page.html {
      return 301 /nouvelle-page.html;
  }
  ```
  Puis rechargez Nginx (`sudo nginx -t && sudo systemctl reload nginx`).
- **WordPress :** installez une extension de redirection (par exemple « Redirection ») et ajoutez l'ancienne et la nouvelle URL. Si vous avez seulement changé le permalien, allez aussi dans Réglages > Permaliens et cliquez sur Enregistrer pour régénérer les règles.
- **Autres CMS ou constructeurs de sites (Shopify, Wix, etc.) :** cherchez un menu « Redirections d'URL » dans les réglages ou le référencement (SEO).

**2. Corriger les liens internes.** Mettez à jour le menu, les autres pages et les articles qui pointent vers l'ancienne adresse, pour qu'ils visent directement la nouvelle.

**3. Vérifier.** Ouvrez l'ancienne URL dans une fenêtre de navigation privée : vous devez arriver sur la nouvelle page. Vous pouvez aussi vérifier le code avec `curl -I https://votresite.com/ancienne-page.html` (il doit indiquer 301).

**4. Prévenir Google.** Dans Google Search Console, mettez à jour votre sitemap et demandez l'indexation de la nouvelle URL. Les 404 disparaîtront progressivement du rapport.

Si la nouvelle page elle-même renvoie une 404, le problème est différent : vérifiez que le fichier est bien au bon endroit sur le serveur, que le nom (y compris majuscules et extension) correspond exactement, et videz le cache du site ou du CDN.

=== Q6 ===
**Pâtes tomates, ail et parmesan (pour 2, environ 15 minutes)**

**Ingrédients :**
- 200 g de pâtes (spaghetti, penne ou ce que vous avez)
- 3 ou 4 tomates bien mûres (ou 250 g de tomates cerises, ou une petite boîte de tomates concassées)
- 2 ou 3 gousses d'ail
- 3 cuillères à soupe d'huile d'olive
- 40 à 50 g de parmesan râpé
- Sel, poivre
- Facultatif : une pincée de piment, quelques feuilles de basilic

**Préparation :**
1. Faites bouillir une grande casserole d'eau salée et lancez la cuisson des pâtes selon le temps indiqué sur le paquet.
2. Pendant ce temps, coupez les tomates en petits dés et émincez finement l'ail.
3. Dans une poêle, faites chauffer l'huile d'olive à feu moyen. Ajoutez l'ail et faites-le revenir 1 minute, sans le laisser brunir (sinon il devient amer). Ajoutez le piment si vous en voulez.
4. Ajoutez les tomates, salez et poivrez. Laissez cuire 6 à 8 minutes en remuant, jusqu'à ce qu'elles fondent en sauce.
5. Avant d'égoutter les pâtes, gardez une petite tasse de leur eau de cuisson.
6. Versez les pâtes égouttées dans la poêle, mélangez bien avec la sauce et ajoutez un peu d'eau de cuisson pour lier si c'est trop sec.
7. Hors du feu, ajoutez la moitié du parmesan et mélangez.
8. Servez aussitôt avec le reste du parmesan, un filet d'huile d'olive et quelques feuilles de basilic.

Bon appétit !
