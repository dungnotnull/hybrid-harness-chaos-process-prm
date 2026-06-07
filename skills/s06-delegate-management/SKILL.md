---
name: harness-delegate-management
description: >
  Install, configure, upgrade, troubleshoot, and manage Harness Delegates.
  Use this skill whenever the user mentions delegates, Harness agents, delegate selectors,
  delegate connectivity issues, installing a delegate on Kubernetes or Docker, delegate
  auto-upgrade, delegate profiles, delegate tags, delegate scoping, or when a pipeline
  fails with "No eligible delegates found". Also trigger when setting up a new cluster
  for Harness, configuring delegate RBAC, or managing delegate resource limits.
---

# Harness Delegate Management

## Purpose
Install, configure, and maintain Harness Delegates — the on-premise agents that execute pipeline tasks, communicate with your infrastructure, and bridge Harness SaaS to your environments.

---

## Prerequisites
- [ ] Service definitions from s05 (Service Onboarding)
- [ ] Kubernetes cluster access and kubeconfig configured
- [ ] Harness account with delegate management permissions
- [ ] Network connectivity between delegate and Harness platform

## Input Contract

| Input | Source | Required |
|---|---|---|
| Service definitions / target clusters | s05 (workflow_context.artifacts) | Yes |
| Kubernetes cluster endpoints and namespaces | s05 output or user | Yes |
| Harness account ID, delegate token | User or Harness UI | Yes |
| Resource sizing preferences | s02 taste or user | No |
| RBAC scope requirements | s05 (service namespaces) | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Delegate Helm values | `.commandcode/artifacts/delegate-values.yaml` | YAML |
| Delegate RBAC YAML | `.commandcode/artifacts/delegate-rbac.yaml` | YAML |
| Delegate install commands | User (for execution) | Shell script |
| Delegate selector tags | s05, s10 (pipeline steps) | String list |
| Troubleshooting guide | s21 (alerting context) | Markdown |

---

## Delegate Architecture

```
Harness Manager (SaaS / Self-Managed)
        │  WebSocket (outbound only, port 443)
        ▼
  Harness Delegate  ─────────────────────────────────────┐
  (runs in your infra)                                    │
        │                                                 │
        ├── kubectl → Kubernetes clusters                 │
        ├── Helm → Chart deployments                      │
        ├── Terraform → IaC execution                     │
        ├── AWS/GCP/Azure CLI → Cloud operations          │
        └── Custom scripts → Shell / PowerShell           │
                                                          │
  Key: Delegate initiates ALL connections (no inbound)   ┘
```

**Important**: Delegates connect OUT to Harness. Your firewall never needs inbound rules for Harness.

---

## Delegate Types

| Type | Best For | Notes |
|---|---|---|
| Kubernetes (Helm) | Production workloads | Auto-upgrade, HA, preferred |
| Kubernetes (YAML) | Custom RBAC control | Manual upgrade |
| Docker | Local dev / testing | Not HA |
| Shell | Legacy VMs | Last resort |

---

## Workflow

### Install Kubernetes Delegate (Helm — Recommended)

#### Step 1 — Generate Token in Harness UI
`Account Settings → Account Resources → Delegates → New Delegate → Kubernetes → Helm Chart`

Copy the generated `delegateToken` value.

#### Step 2 — Add Harness Helm Repo
```bash
helm repo add harness https://app.harness.io/storage/harness-download/harness-helm-charts/
helm repo update
```

#### Step 3 — Create Namespace and Secret
```bash
kubectl create namespace harness-delegate
kubectl create secret generic harness-delegate-token \
  --from-literal=DELEGATE_TOKEN=<DELEGATE_TOKEN> \
  -n harness-delegate
```

#### Step 4 — Install via Helm
```bash
helm upgrade --install harness-delegate harness/harness-delegate \
  -n harness-delegate \
  --set delegateName=<DELEGATE_NAME> \
  --set accountId=<ACCOUNT_ID> \
  --set delegateToken=<DELEGATE_TOKEN> \
  --set managerEndpoint=https://app.harness.io \
  --set delegateDockerImage=harness/delegate:latest \
  --set replicas=2 \
  --set upgrader.enabled=true \
  --set resources.limits.cpu=2 \
  --set resources.limits.memory=4Gi \
  --set resources.requests.cpu=500m \
  --set resources.requests.memory=2Gi
```

#### Step 5 — Verify Registration
```bash
kubectl get pods -n harness-delegate
# Expected: harness-delegate-xxxxx   Running

# Check delegate logs
kubectl logs -n harness-delegate -l app=harness-delegate --tail=50
# Look for: "Delegate registration successful"
```

---

## Delegate Configuration Best Practices

### Resource Sizing

| Workload | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---|---|---|---|---|
| Light (few pipelines) | 250m | 1 | 512Mi | 2Gi |
| Medium (default) | 500m | 2 | 2Gi | 4Gi |
| Heavy (parallel builds) | 1 | 4 | 4Gi | 8Gi |
| CI-intensive | 2 | 8 | 8Gi | 16Gi |

