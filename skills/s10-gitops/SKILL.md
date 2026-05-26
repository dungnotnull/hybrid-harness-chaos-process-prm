---
name: harness-gitops
description: >
  Implement and operate GitOps workflows using Harness GitOps (ArgoCD-backed) for
  Kubernetes deployments. Use this skill whenever the user mentions GitOps, ArgoCD,
  ApplicationSet, drift detection, sync policy, self-healing, Git as source of truth,
  multi-cluster GitOps, Harness GitOps agent, app-of-apps pattern, or managing
  Kubernetes state declaratively from a Git repository. Also trigger when the user
  wants to audit what is running in a cluster vs what is in Git.
---

# Harness GitOps

## Purpose
Establish Git as the single source of truth for Kubernetes cluster state. All changes flow through Git PRs — never direct `kubectl apply`. Harness GitOps continuously reconciles cluster state to match the Git repository.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Service definitions | s05 (workflow_context.artifacts) | Yes |
| Deploy templates | s09 output | No |
| Pipeline YAML | s04 output | Yes |
| Git repository details | s01 or user | Yes |
| GitOps preference (s02 taste) | s02 taste (deployment category) | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| GitOps Application YAML | `.commandcode/artifacts/app-<service>.yaml` | YAML |
| ApplicationSet YAML | `.commandcode/artifacts/applicationset.yaml` | YAML |
| GitOps Agent config | `.commandcode/artifacts/gitops-agent.yaml` | YAML |
| Drift alert notification rule | s21 (alerting context) | YAML |
| Pipeline GitOps sync step | s04 (pipeline updates) | YAML |

---

## Prerequisites
- [ ] Kubernetes cluster accessible by Harness delegate
- [ ] Git repository with Kubernetes manifests or Helm charts
- [ ] Harness GitOps Agent installed in cluster
- [ ] ArgoCD CRDs installed (done automatically by Harness GitOps agent)

---

## GitOps Architecture

```
Developer
    │  git push / PR merge → main branch
    ▼
Git Repository (GitHub / GitLab / Bitbucket)
    │  Harness GitOps watches for changes
    ▼
Harness GitOps (ArgoCD engine)
    │  Detects drift OR manual sync triggered
    ▼
Harness GitOps Agent (runs in cluster)
    │  Applies manifests via kubectl
    ▼
Kubernetes Cluster
    │  Reconciles to match Git state
    ▼
Drift Alert → Harness notification → Auto-heal OR manual review
```

---

## Step 1 — Install GitOps Agent

```bash
# Generate agent token in Harness UI:
# GitOps → Agents → New Agent → Kubernetes → Download YAML

# Apply to cluster
kubectl apply -f harness-gitops-agent.yaml

# Verify
kubectl get pods -n harness-gitops-agent
# Expected: gitops-agent-xxxx   Running

kubectl logs -n harness-gitops-agent <AGENT_POD> | grep -i "registered"
# Expected: "Agent registered successfully"
```

---

## Step 2 — Create GitOps Repository

```yaml
repository:
  name: <SERVICE_NAME> Manifests
  identifier: <service_identifier>_manifests
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  agentIdentifier: <GITOPS_AGENT_IDENTIFIER>
  repo: https://github.com/<ORG>/<REPO>
  connectionType: HTTPS
  authType: USERNAME_PASSWORD
  username: <+secrets.getValue("github_username")>
  password: <+secrets.getValue("github_pat")>
  insecure: false
  enableLfs: false
  inherit: false
```

---

## Step 3 — Create GitOps Cluster

```yaml
cluster:
  name: Production EKS Cluster
  identifier: prod_eks
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  agentIdentifier: <GITOPS_AGENT_IDENTIFIER>
  server: https://<EKS_API_SERVER>
  name: in-cluster        # Use "in-cluster" if agent is IN the target cluster
  namespaces:
    - <TARGET_NAMESPACE>
```

---

## Step 4 — Create Application

```yaml
application:
  name: <SERVICE_NAME>-production
  identifier: <service_identifier>_production
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  agentIdentifier: <GITOPS_AGENT_IDENTIFIER>
  clusterIdentifier: prod_eks
  repoIdentifier: <service_identifier>_manifests
  spec:
    source:
      repoURL: https://github.com/<ORG>/<REPO>
      targetRevision: main           # Branch / tag / commit
      path: k8s/production/          # Path within repo
      # For Helm:
      # chart: my-chart
      # helm:
      #   valueFiles: [values-production.yaml]
      #   parameters:
      #     - name: image.tag
      #       value: <+artifact.tag>
    destination:
      server: https://kubernetes.default.svc  # in-cluster
      namespace: <TARGET_NAMESPACE>
    syncPolicy:
      automated:
        prune: true                  # Remove resources deleted from Git
        selfHeal: true               # Auto-revert manual kubectl changes
        allowEmpty: false            # Never sync an empty repo
      syncOptions:
        - CreateNamespace=true
        - PrunePropagationPolicy=foreground
        - PruneLast=true             # Prune only after other resources sync
        - RespectIgnoreDifferences=true
      retry:
        limit: 5
        backoff:
          duration: 5s
          factor: 2
          maxDuration: 3m
    ignoreDifferences:
      # Ignore fields managed by controllers (not by GitOps)
      - group: apps
        kind: Deployment
        jsonPointers:
          - /spec/replicas          # HPA manages replicas
      - group: ""
        kind: Service
        jsonPointers:
          - /spec/clusterIP         # Assigned by K8s, not in Git
```

