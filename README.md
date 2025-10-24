# Pingar_CTO
Uma das funções era verificar se os clientes estavam online quando os técnicos externos estavam dando manutenção na CTO, mas estava sendo uma dor pois nós do suporte técnico tinhamos que pegar cliente por cliente, abrir um cmd para cada um e etc.

Tendo em vista essa dor eu desenvolvi um programa em Python e utilizei a biblioteca PANDAS para ter pegar um arquivo EXCEL com os clientes e "pingar" todos automaticamente com poucos cliques. O programa foi um sucesso no nosso setor!

O programa importa um arquivo .xlsx informando o nome do cliente, ip e porta que está conectado na CTO

Após isso ele pega a string do tempo de resposta e exibe na tela, caso não tenha um retorno de "tempo = xxms" ele considera o cliente offline e muda de verde para amarelo/vermelho
<img width="614" height="200" alt="image" src="https://github.com/user-attachments/assets/bc504758-1528-46a3-9b59-f47af81cfc9e" />
