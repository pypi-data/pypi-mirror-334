DOMAIN=chronulus-central-artifacts
PIP_REPO=pip
AWS_REGION=us-east-1
CA_AWS_ACCOUNT_ID=605134426679

TOKEN=$(aws codeartifact get-authorization-token --profile CentralArtifacts  --domain $DOMAIN --domain-owner $CA_AWS_ACCOUNT_ID --query authorizationToken --output text)

export UV_EXTRA_INDEX_URL="https://aws:${TOKEN}@${DOMAIN}-${CA_AWS_ACCOUNT_ID}.d.codeartifact.${AWS_REGION}.amazonaws.com/pypi/${PIP_REPO}/simple/"
echo $UV_EXTRA_INDEX_URL > chronulus_index_url.txt
