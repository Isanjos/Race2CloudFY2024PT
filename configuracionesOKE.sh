#!/bin/bash
KUBECTL=$(which kubectl)
GREP=$(which grep)
AWK=$(which awk)
OPENSSL=$(which openssl)

URL_INGRESS='deploy-ingress.yaml'
NS_ARGO='argocd'
URL_ARGO='https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml'



$KUBECTL create clusterrolebinding oke_clst_adm --clusterrole=cluster-admin --user=${OCI_CS_USER_OCID}
if [ $? -eq 0 ]; then 
	echo 'ClusterRole admin Creado'; 
else 
	echo 'Error al crear Cluster Role'; 
fi

$KUBECTL apply -f $URL_INGRESS
if [ $? -eq 0 ]; then 
	echo 'Service Ingress creado correctamente'; 
else 
	echo 'Error al crear ingress'; 
fi

$OPENSSL req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=nginxsvc/O=nginxsvc"
$KUBECTL create secret tls tls-secret --key tls.key --cert tls.crt

$KUBECTL create namespace $NS_ARGO
$KUBECTL apply -n $NS_ARGO -f $URL_ARGO
$KUBECTL patch svc argocd-server -n $NS_ARGO -p '{"spec": {"type": "LoadBalancer"}}'

URL_ARGO=$($KUBECTL get svc argocd-server -n $NS_ARGO | $GREP -v EXTER | $AWK '{print $4}')

while [ "$URL_ARGO" == "<pending>" ]; do 
	sleep 5;
	URL_ARGO=$($KUBECTL get svc argocd-server -n $NS_ARGO | $GREP -v EXTER | $AWK '{print $4}');  
done
PASS_ARGO=$($KUBECTL -n $NS_ARGO get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

echo -e "\nURL ArgoCd: http://${URL_ARGO}:80 \nUsuario ArgoCd: admin\nPass ArgoCd: ${PASS_ARGO}"
