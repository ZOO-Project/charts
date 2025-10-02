# KEDA PostgreSQL Queries

Ce répertoire contient les requêtes SQL utilisées par KEDA pour l'autoscaling basé sur PostgreSQL.

## Fichiers disponibles

### postgresql-scaler-query.sql
Requête complexe recommandée pour la production avec :
- Protection absolue des pods ayant des workers actifs
- Logique hybride basée sur les workers ET les services
- Support du scale-to-zero
- Calculs sophistiqués pour optimiser les ressources

### postgresql-scaler-query-simple.sql
Requête simplifiée pour les tests et développement :
- Simple comptage des workers actifs
- Plus facile à comprendre et déboguer

## Configuration

Pour utiliser une ConfigMap (recommandé pour réduire la taille des secrets Helm) :

```yaml
keda:
  triggers:
    postgresql:
      useConfigMap: true
```

Pour utiliser une requête inline (pour des requêtes simples) :

```yaml
keda:
  triggers:
    postgresql:
      useConfigMap: false
      query: "SELECT COUNT(*) FROM workers WHERE status = 1"
```

## Avantages de l'approche ConfigMap

1. **Taille des secrets** : Réduit significativement la taille des secrets Helm
2. **Lisibilité** : Code SQL dans des fichiers dédiés avec coloration syntaxique
3. **Maintenance** : Plus facile à modifier et versionner
4. **Réutilisabilité** : Peut être partagé entre différents déploiements

## Personnalisation

Pour créer votre propre requête :

1. Créez un nouveau fichier `.sql` dans ce répertoire
2. Modifiez la ConfigMap pour pointer vers votre fichier
3. La requête doit retourner un entier représentant le nombre de réplicas souhaité