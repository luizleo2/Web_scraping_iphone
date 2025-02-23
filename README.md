# Web Scraping de Preços do iPhone

Este projeto realiza Web Scraping para monitorar o preço de um iPhone na Amazon, armazenando os dados em um banco de dados SQLite.

## 🚀 Tecnologias Utilizadas
- Python
- Requests
- BeautifulSoup
- Pandas
- SQLite
- Telegram Bot (opcional)

## 📌 Funcionalidades
- Coleta o nome e preço do produto na Amazon
- Armazena os dados em um banco de dados SQLite
- Verifica e mantém o maior preço registrado
- (Futuramente) Envia notificações via Telegram quando um novo preço máximo for detectado

## 🔧 Como Usar
1. Clone este repositório:
   ```bash
   git clone https://github.com/luizleo2/Web_scraping_iphone.git
   cd Web_scraping_iphone
   ```
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o script:
   ```bash
   python nome_do_arquivo.py
   ```

## 🛠 Configuração do Telegram Bot (Opcional)
Se desejar receber notificações no Telegram, defina as variáveis de ambiente:
```bash
export TELEGRAM_TOKEN="seu_token"
export TELEGRAM_CHAT_ID="seu_chat_id"
```

## ⚠️ Observações
- O tempo entre requisições é ajustado para evitar bloqueios.
- Certifique-se de seguir os Termos de Serviço da Amazon ao realizar Web Scraping.

---
✉️ **Contato:** Caso tenha dúvidas ou sugestões, sinta-se à vontade para abrir uma issue ou entrar em contato! 🚀

