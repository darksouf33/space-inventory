oaps_prim_get_sysout
====================

Ce rôle demande une sysout via Zowe


## Prérequis
Les variables d'accès au script Zowe doivent être définies :

* zowe_get_sysout_cmd_var: ./Zowe-Sysout.sh   
* zowe_chdir_var: /app/list/care_oaps/zowe/scripts/DEV/V1.00.0

## Variables en entrée
Les paramètres devant être fournis en entrée sont les suivants :
* get_sysout_caisse : Client issue de l’alerte sur 4 caractères (EX : TET8)
* get_sysout_adid : Nom du job issu de l’alerte (EX : TEZERROR)
* get_sysout_jobidcare : jobid issu de l’alerte (EX : JOB11402)

## Retour du rôle
Le rôle retourne op_exec_rc = 0 si la lecture a pu être faite, la sysout est accessible via la variable sysout_result.stdout.  

Dans le cas contraire, il retourne : op_exec_rc et op_short_msg contenant le message d'erreur.  
  
| op_exec_rc | Description |
| ---------- | ----------- |
| 0 | OK, sysout lue |
| 400 | Erreur préalable à l'exécution du script |
| 401 | Erreur d'exécution du script, y compris erreurs retournées par le script |


**Variables alimentées :**
* sysout_result.stdout : contient le résultat de la sysout


## Tests
Les tests utilisent un container docker de simulation (simulation_ZOWE).  
Le dossier molecule contient un ensemble de tests.
Les fichiers molecule.yml utilisent le driver delegated, i.e. le container docker doit être accessible via ssh.



