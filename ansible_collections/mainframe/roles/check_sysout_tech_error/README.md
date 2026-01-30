oaps_prim_check_sysout_tech_error
=================================

Ce rôle demande une sysout, vérifie si un message d'erreur technique y est contenu et sort en erreur si une erreur a été trouvée.

## Prérequis
Les patterns des messages d'erreurs sont stockés dans le rôle oaps_ref_common_files, dans le dossier files et répondent à une convention de nommage variabilisée <file_name>_<code_SI>.txt, <file_name> étant renseigné dans la variable `zowe_tech_error_file_base_name` et <code_SI> étant renseigné par `code_SI`.

Le rôle fait appel au rôle oaps_get_sysout qui effectue les opérations de récupération de sysout, et à ce titre, les variables nécessaires pour l'exécution de ce rôle doivent être fournies.

Les dépendances à ces rôles sont définies dans le fichier meta/requirements.yml et doivent être adaptées au repository où ils sont installés.

Les variables d'accès au script Zowe doivent être définies :
* zowe_get_sysout_cmd_var: ./Zowe-Sysout.sh   
* zowe_chdir_var: /app/list/care_oaps/zowe/scripts/DEV/V1.00.0

La variable de pattern de nom de fichier d'erreur technique doit être définie et pointer sur l'emplacement du rôle qui les contient :
* zowe_tech_error_file_base_name : ../oaps_ref_common_files/files/sysout_tech_errors_


## Variables en entrée
Les paramètres devant être fournis en entrée sont les suivants :
* code_SI : Code SI permettant de préciser le fichier des erreurs techniques.
* get_sysout_caisse : Client issue de l’alerte sur 4 caractères (EX : TET8)
* get_sysout_adid : Nom du job issu de l’alerte (EX : TEZERROR)
* get_sysout_jobidcare : jobid issu de l’alerte (EX : JOB11402)


## Retour du rôle
Le rôle retourne op_exec_rc = 0 si la lecture a pu être faite, la sysout est accessible via la variable sysout_result.stdout.  

Dans le cas contraire, il retourne : op_exec_rc et op_short_msg contenant le message d'erreur.  
  

| op_exec_rc | Description |
| ---------- | ----------- |
| 0 | OK, sysout lue et ne contient pas de message d'erreur technique |
| 400 | Erreur préalable à l'exécution du script |
| 401 | Erreur d'exécution du script |
| 402 | Sysout lue, mais contient au moins un message d'erreur. |
 
**Variables alimentées :**
* sysout_result.stdout : contient le résultat de la sysout
* sysout_tech_error_found : true si une erreur technique a été trouvée, false sinon
* sysout_tech_error_line : contient la ligne contenant l'erreur le cas échéant.

## Tests
Les tests utilisent un container docker de simulation (simulation_ZOWE).  
Les fichiers molecule.yml utilisent le driver delegated, i.e. le container docker doit être accessible via ssh.
