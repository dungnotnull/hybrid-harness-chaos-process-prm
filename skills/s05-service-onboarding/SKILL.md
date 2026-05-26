---
name: harness-service-onboarding
description: >
  Onboard a new service, microservice, or application onto the Harness platform end-to-end.
  Use this skill whenever the user says "add a new service to Harness", "onboard my app",
  "register a new microservice", "set up Harness for X service", or needs to create
  service definitions, infrastructure definitions, environment configurations, monitored
  services, connector registrations, or delegate scoping for a new workload.
  Also trigger when a developer joins a team and needs to wire up their service for the first time.
---

# Harness Service Onboarding

## Purpose
Guide the complete end-to-end onboarding of a new service onto Harness: from creating the service entity to wiring up environments, infrastructure definitions, connectors, monitored services, and the first pipeline run.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Pipeline YAML / service name | s04 (workflow_context.artifacts) | Yes |
| Repository URL, container registry | s01 or user | Yes |
| Kubernetes cluster info | s06 output or user | Yes |
| Harness org/project identifiers | CLAUDE.md | Yes |
| Delegate selector | s06 output | No |
| Observability tool choice | s02 taste or s01 | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Service definition YAML | `.commandcode/artifacts/service-<name>.yaml` | YAML |
| Environment YAML per tier | `.commandcode/artifacts/env-<tier>.yaml` | YAML |
| Infrastructure definition YAML | `.commandcode/artifacts/infra-<name>-<tier>.yaml` | YAML |
| Connector configs | `.commandcode/artifacts/connectors.yaml` | YAML |
| Onboarding hand-off document | User + s06 feed | Markdown |
| Service context (for s06, s07, s08, s10, s15) | workflow_context.artifacts | YAML object |

---

## Prerequisites
Gather before proceeding:
- [ ] Service name, language/runtime, and repository URL
- [ ] Container registry location (ECR, GCR, DockerHub, ACR)
- [ ] Kubernetes cluster and namespace (or other target infra)
- [ ] Harness Organization and Project identifiers
- [ ] Cloud provider credentials (for connector setup)
- [ ] Observability tool (Prometheus, Datadog, etc.) if CV is needed

---

## Onboarding Checklist (run in order)

```
[ ] 1. Create Connector(s)
[ ] 2. Create Service Definition
[ ] 3. Create Environment(s)
[ ] 4. Create Infrastructure Definition(s)
[ ] 5. Scope Delegate to Namespace
[ ] 6. Create Monitored Service (if CV enabled)
[ ] 7. Create Pipeline (reference harness/01-pipeline-design)
[ ] 8. Create Input Set for each environment
[ ] 9. First dry-run validation
[ ] 10. Hand-off documentation
```

---

## Step 1 — Connectors

### Kubernetes Cluster Connector
```yaml
connector:
  name: <CLUSTER_NAME> K8s
  identifier: <cluster_name>_k8s
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  type: K8sCluster
  spec:
    credential:
      type: InheritFromDelegate
    delegateSelectors:
      - <DELEGATE_SELECTOR>
```

### Docker Registry Connector
```yaml
connector:
  name: <REGISTRY_NAME>
  identifier: <registry_identifier>
  type: DockerRegistry
  spec:
    dockerRegistryUrl: https://index.docker.io/v2/
    providerType: DockerHub
    auth:
      type: UsernamePassword
      spec:
        username: <+secrets.getValue("docker_username")>
        passwordRef: docker_password_secret
```

### GitHub Source Connector
```yaml
connector:
  name: GitHub <REPO_NAME>
  identifier: github_<repo_identifier>
  type: Github
  spec:
    url: https://github.com/<ORG>
    connectionType: Account
    authentication:
      type: Http
      spec:
        type: UsernameToken
        spec:
          username: <+secrets.getValue("github_username")>
          tokenRef: github_pat_secret
    apiAccess:
      type: Token
      spec:
        tokenRef: github_pat_secret
    delegateSelectors:
      - <DELEGATE_SELECTOR>
```

---

## Step 2 — Service Definition

```yaml
service:
  name: <SERVICE_NAME>
  identifier: <service_identifier>
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  description: "<Service description>"
  tags:
    team: <TEAM_NAME>
    domain: <DOMAIN>
    managed-by: hcprm
  serviceDefinition:
    type: Kubernetes
    spec:
      manifests:
        - manifest:
            identifier: k8s_manifests
            type: K8sManifest
            spec:
              store:
                type: Github
                spec:
                  connectorRef: github_<repo_identifier>
                  gitFetchType: Branch
                  branch: main
                  paths:
                    - k8s/
              valuesPaths:
                - k8s/values.yaml
              skipResourceVersioning: false
              enableDeclarativeRollback: true
      artifacts:
        primary:
          primaryArtifactRef: primary
          sources:
            - identifier: primary
              sourceType: DockerRegistry
              spec:
                connectorRef: <registry_identifier>
                imagePath: <IMAGE_PATH>
                tag: <+input>
      variables:
        - name: replicaCount
          type: String
          value: "2"
        - name: memoryLimit
          type: String
          value: "512Mi"
        - name: cpuLimit
          type: String
          value: "500m"
```

