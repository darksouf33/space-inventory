# CAGIP-CARE-mainframe-restart-02

## Synopsis

Ce playbook a pour objectif de relancer un JOB mainframe en ABEND puis de le mettre à COMPLETE en cas d'échec.
Un exemple de ce type de consigne est la consigne https://prd-carine.prodinfo.gca/instruction/379584.



## Procédure

Alerte EX : "EQQ7INIT-A2O1_JOB_YE9DJC_JOBID_JOB06354_010_2307261900_U3E7 - 26 Jul 2023 - 18:04:47 (EQQ7INIT-A2O1-YE9DJC-010-2307261900)"
L'automate extrait les informations suivantes de la description de l'alerte dans CARE comme ce-ci:
- Contrôleur TWS -> A2O1
- JOB -> YE9DJC
- JOBID-> JOB06354
- OPNO -> 010
- IAT -> 2307261900
- Caisse -> HOSTNAME


Il commence par vérifier si le JOB en ABEND n'est pas en erreur technique.

Si pas d'erreur technique il passe une commande à l'API ZOWE de relance du JOB.
Si la relance n'est pas effective il passe une commande à l'API ZOWE pour une mise à COMPLETE du job.

Escalade le ticket vers le groupe support après une relance sans erreur ou la mise à COMPLETE.

## Prérequis

Le groupe d'escalade, le maximum de relance du restart, le code SI et l'action après un restart en échec doivent être ajouté en paramètre de la consigne :

```json
"param_consigne": {
    "code_si":"BPCR",
    "escgrp1": "CAGIP-OPN-UNX-LINUX_BUILD",
    "max_step": "2",
    "CMD_Si_Ko": "COMPLETE"
    "close": "oui"
    "wait": "10"
}
```
## Valeur possible:
| Paramètre | Valeur              |
|----------|---------------------|
|max_step| 0 : pas de restart  |
|max_step| 1 : un seul restart |
|max_step| 2 : deux restart    |
|max_step| n : n restart       |

| Paramètre | Valeur                                                               |
|----------|----------------------------------------------------------------------|
|CMD_Si_Ko| COMPLETE : pour une mise à COMPLETE du JOB après un restart en echec |
|CMD_Si_Ko| Laisser-en-etat : pour ne rien faire sur le JOB                      |

| Paramètre | Valeur                                                                         |
|----------|--------------------------------------------------------------------------------|
|code_si| BPCR : permet d'identifier quel fichier des erreurs technique qui sera utilisé |

| Paramètre | Valeur                                                                   |
|----------|--------------------------------------------------------------------------|
|close| oui/non : permet de faire une clôture du ticket si le restart est réussi |

| Paramètre | Valeur                                                                      |
|-----------|-----------------------------------------------------------------------------|
| wait      | int en minute : permet de faire une temporisation sur la demande de restart |

## Playbook d'entrée

event_main.yml

## Variables

| Variable | Type  | Défaut | Description                                                            |
|----------|-------| ------ |------------------------------------------------------------------------|
| escgrp1  | String |        | Contient le groupe d'escalade de l'incident                            |
| code_si  | String |        | Contient le nom du SI afin de connaître la liste des erreurs technique |
| max_step  | INT   |        | Contient le nombre maximun de tentative de relance du JOB              |


## Résultats d'éxecution

| Condition                                       | Résultats en sortie                                                                                                                                                                                                                                                                                                 |
|:------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Si la relance est effective                     | escalade: true<br/>short_msg: Carebot - COMPLETE après restart du JOB : ' + tws_manage_adid + ' et escalade vers: ' + groupe_escalade<br/>long_msg: Carebot - COMPLETE après restart du JOB : ' + tws_manage_adid + ' et escalade vers: ' + groupe_escalade<br/>return_code: 2 (Diagnosis)<br/>retour_pilote: false |
| Si la relance est sur une itération du max_step | escalade: false<br/>short_msg: 'Carebot - Restart du JOB : ' + tws_manage_adid<br/>long_msg: 'Carebot - Restart du JOB : ' + tws_manage_adid<br/>return_code: 2 (Diagnosis)<br/>retour_pilote: false                                                                                                                |
| Si le maximun de relance                        | escalade: false<br/>short_msg: 'Carebot - Max restart du JOB : ' + tws_manage_adidd<br/>long_msg: 'Carebot - Nombre maximum de reprises atteintes pour le JOB : ' + tws_manage_adid<br/>return_code: 2 (Diagnosis)<br/>retour_pilote: true                                                                                                                 |
| Si on trouve une erreur technique               | escalade: false<br/>short_msg: 'Carebot - Erreur technique voir ticket METIS'<br/>long_msg: 'Carebot - Erreur technique : ' + My_sysout_tech_error_line<br/>return_code: 2 (Diagnosis)<br/>retour_pilote: true                                                                                                      |
| Si une erreur lors de l'éxécution du playbook   | escalade: false<br/>short_msg: 'Carebot - Erreur sur le robot, reprise manuelle de la consigne<br/>long_msg: 'Carebot - Erreur sur le robot, reprise manuelle de la consigne<br/>return_code: 2 (Diagnosis)<br/>retour_pilote: true                                                                                 |
| Si une erreur lors de l'éxécution de ZOWE       | escalade: false<br/>short_msg: 'Carebot - Erreur sur l'API Zowe, reprise manuelle de la consigne<br/>long_msg: 'Carebot - Erreur sur l'API Zowe, reprise manuelle de la consigne<br/>return_code: 2 (Diagnosis)<br/>retour_pilote: true                                                                             |