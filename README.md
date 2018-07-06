# Project Swayze
If you want the ultimate, you've got to be willing to pay the ultimate price. It's not tragic to die doing what you love.

![alt text](pics/brodhi.jpg "Bodhi")

# Reference
[How to generate self-signed certificates](https://coreos.com/os/docs/latest/generate-self-signed-certificates.html)

    cfssl print-defaults config > ca-config.json
    cfssl print-defaults csr > ca-csr.json
    cfssl gencert -initca ca-csr.json | cfssljson -bare ca -
    cfssl print-defaults csr > server.json
    cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server server.json | cfssljson -bare server

# Generate certificate authority key
    openssl genrsa -out ca.key 4096

# Generate certificate authority certificate
    openssl req -new -sha256 -key ca.key -out ca.pem -subj "/C=US/ST=Pennsylvania/L=Philadelphia/O=dafinga.net/OU=ProjectSwayze/CN=localhost"