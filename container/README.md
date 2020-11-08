# Docker container

## Test a container of LIGTHBO.LT

1. git clone <https://github.com/BlockchainBrussels/LIGHTBO.LT.git> && cd LIGHTBO.LT/container
1. docker build -t lightbo.lt:latest .
1. docker run -p 3030:3000 -t lightbo.lt:latest
1. Eventually test it differently?  docker run -i -t lightbo.lt /bin/bash