### High Availability
Always run `replicas: 2` minimum in staging/production. Harness load-balances tasks across available replicas.

```yaml
# In Helm values or patch:
replicas: 2
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app
                operator: In
                values: [harness-delegate]
          topologyKey: kubernetes.io/hostname
```

### Delegate Selectors (Tags)
Apply tags to route specific tasks to specific delegates:

```yaml
# In delegate Helm values:
delegateTags: "prod-cluster,aws-us-east-1,team-payments"
```

```yaml
# In pipeline step — target specific delegate:
step:
  type: ShellScript
  spec:
    delegateSelectors:
      - prod-cluster
      - aws-us-east-1
```

---

## RBAC Configuration

### Minimal RBAC for Kubernetes Deployments
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: harness-delegate
  namespace: harness-delegate
  labels:
    managed-by: hcprm
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: harness-delegate-cluster-role
  labels:
    managed-by: hcprm
rules:
  - apiGroups: [""]
    resources: ["namespaces", "nodes"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps", "endpoints",
                "persistentvolumeclaims", "events", "secrets"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets", "statefulsets", "daemonsets"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: ["batch"]
    resources: ["jobs", "cronjobs"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: ["networking.k8s.io"]
    resources: ["ingresses"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: ["rbac.authorization.k8s.io"]
    resources: ["roles", "rolebindings"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: harness-delegate-binding
  labels:
    managed-by: hcprm
subjects:
  - kind: ServiceAccount
    name: harness-delegate
    namespace: harness-delegate
roleRef:
  kind: ClusterRole
  name: harness-delegate-cluster-role
  apiGroup: rbac.authorization.k8s.io
```

---

## Troubleshooting Guide

### "No eligible delegates found"

**Diagnosis checklist:**
```bash
# 1. Check delegate pods are running
kubectl get pods -n harness-delegate

# 2. Check delegate registered in Harness UI
# Account Settings → Delegates → verify status = "Connected"

# 3. Check delegate selector mismatch
# Compare pipeline delegateSelectors vs delegate tags

# 4. Check delegate connectivity
kubectl logs -n harness-delegate <DELEGATE_POD> | grep -i "error\|failed\|disconnect"

# 5. Verify outbound connectivity from delegate
kubectl exec -n harness-delegate <DELEGATE_POD> -- \
  curl -sv https://app.harness.io/api/health
```

### Delegate Disconnected / CrashLooping

```bash
# Check events
kubectl describe pod -n harness-delegate <DELEGATE_POD>

# Common causes:
# 1. OOMKilled → increase memory limit
# 2. Token expired → regenerate token in UI, update secret
# 3. DNS resolution failure → check cluster DNS

# Fix OOMKilled:
kubectl patch deployment harness-delegate -n harness-delegate \
  --type='json' \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/resources/limits/memory","value":"6Gi"}]'
```

### Delegate Token Rotation
```bash
# 1. Generate new token in Harness UI (don't revoke old yet)
# 2. Update secret
kubectl create secret generic harness-delegate-token \
  --from-literal=DELEGATE_TOKEN=<NEW_TOKEN> \
  -n harness-delegate \
  --dry-run=client -o yaml | kubectl apply -f -

# 3. Restart delegates
kubectl rollout restart deployment/harness-delegate -n harness-delegate

# 4. Verify reconnected, then revoke old token in UI
```

---

## Auto-Upgrade

Harness delegate auto-upgrade is strongly recommended:
```yaml
# In Helm values:
upgrader:
  enabled: true
  # Upgrader checks for new delegate image versions every hour
  # and applies updates with zero-downtime rolling strategy
```

To check current delegate version:
```bash
kubectl get deployment harness-delegate -n harness-delegate \
  -o jsonpath='{.spec.template.spec.containers[0].image}'
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | AI suggests delegate configuration and RBAC templates |
| Target | L2 | AI drafts delegate install scripts and RBAC policies |

### Harness AI Agent

**Agent**: Harness AI DevOps Agent
**Capabilities**:
- Delegate install guidance
- RBAC policy template generation
- Namespace scoping recommendations

### Human Gates

- Delegate installation execution
- RBAC changes
- Namespace access grants

### Fallback

When Harness AI is unavailable: Use static pipeline templates from s09 Template Library and manual YAML construction following Harness schema documentation.

---

## Success Criteria
- [ ] Delegate pods: `Running`, replicas ≥ 2
- [ ] Harness UI shows delegate as "Connected"
- [ ] Delegate selectors correctly configured and matching pipeline usage
- [ ] RBAC verified: delegate can list/get/create pods in target namespaces
- [ ] Auto-upgrade enabled
- [ ] Token stored as Kubernetes secret (not in pipeline YAML)
- [ ] Resource limits set appropriately for workload
