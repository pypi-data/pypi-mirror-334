#!/bin/bash
# Run this to generate a new self-signed cert for localhost for the purposes of
# integration testing

# One-liner for subjectAltName from:
# http://www.scispike.com/blog/openssl-subjectaltname-one-liner/
key_path="${HTTPS_PYTEST_FIXTURES_KEY:-tests/key.pem}"
cert_path="${HTTPS_PYTEST_FIXTURES_CERT:-tests/cert.pem}"
openssl req -newkey rsa:2048 -nodes -keyout "${key_path}" -x509 -days 10000 -out "${cert_path}" \
    -subj '/CN=127.0.0.1' \
    -extensions SAN \
    -config <( cat /etc/ssl/openssl.cnf \
    <(printf "[SAN]
subjectAltName='IP.1:127.0.0.1,DNS.1:localhost'

[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name

[req_distinguished_name]"))
