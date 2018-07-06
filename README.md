# Project Swayze
If you want the ultimate, you've got to be willing to pay the ultimate price. It's not tragic to die doing what you love.

![alt text](pics/brodhi.jpg "Bodhi")

# Reference (https://coreos.com/os/docs/latest/generate-self-signed-certificates.html)
    cfssl print-defaults config > ca-config.json
    cfssl print-defaults csr > ca-csr.json
    cfssl gencert -initca ca-csr.json | cfssljson -bare ca -

# Generate certificate authority key
    openssl genrsa -out ca.key 4096

# Generate certificate authority certificate
    openssl req -new -sha256 -key ca.key -out ca.pem -subj "/C=US/ST=Pennsylvania/L=Philadelphia/O=dafinga.net/OU=ProjectSwayze/CN=localhost"