## CD Automatizado via ArgoCD em Cluster OKE

## ##

### Requisitos:

- Conta da Oracle Cloud Infrastructure (teste gratuito https://www.oracle.com/cloud/free/)

### O que vamos fazer?

- Clonar repositório GitHub
- Configurar OKE
- Implementar aplicação via ArgoCD

### Passo a Passo

### Atividades pós-criação do cluster

1. Após a criação do cluster OKE, acesse:
	Menu > Developer Services > Kubernetes Clusters (OKE)
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/af8781b0-f2fa-4575-97ff-a6705f171d20)

3. Acesse o cluster criado (o nome do cluster pode variar)

	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/56f2949d-43c4-4999-a91e-6732affc4d22)

4. Clique na parte superior para abrir o **"Cloud Shell"**

	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/c281f159-c86e-4051-b12f-618c447739ab)

	Um console será aberto na parte inferior da tela. Uma vez carregado, se for a primeira vez que está sendo aberto, mostrará uma mensagem perguntando se você deseja saber mais sobre o *Cloud Shell*. Caso não deseje, digite a letra N e pressione Enter.

5. Como o Cluster de Kubernetes está configurado em uma **"sub-rede privada"**, devemos criar um acesso privado.

	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/2fa17022-c6b8-416f-b8df-3fc7679b91cc)

	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/d2ca2f22-0edd-4b32-a77c-6b3caa277757)

	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/91486d4a-1909-4e30-8acf-057630ea4620)

	Posteriormente, nosso console Cloud Shell se conectará por meio de uma interface privada na rede do cluster Kubernetes.

	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/dc2253d4-00c1-41db-9cf0-017f215a3c94)

7. Agora clique em **"Access Cluster"**

   	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/a1f39e2c-39fc-4cd0-98b4-5581f3978117)

8. Agora serão mostrados os comandos que devem ser copiados e colados para executar no console do *Cloud Shell*

	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/383a892e-228a-4f0f-bbb2-315b740b5bf8)

	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/05ae701e-d6cd-422c-9f9a-f21abc8aa2ba)

9. Clone o repositório git do console usando o comando
	```
	git clone https://github.com/whiplash0104/Race2CloudFY24.git
	```
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/1aac26c5-52e1-4020-b0ce-eb34368a450d)
	
	Este comando baixará o conteúdo necessário para configurar o cluster.

12. Uma vez baixado, entre no diretório ***Race2CloudFY24*** e execute o script ***configuracionesOKE.sh*** usando os comandos
	```
	cd Race2CloudFY24
	bash configuracionesOKE.sh
	```
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/d83e682c-d92e-4151-9700-9a89d89aed1a)

	A execução deste comando levará aproximadamente um minuto e, ao finalizar, fornecerá os dados de acesso ao ArgoCD.
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/8788492d-f3a7-4a2d-9567-b8db7fb51f4b)

13. Acesse a URL fornecida pelo comando anterior usando as credenciais também fornecidas (para cada caso as credenciais e IP são diferentes)
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/5fc8f180-3521-4feb-be63-9aad5adf1513)

14. Uma vez dentro da plataforma, precisamos criar 3 aplicações diferentes da seguinte maneira:
	Clique no botão ***+ NEW APP***
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/06adb6f9-1d48-4def-bc47-2e320af0d7e1)

 	Na seção ***NEW APPLICATION***, para criar o primeiro, defina os seguintes parâmetros na seção ***GENERAL***:
 	```
	Application Name:			api-reader
  	Project Name: 				Selecione o projeto default
  	SYNC POLICY:				Selecione a opção Automatic
	Clique e selecione a opção AUTO-CREATE NAMESPACE
  	```
  	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/84f7596b-e74e-4c8a-9059-f5a4dd573438)

	Na seção SOURCE, defina:
	```
	Repository URL:				https://github.com/whiplash0104/Race2CloudFY24.git
 	Revision:				main
 	Path:					api-reader/api-reader-manifest
 	```
 	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/29d6535c-4941-43ac-8323-4bbf784c2799)

	Na seção ***DESTINATION***:
	```
	Cluster URL:				Selecione a opção https://kubernetes.default.svc
 	Namespace:				api-reader
 	```
 	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/cf41c3f9-24c4-431a-ac57-0697c73bfafb)

	Finalmente, clique no botão ***CREATE***
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/3d466c5a-9e11-4100-b67a-9f194cc337fd)

	Após isso, o ArgoCD começará a implantar o aplicativo no cluster.

	A aplicação aparecerá na cor azul clara enquanto estiver sendo implantada
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/5bf4aa77-677c-434b-9a4c-47802205042d)

	Se o processo de implantação terminar corretamente, mudará para a cor verde
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/36c2fe79-7f47-40bb-9bba-9da04c8c2c5f)

15. Repita o mesmo processo para a próxima aplicação:
	Clique em ***NEW APPLICATION*** e defina os seguintes parâmetros:
 	```
	Application Name:			oci-transcribe
  	Project Name: 				Selecione o projeto default
  	SYNC POLICY:				Selecione a opção Automatic
	Clique e selecione a opção AUTO-CREATE NAMESPACE
  	Repository URL:				https://github.com/whiplash0104/Race2CloudFY24.git
 	Revision:				main
 	Path:					oci-transcribe/oci-transcribe-manifest-pt
  	Cluster URL:				Selecione a opção https://kubernetes.default.svc
 	Namespace:				oci-transcribe
  	```
  	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/722a700b-5ccf-4587-ab75-ef0f50599335)
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/b904c0bb-6e34-4312-acb5-5e51e9fdc1de)

	Podemos ver que a nova aplicação já está implantada
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/7bb44188-3313-4133-ad18-e9f38dd056c0)

	Ao clicar nessas aplicações, podemos ver os detalhes do que foi implantado
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/3bc6200e-c1d0-42ad-87da-f8ab24e57c80)

17. Repita o mesmo processo para a última aplicação:
	Clique em ***NEW APPLICATION*** e defina os seguintes parâmetros:
 	```
	Application Name:			oci-reader
  	Project Name: 				Selecione o projeto default
  	SYNC POLICY:				Selecione a opção Automatic
	Clique e selecione a opção AUTO-CREATE NAMESPACE
  	Repository URL:				https://github.com/whiplash0104/Race2CloudFY24.git
 	Revision:				main
 	Path:					oci-reader/oci-reader-manifest
  	Cluster URL:				Selecione a opção https://kubernetes.default.svc
 	Namespace:				oci-reader
  	```
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/09740c03-d10a-4b16-9b03-36b0b1631c37)
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/e92bb58f-c2be-44a3-a825-f924fcfe7a9b)

	Podemos ver que na nova aplicação temos uma porcentagem em verde e outra em azul claro
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/40583067/da7beb6a-9751-43ba-9464-207aadcf6235)

	Uma vez finalizado, deveríamos ter as três aplicações rodando corretamente
	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/4faa5440-eea7-4a2a-811a-0b87d3af0ece)

19. Para se conectar ao aplicativo implantado no ***Cloud Shell***, execute:
	```
	kubectl get service -n ingress-nginx | grep LoadBalancer | awk '{print $4}'
 	```
 	![image](https://github.com/whiplash0104/Race2CloudFY24/assets/14284928/98e7e60c-e995-433d-bc0a-b7ff34e9dcce)

20. Acesse o IP público fornecido através do seu navegador web.

