# Roteiro do Vídeo Pitch (até 4 minutos)

Tempo total alvo: **3min30s**. Fale devagar, grave a tela com o dashboard aberto e o terminal ao lado.
Publique no YouTube como **não listado** e teste o link em uma aba anônima antes de enviar.

## 0:00 – 0:30 | Abertura e propósito
**Tela:** você na câmera (ou slide com o título).
> "Olá, eu sou o Lucas, aluno de Análise e Desenvolvimento de Sistemas na UniFECAF. Neste projeto construí um pipeline de dados para IoT: ele pega leituras de temperatura de dispositivos, guarda em um banco PostgreSQL rodando no Docker e mostra tudo em um dashboard interativo. O objetivo é transformar dados brutos de sensores em informação que ajude a tomar decisão."

## 0:30 – 1:15 | Arquitetura e tecnologias
**Tela:** diagrama do README (CSV → Python → PostgreSQL → Views → Streamlit) ou a estrutura de pastas no VS Code.
> "Os dados vêm de um dataset do Kaggle, o Temperature Readings: IoT Devices. Usei Python com pandas para ler e limpar o CSV, SQLAlchemy para conectar ao banco, PostgreSQL dentro de um container Docker para armazenar, views SQL para organizar as consultas e Streamlit com Plotly para a visualização. O Docker garante que o banco sobe igual em qualquer máquina com um único comando."

## 1:15 – 2:00 | Como os dados foram processados
**Tela:** terminal rodando `docker compose up -d` e `python src/ingest.py`; mostrar a saída com o total de linhas.
> "Primeiro subo o container com docker compose. Depois rodo o script de ingestão: ele converte a data para o formato correto, padroniza os campos, remove linhas nulas e duplicadas e carrega tudo na tabela temperature_readings. Aqui dá para ver o total de registros inseridos. Ao final, o script cria as três views SQL."

## 2:00 – 2:40 | As 3 views
**Tela:** arquivo `sql/views.sql` ou `psql` com um SELECT em cada view.
> "A primeira view traz a temperatura média por dispositivo e por local, interno ou externo. A segunda conta quantas leituras chegam em cada hora do dia. A terceira mostra a temperatura máxima e mínima de cada dia. Cada uma alimenta um gráfico do dashboard."

## 2:40 – 3:30 | Demonstração e conclusões
**Tela:** navegador no dashboard (`streamlit run src/dashboard.py`); passe o mouse nos gráficos para mostrar a interatividade.
> "Aqui está o dashboard. No primeiro gráfico comparo a média de temperatura por dispositivo. No segundo vejo em quais horários há mais leituras. No terceiro acompanho as máximas e mínimas por dia. [CITE 2 OU 3 INSIGHTS REAIS DOS SEUS DADOS, por exemplo a diferença entre interno e externo e o dia de maior variação.] Na prática, esse pipeline poderia alimentar alertas de temperatura em salas de servidores, câmaras frias ou estufas."

## 3:30 – 3:45 | Encerramento
> "O código, o Docker e a documentação estão no meu GitHub, com o passo a passo no README. Obrigado!"

## Checklist antes de gravar
- [ ] Container rodando e dados carregados com o CSV real
- [ ] Dashboard abrindo sem erro
- [ ] Insights reais anotados (rode `sql/insights.sql`)
- [ ] Vídeo com no máximo 4 minutos
- [ ] Link do YouTube testado em aba anônima
