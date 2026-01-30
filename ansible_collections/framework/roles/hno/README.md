# OAPS_frm_hno
Rôle de gestion des jours fériés et heures non ouvrées. <br/><br/>
**Partie HO/HNO:** <br/><br/>
Ci-dessous les variables hno à partir desquelles le rôle effectue son calcul (hno: true/false): <br/> 
**CA-GIP-HNO1**:19H-8H
 	 
**CA-GIP-HNO2**:18H-8H
 	 
**CA-GIP-HNO3**:19h-7H
 	 
**CA-GIP-HNO4**:18H-9H
 	 
**CA-GIP-HNO5**:17H-9H
 	 
**CA-GIP-HNO6**:17H-8H
 	 
**CA-GIP-HNO7**:19H-6H
<br/><br/>
Intervalle à positionner dans la zone **Parametres** de la partie **Carebot** de la consigne : <br/>
{"escgrp1":"keyhno1":"CA-GIP-HNO1"}. <br/><br/>
Extraction de la valeur à réaliser dans le **event_date_tasks.yml** du projet (extraction globale de param_consigne au préalable): <br/>
`-` name: Extract event data (type de hno) <br/>
` ` set_fact: <br/>
` ` ` `   keyhno1: "{{ param_consigne['keyhno1'] | default('')}}" <br/><br/>

Appel du rôle avec passage de la valeur dans le **main.yml** du projet: <br/>
`-` name: Evaluate HNO (retour avec variable < hno > de type booléen) <br/>
` `  include_role:<br/>
` ` ` `name: OAPS_frm_hno<br/>
` `  vars:<br/>
` ` ` `key: "{{ keyhno1 }}"




