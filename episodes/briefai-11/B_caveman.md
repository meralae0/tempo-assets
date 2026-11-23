=== Q1 ===
`=SOMME.SI(A:A;"Courses";B:B)`

Version anglaise d'Excel : `=SUMIF(A:A,"Courses",B:B)`. Le texte doit correspondre exactement à la cellule. Les majuscules ne comptent pas, mais les espaces en trop font échouer la formule.

=== Q2 ===
À vérifier, dans cet ordre :

1. Paramètres > Batterie > Utilisation : repère l'appli qui consomme le plus.
2. Juste après une mise à jour, le système réindexe et optimise pendant 1 à 3 jours. Attends avant de conclure.
3. Applis : mets-les toutes à jour via le Play Store. Une appli pas encore compatible peut tourner en boucle.
4. Redémarre le téléphone.
5. Écran : luminosité auto, mise en veille courte, taux 60 Hz au lieu de 120 Hz si l'option existe.
6. Désactive GPS, Bluetooth et Wi-Fi quand ils ne servent pas.
7. Toujours pareil ? Vide le cache système (mode recovery) ou fais une sauvegarde puis une réinitialisation.

La batterie chauffe ou gonfle ? Arrête de l'utiliser et fais-la contrôler.

=== Q3 ===
Taux fixe : taux bloqué toute la durée du prêt. Mensualité identique du début à la fin. Budget prévisible, aucun risque si les taux montent.

Taux variable : taux revu périodiquement (souvent chaque année) selon un indice de référence, par exemple l'Euribor. Mensualité ou durée change. Départ souvent moins cher, mais coût final incertain.

Variante : taux variable capé. La hausse est plafonnée, par exemple à +1 ou +2 points.

Choix : fixe si tu veux la sécurité ou si les taux sont bas. Variable si tu supportes le risque, si les taux doivent baisser, ou si tu comptes revendre ou rembourser tôt.

=== Q4 ===
Attention : cette commande est irréversible. Elle ne passe pas par la corbeille, et le dossier ainsi que tout son contenu seront perdus sans possibilité de récupération simple. Vérifie d'abord que tu es dans le bon répertoire et que tu n'as plus besoin de ces fichiers.

Vérifie le contenu avant :

```
ls -la photos_2019
```

Puis supprime :

```
rm -rf photos_2019
```

`-r` supprime le contenu de façon récursive. `-f` supprime sans demander de confirmation. Pour avoir une confirmation à chaque fichier, remplace `-rf` par `-ri`. Si le dossier appartient à un autre utilisateur, ajoute `sudo` devant, mais seulement après avoir revérifié le chemin.

=== Q5 ===
Ancienne URL ne pointe plus vers rien. Solution : redirection 301 de l'ancienne adresse vers la nouvelle.

Apache, dans `.htaccess` :

```
Redirect 301 /ancienne-page.html /nouvelle-page.html
```

Nginx, dans le bloc `server` :

```
location = /ancienne-page.html {
    return 301 /nouvelle-page.html;
}
```

Puis recharge Nginx : `sudo nginx -s reload`.

WordPress : extension de redirection, ou Réglages > Permaliens > Enregistrer pour régénérer les règles.

Ensuite :
1. Corrige les liens internes du site vers la nouvelle URL.
2. Vide le cache du site, du CDN et du navigateur.
3. Mets à jour le sitemap et soumets-le dans Google Search Console.

=== Q6 ===
Pâtes tomate, ail, parmesan. 2 personnes, 15 min.

Ingrédients :
- 200 g de pâtes (spaghetti ou penne)
- 3 tomates mûres, ou 250 g de tomates cerises
- 2 gousses d'ail
- 3 c. à soupe d'huile d'olive
- 40 g de parmesan râpé
- Sel, poivre, basilic ou piment (facultatif)

Étapes :
1. Fais cuire les pâtes dans l'eau bouillante salée, selon le temps du paquet.
2. Pendant ce temps, émince l'ail. Coupe les tomates en dés.
3. Chauffe l'huile à feu moyen. Fais revenir l'ail 1 min, sans le laisser brunir.
4. Ajoute les tomates, sale, poivre. Laisse cuire 5 à 7 min.
5. Garde une demi-tasse d'eau de cuisson. Égoutte les pâtes.
6. Mélange les pâtes à la sauce avec un peu d'eau de cuisson pour lier.
7. Hors du feu, ajoute le parmesan. Sers tout de suite.
