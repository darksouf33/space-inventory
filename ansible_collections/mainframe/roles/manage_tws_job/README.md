oaps_prim_manage_tws_job
=================================

Ce rôle permet d'agir sur les jobs TWS grâce aux actions suivantes :
* RESTART : relance de job
* COMPLETE : mise à l'état COMPLETE

## Prérequis

Les variables d'accès au script Zowe doivent être définies :
* zowe_cmd_TWS_manage_var: ./Zowe-TWS.sh   
* zowe_chdir_var: /app/list/care_oaps/zowe/scripts/DEV/V1.00.0

## Variables en entrée
Les paramètres devant être fournis en entrée sont les suivants :
* tws_manage_caisse: Client issue de l’alerte sur 4 caractères (EX : TET8)
* tws_manage_adid: Le nom de l’application (en général sur 6 positions mais il y a des exceptions). (EX : ZERROR)
* tws_manage_opc: Nom du contrôleur TWS sur 4 positions. (EX : S806)
* tws_manage_iat: L’IATime sur 10 positions. (EX : 2207131100)
* tws_manage_status: RESTART / COMPLETE
* tws_manage_opno: Numéro d’opération sur 3 positions. (EX : 010)


## Retour du rôle
Le rôle retourne op_exec_rc = 0 si l'opération a pu être réalisée sans erreur.

Dans le cas contraire, il retourne : op_exec_rc et op_short_msg contenant le message d'erreur.  
  

| op_exec_rc | Description |
| ---------- | ----------- |
| 0 | OK, sysout lue et ne contient pas de message d'erreur technique |
| 400 | Erreur préalable à l'exécution du script |
| 401 | Erreur d'exécution du script |
 


## Tests
Les tests utilisent un container docker de simulation (simulation_ZOWE).  
Les fichiers molecule.yml utilisent le driver delegated, i.e. le container docker doit être accessible via ssh.
