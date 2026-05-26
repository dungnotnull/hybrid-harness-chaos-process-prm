---
name: harness-secrets-management
description: >
  Create, reference, rotate, and audit secrets in Harness pipelines and configurations.
  Use this skill whenever the user asks about secrets, credentials, API keys, passwords,
  certificates, Vault integration, AWS Secrets Manager, KMS, GCP Secret Manager,
  Azure Key Vault, encrypted variables, or how to avoid hardcoding sensitive values in
  pipelines. Also trigger when a pipeline is leaking credentials in logs, or when the
  user needs to rotate a secret safely across multiple pipelines.
---

# Harness Secrets Management

## Purpose
Establish a zero-hardcoded-secret policy across all Harness resources. Every credential, API key, password, and certificate must flow through a secrets manager — never embedded in YAML, logs, or environment variables.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Service definitions requiring secrets | s05 (workflow_context.artifacts) | Yes |
| Secrets backend choice | s02 taste or user | Yes |
| Delegate connectivity info | s06 output | Yes |
| List of required secrets (DB, API keys, certs) | s01 PRD or user | Yes |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Secret Manager connector YAML | `.commandcode/artifacts/secrets-manager.yaml` | YAML |
| Secret reference definitions | `.commandcode/artifacts/secrets-references.yaml` | YAML |
| Pre-commit hook script | `.git/hooks/pre-commit` | Bash |
| Secret rotation runbook | s25 (postmortem context) | Markdown |
| Secret usage map | s22 (governance audit) | YAML |

---

## Prerequisites
- [ ] Harness Account / Project access with Secrets Manager permissions
- [ ] Choice of secrets backend: Harness Built-in / HashiCorp Vault / AWS SM / GCP SM / Azure KV
- [ ] Delegate deployed with access to the chosen secrets backend (network path confirmed)

---

## Secrets Architecture

```
External Secrets Backend           Harness Secret Manager Connector
(Vault / AWS SM / GCP SM)  ◄──────────────────────────────────────
         │                                       │
         │  Secret Value (never leaves infra)    │
         ▼                                       ▼
   Harness Secret Reference               Pipeline YAML
   secrets.getValue("my_key")     ←   <+secrets.getValue("my_key")>
         │
         ▼
   Delegate fetches at runtime → injects into step environment
   (masked in logs as ***)
```

**Golden Rule**: Harness never stores the actual secret value (when using external SM). It stores only the reference path. The delegate fetches the value at runtime, directly from your backend.

---

## Supported Secret Manager Backends

| Backend | Connector Type | Auth Methods |
|---|---|---|
| Harness Built-in | Native | Account-level encryption |
| HashiCorp Vault | HashiCorpVault | Token, AppRole, K8s Auth, AWS IAM |
| AWS Secrets Manager | AwsSecretManager | IAM Role (delegate), Access Key |
| AWS KMS | AwsKms | IAM Role (delegate), Access Key |
| GCP Secret Manager | GcpSecretManager | Service Account, Workload Identity |
| Azure Key Vault | AzureKeyVault | Service Principal, Managed Identity |
| CyberArk | CyberArk | Application + Safe |

---

## Step 1 — Configure Secret Manager Connector

### HashiCorp Vault (AppRole)
```yaml
connector:
  name: HashiCorp Vault Prod
  identifier: vault_prod
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  type: VaultConnector
  spec:
    authTokenRef: vault_auth_token_secret    # Bootstrap token only
    basePath: secret/data/harness            # Vault path prefix
    vaultUrl: https://vault.internal.company.com
    renewalIntervalMinutes: 10
    secretEngineManuallyConfigured: true
    secretEngineName: secret
    secretEngineVersion: 2
    useVaultAgent: false
    useAwsIam: false
    useK8sAuth: false
    appRoleId: <APP_ROLE_ID>
    secretId: vault_approle_secret_id        # Reference to bootstrap secret
    delegateSelectors:
      - prod-cluster
```

### HashiCorp Vault (Kubernetes Auth — preferred for K8s delegates)
```yaml
connector:
  name: Vault K8s Auth
  identifier: vault_k8s_auth
  type: VaultConnector
  spec:
    vaultUrl: https://vault.internal.company.com
    basePath: secret/data/harness
    useK8sAuth: true
    k8sAuthEndpoint: kubernetes
    vaultK8sAuthRole: harness-delegate-role
    serviceAccountTokenPath: /var/run/secrets/kubernetes.io/serviceaccount/token
    secretEngineManuallyConfigured: true
    secretEngineName: secret
    secretEngineVersion: 2
    renewalIntervalMinutes: 10
    delegateSelectors:
      - prod-cluster
```

### AWS Secrets Manager (IAM Role on Delegate)
```yaml
connector:
  name: AWS Secrets Manager Prod
  identifier: aws_sm_prod
  type: AwsSecretManager
  spec:
    region: us-east-1
    credential:
      type: AssumeIAMRole   # No access keys needed; uses delegate's EC2/pod role
    delegateSelectors:
      - aws-prod-delegate
    default: false
```