---

## Step 3 — Environments

```yaml
# Create one environment entity per tier
environment:
  name: <ENV_TIER>  # e.g., staging
  identifier: <env_tier>
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  type: PreProduction  # or Production
  tags:
    managed-by: hcprm
  variables:
    - name: replicaCount
      type: String
      value: "1"   # override per-env
  overrides:
    manifests:
      - manifest:
          identifier: env_values
          type: Values
          spec:
            store:
              type: Github
              spec:
                connectorRef: github_<repo_identifier>
                gitFetchType: Branch
                branch: main
                paths:
                  - k8s/values-<ENV_TIER>.yaml
```

---

## Step 4 — Infrastructure Definition

```yaml
infrastructureDefinition:
  name: <SERVICE_NAME>-<ENV_TIER>-infra
  identifier: <service_identifier>_<env_tier>_infra
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  environmentRef: <env_tier>
  deploymentType: Kubernetes
  type: KubernetesDirect
  spec:
    connectorRef: <cluster_name>_k8s
    namespace: <K8S_NAMESPACE>
    releaseName: release-<+INFRA_KEY>
  allowSimultaneousDeployments: false
```

---

## Step 5 — Delegate Scoping

Ensure the delegate has access to the target namespace:

```yaml
# If using Harness Delegate Helm chart, apply RBAC:
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: harness-delegate-role
  namespace: <K8S_NAMESPACE>
  labels:
    managed-by: hcprm
rules:
  - apiGroups: ["", "apps", "extensions", "batch"]
    resources: ["pods", "deployments", "services", "configmaps",
                "secrets", "replicasets", "jobs", "statefulsets"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: ["networking.k8s.io"]
    resources: ["ingresses"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: harness-delegate-binding
  namespace: <K8S_NAMESPACE>
subjects:
  - kind: ServiceAccount
    name: harness-delegate
    namespace: harness-delegate
roleRef:
  kind: Role
  name: harness-delegate-role
  apiGroup: rbac.authorization.k8s.io
```

Reference `harness/03-delegate-management` for full delegate setup.

---

## Step 6 — Input Sets

Input sets capture environment-specific values, avoiding pipeline duplication.

```yaml
inputSet:
  name: <ENV_TIER> Input Set
  identifier: <env_tier>_input_set
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  pipelineIdentifier: <service_identifier>_pipeline
  inputSetReferences: []
  pipeline:
    identifier: <service_identifier>_pipeline
    variables:
      - name: imageTag
        value: latest
      - name: targetEnv
        value: <ENV_TIER>
    stages:
      - stage:
          identifier: Deploy_<env_identifier>
          spec:
            environment:
              environmentRef: <env_tier>
              infrastructureDefinitions:
                - identifier: <service_identifier>_<env_tier>_infra
```

---

## Step 7 — Dry-Run Validation

Before first real deployment, run pipeline with `skipDryRun: false`:
1. Navigate to pipeline → Run → select input set
2. Enable **"Dry Run"** toggle (CD stage will generate manifests without applying)
3. Review generated manifest in execution logs
4. Confirm: correct image, namespace, resource limits, labels

---

## Onboarding Hand-off Template

Generate and share this document with the service team:

```markdown
## Harness Onboarding Summary — <SERVICE_NAME>

**Project**: <PROJECT_ID> | **Org**: <ORG_ID>

### Resources Created
| Resource | Identifier |
|---|---|
| Service | <service_identifier> |
| Environment (dev) | dev |
| Environment (staging) | staging |
| Infrastructure (dev) | <service_identifier>_dev_infra |
| Infrastructure (staging) | <service_identifier>_staging_infra |
| Pipeline | <service_identifier>_pipeline |

### How to Deploy
1. Push to `main` branch → webhook trigger fires automatically
2. Or: Harness UI → Pipelines → <SERVICE_NAME> → Run → select input set

### Contacts
- SRE Owner: <SRE_NAME>
- Harness Admin: <ADMIN_NAME>
- Runbook: <LINK>
```

---

## Success Criteria
- [ ] All connectors tested and showing "Success"
- [ ] Service definition saved and visible in Harness UI
- [ ] Infrastructure definition linked to correct cluster/namespace
- [ ] Dry-run executed without errors
- [ ] First real deployment to dev completed successfully
- [ ] Hand-off document delivered to service team
