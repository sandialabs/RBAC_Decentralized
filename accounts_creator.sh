# Create the Ethereum network - based on the rbac_generation.py script
npx ganache-cli -i $1 --deterministic -a $2 -p $3 --db $4 -e 300 >> log.txt