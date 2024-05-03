# Sheets Updater service
Fault tolerant and Concurrent Consumer service. The Sheets Updater service dequeues the data from the message, then processes it to upload them to Google Sheets. This approach also consists of caching the data and attempting the Exponential Backoff to ensure response data is uploaded to Google Sheets, ensuring fault tolerant behaviour.

# Installation
1. Make sure RabbitMQ is running. If not, then:  
```docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.10-management```
2. Make sure redis server is active  
3. Build Docker container for Sheets Updater service  
```docker build -t "sheetsupdater" .```
4. Run the container  
```docker run -it --network=host "sheetsupdate"```