---

## Step 2 — Create Secrets

### Text Secret (API Key, Password)
```yaml
secret:
  type: SecretText
  name: Stripe API Key
  identifier: stripe_api_key
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  spec:
    secretManagerIdentifier: vault_prod
    valueType: Reference           # For external SM: path to secret
    value: "payment/stripe/api_key"  # Vault path (relative to basePath)
```

### File Secret (TLS Cert, SSH Key, kubeconfig)
```yaml
secret:
  type: SecretFile
  name: TLS Certificate
  identifier: tls_cert_pem
  spec:
    secretManagerIdentifier: vault_prod
    # Upload file via Harness API or UI
```

### SSH Credential (Git, bastion access)
```yaml
secret:
  type: SSHKey
  name: GitHub Deploy Key
  identifier: github_deploy_key
  spec:
    auth:
      type: SSH
      spec:
        credentialType: KeyReference
        spec:
          userName: git
          key: github_ssh_private_key    # Reference to file secret
          encryptedPassphrase: ""
```

---

## Step 3 — Reference Secrets in Pipelines

### In Step Environment Variables
```yaml
step:
  type: Run
  spec:
    envVariables:
      STRIPE_API_KEY: <+secrets.getValue("stripe_api_key")>
      DB_PASSWORD: <+secrets.getValue("database_password")>
      JWT_SECRET: <+secrets.getValue("jwt_signing_secret")>
    command: |
      # $STRIPE_API_KEY is available here, masked as *** in logs
      ./deploy.sh
```

### In Connector References
```yaml
connector:
  spec:
    auth:
      spec:
        passwordRef: database_password    # Harness secret identifier
```

### In Kubernetes Secrets via Pipeline
```yaml
step:
  name: Sync K8s Secret
  type: ShellScript
  spec:
    shell: Bash
    source:
      type: Inline
      spec:
        script: |
          kubectl create secret generic app-secrets \
            --from-literal=STRIPE_KEY="<+secrets.getValue("stripe_api_key")>" \
            --from-literal=DB_PASS="<+secrets.getValue("database_password")>" \
            -n <+infra.namespace> \
            --dry-run=client -o yaml | kubectl apply -f -
```

---

## Step 4 — Secret Rotation Workflow

```
1. Create new secret version in backend (Vault / AWS SM)
2. Update Harness secret reference (if path changed)
3. Test in dev environment first:
   - Run pipeline with new secret
   - Verify application accepts new credential
4. Roll to staging → verify
5. Roll to production:
   - Deploy new secret
   - Verify connections healthy
   - Revoke old secret version
6. Update rotation date in audit log
```

### Zero-Downtime Rotation for Live Services
```yaml
# Use a "shadow" secret approach:
# 1. App reads BOTH old and new secrets (grace period)
# 2. Deploy app with dual-secret support
# 3. Confirm old secret no longer used
# 4. Remove old secret from application config
# 5. Remove old secret from backend
```

---

## Audit and Compliance

### Find All Secret Usage in Project (API)
```bash
curl -X GET \
  "https://app.harness.io/gateway/ng/api/v2/secrets?accountIdentifier=<ACCOUNT>&projectIdentifier=<PROJECT>&orgIdentifier=<ORG>&pageSize=100" \
  -H "x-api-key: <HARNESS_API_KEY>" \
  | jq '.data.content[] | {identifier, name, secretManagerIdentifier, updatedAt}'
```

### Detect Hardcoded Secrets in Pipeline YAML (pre-commit hook)
```bash
#!/bin/bash
# .git/hooks/pre-commit
# Block commits that contain hardcoded secrets in Harness YAML files

files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.yaml$|\.yml$')

for file in $files; do
  # Check for patterns that suggest hardcoded secrets
  if grep -qE '(password|token|secret|key|apiKey)\s*:\s*["\x27][A-Za-z0-9+/]{20,}' "$file"; then
    echo "ERROR: Potential hardcoded secret in $file"
    echo "Use: <+secrets.getValue(\"your_secret_id\")> instead"
    exit 1
  fi
done
```

---

## Secret Scope Hierarchy

```
Account-level secrets    → Available across all orgs and projects
    └── Org-level secrets     → Available across all projects in org
            └── Project-level secrets  → Available only in this project
```

**Rule of thumb:**
- Infrastructure credentials (cloud provider) → Account level
- Shared integration secrets (Slack, Jira) → Org level
- Application secrets (DB passwords, API keys) → Project level

---

## Success Criteria
- [ ] Zero hardcoded secrets in any pipeline YAML
- [ ] All secrets referencing external SM (not Harness built-in) for production
- [ ] Secret rotation runbook documented and tested
- [ ] Pre-commit hook blocking hardcoded secrets in repository
- [ ] Secret access audited — each secret has a designated owner
- [ ] Delegate has network access to secrets backend (tested with `nc` or `curl`)
- [ ] Logs confirmed: secret values appear as `***` not plaintext