---

## Step 5 — ApplicationSet (Multi-Cluster / Multi-Env)

ApplicationSets generate multiple Applications from a single template:

```yaml
# app-of-apps pattern: one ApplicationSet manages all services
applicationSet:
  name: All Services
  identifier: all_services
  agentIdentifier: <GITOPS_AGENT_IDENTIFIER>
  spec:
    generators:
      # Generate one app per service directory
      - git:
          repoURL: https://github.com/<ORG>/gitops-config
          revision: main
          directories:
            - path: services/*/production
    template:
      metadata:
        name: "{{path.basenameNormalized}}-production"
        labels:
          managed-by: hcprm
          generated-by: applicationset
      spec:
        source:
          repoURL: https://github.com/<ORG>/gitops-config
          targetRevision: main
          path: "{{path}}"
        destination:
          server: https://kubernetes.default.svc
          namespace: "{{path.basename}}"
        syncPolicy:
          automated:
            prune: true
            selfHeal: true
```

---

## Step 6 — GitOps in CD Pipeline

Trigger GitOps sync as part of a Harness CD pipeline step:

```yaml
- step:
    name: Update Image Tag in Git
    identifier: update_image_tag_git
    type: ShellScript
    spec:
      shell: Bash
      source:
        type: Inline
        spec:
          script: |
            # Clone GitOps config repo
            git clone https://$GIT_USERNAME:$GIT_TOKEN@github.com/<ORG>/gitops-config.git
            cd gitops-config

            # Update image tag using yq
            yq e -i '.image.tag = "<+artifact.tag>"' \
              services/<+service.name>/production/values.yaml

            # Commit and push
            git config user.email "harness-bot@company.com"
            git config user.name "Harness Pipeline"
            git add .
            git commit -m "chore: update <+service.name> to <+artifact.tag> [skip ci]"
            git push origin main
      envVariables:
        GIT_USERNAME: <+secrets.getValue("github_username")>
        GIT_TOKEN: <+secrets.getValue("github_pat")>
      onDelegate: true

- step:
    name: Wait for GitOps Sync
    identifier: wait_gitops_sync
    type: GitOpsSync
    spec:
      prune: true
      dryRun: false
      applicationsList:
        - <service_identifier>_production
      retrySteps: 10
      retryInterval: 30s
```

---

## Drift Detection and Alerting

Configure alerts when cluster state diverges from Git:

```yaml
# Harness GitOps notification rule
notificationRule:
  name: Drift Alert
  identifier: drift_alert
  spec:
    conditions:
      - type: SyncStatusChange
        conditions:
          - operator: Equals
            value: OutOfSync
    destinations:
      - type: Slack
        spec:
          webhookUrl: <SLACK_WEBHOOK>
          channel: "#gitops-alerts"
          message: |
            ⚠️ GitOps Drift Detected!
            Application: {{app.name}}
            Status: {{app.status.sync.status}}
            Review: {{app.url}}
```

---

## Rollback via GitOps

GitOps rollback = revert the Git commit:

```bash
# Option 1: Git revert (preserves history — preferred)
git revert HEAD
git push origin main
# GitOps agent will sync back to previous state automatically

# Option 2: Pin to previous commit
git checkout <PREVIOUS_COMMIT> -- services/<SERVICE>/production/
git commit -m "revert: rollback <SERVICE> to <PREVIOUS_COMMIT>"
git push origin main
```

**Never do**: `kubectl rollout undo` — this creates drift and will be reverted by self-heal.

---

## Success Criteria
- [ ] GitOps agent running with `Connected` status in Harness
- [ ] Application syncing automatically within 3 minutes of Git push
- [ ] `selfHeal: true` — verified by making a manual `kubectl` change and observing auto-revert
- [ ] Drift detection alerts flowing to Slack / PagerDuty
- [ ] Image tag updates flowing through pipeline → Git → GitOps sync chain
- [ ] Multi-env ApplicationSet or separate apps per environment configured
- [ ] Rollback procedure tested and documented
