lsof -P | grep ':9545' | awk '{print $2}' | xargs kill -9
lsof -P | grep ':5000' | awk '{print $2}' | xargs kill -9
lsof -P | grep ':8080' | awk '{print $2}' | xargs kill -9