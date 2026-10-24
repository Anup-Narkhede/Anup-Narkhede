<!--
  ATLAS OF DESIRED STATE · VOL. 01
  Every plate on this page is an animated SVG drawn in code — see tools/README.md.
  Light and dark variants are swapped with <picture>; PL. 06 is regenerated weekly by GitHub Actions.
-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/hero-dark.svg">
  <a href="https://github.com/Anup-Narkhede"><img src="assets/plates/hero-light.svg" width="100%" alt="Anup Narkhede, Cloud DevOps Engineer. An animated title plate: a noisy signal labelled toil, drift and 3 a.m. pages travels into a reconciliation loop of observe, diff and act, and leaves as a steady line. Tagline: Declare it once. Let the loop do the rest."></a>
</picture>

<br>

I’m **Anup Narkhede**, a Cloud DevOps Engineer. I build and automate cloud infrastructure with **AWS, Kubernetes, Terraform and Python**, and I’m currently pursuing an **M.Tech in Cloud Computing at BITS Pilani**.

My rule of thumb: anything done twice should be *declared once and reconciled forever*, which means pipelines instead of runbooks and controllers instead of reminders. The loop I’m exploring next is **AI agents that operate infrastructure through MCP**, with a human holding the approve key.

This page is an atlas of that idea. Each plate is a hand-composed, animated SVG, drawn entirely in code.

<sub><code>PL. 01</code>&nbsp;<a href="#the-delivery-line">The Delivery Line</a> &nbsp;·&nbsp; <code>PL. 02</code>&nbsp;<a href="#two-control-planes">Two Control Planes</a> &nbsp;·&nbsp; <code>PL. 03</code>&nbsp;<a href="#stratigraphy">Stratigraphy</a> &nbsp;·&nbsp; <code>PL. 04</code>&nbsp;<a href="#exhibits">Exhibits</a> &nbsp;·&nbsp; <code>PL. 05</code>&nbsp;<a href="#credentials">Credentials</a> &nbsp;·&nbsp; <code>PL. 06</code>&nbsp;<a href="#signal">Signal</a> &nbsp;·&nbsp; <code>PL. 07</code>&nbsp;<a href="#open-channel">Open Channel</a></sub>

<br>
<a id="the-delivery-line"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/delivery-dark.svg">
  <img src="assets/plates/delivery-light.svg" width="100%" alt="Plate 01, The Delivery Line. A transit map of a delivery pipeline. Line 1 runs through commit (git, GitHub), build (Jenkins), package (Docker), registry (Amazon ECR), sync (Argo CD, GitOps), run (Kubernetes, Amazon EKS) and observe (Prometheus, Grafana). Line 2, infrastructure as code with Terraform plan and apply, interchanges at run. A dashed feedback loop carries metrics, alerts and postmortems back to the next commit while an animated train rides the loop.">
</picture>

**PL. 01 — The Delivery Line.** Every change rides the same line: commit, Jenkins build, Docker image, Amazon ECR, Argo CD sync, Kubernetes, then observability. Terraform joins at *run*, and whatever production learns loops back into the next commit.

<br>
<a id="two-control-planes"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/planes-dark.svg">
  <img src="assets/plates/planes-light.svg" width="100%" alt="Plate 02, Two Control Planes. Figure A, for containers: a Kubernetes control plane with api-server, scheduler, controller and etcd watches three worker nodes. A pod crashes, ready replicas fall from six to five, and the controller schedules a replacement on another node until six of six are ready. Figure B, for intent: an intent card feeds an agent, which waits at a human approval switch, then calls kubectl, terraform, aws and gh through an MCP bus and verifies the result.">
</picture>

**PL. 02 — Two Control Planes.** Kubernetes taught me to think in reconciliation loops (*fig. A*). *Fig. B* is where I’m taking that idea: agents that plan against a goal, wait for a human to approve, then act through MCP tools and verify what happened.

<br>
<a id="stratigraphy"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/strata-dark.svg">
  <img src="assets/plates/strata-light.svg" width="100%" alt="Plate 03, Stratigraphy of a Stack. A geological cross-section with the oldest layer at the bottom: bedrock (Linux, Bash, networking, C), cloud (AWS, Azure), infrastructure as code (Terraform, CloudFormation, Boto3), containers (Docker, Kubernetes, kind, EKS), delivery (Git, Jenkins, Argo CD), observability (Prometheus, Grafana, CloudWatch), and the newest deposit on top, intelligence (Python, LLM agents, MCP). The layers are folded into an anticline and cut by a fault labelled ‘the stack held’; two boreholes carry rising particles upward.">
</picture>

**PL. 03 — Stratigraphy of a Stack.** These are the tools I use, not a pile of badges. Each layer was laid down on the one beneath it, roughly in the order my public repositories show I learned them: Linux bedrock in 2021, and the newest deposit, agents and MCP, still settling.

<br>
<a id="exhibits"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/section-exhibits-dark.svg">
  <img src="assets/plates/section-exhibits-light.svg" width="100%" alt="Plate 04 — Exhibits">
</picture>

Four public repositories, each drawn as the system it builds.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/exhibit-01-dark.svg">
  <a href="https://github.com/Anup-Narkhede/cloud-native-monitoring-app-code"><img src="assets/plates/exhibit-01-light.svg" width="100%" alt="Exhibit 01, Two-Repo GitOps: ship by commit and let the cluster pull. Animated schematic of an app repository built by Jenkins into an Amazon ECR image, and a manifest repository synced by Argo CD into a Kubernetes cluster."></a>
</picture>

> **Problem**&ensp;Clusters changed by hand drift away from what’s in git.<br>
> **Engineering**&ensp;Application code and Kubernetes manifests live in separate repositories. A Jenkins pipeline builds the Flask + psutil app into a Docker image and pushes it to Amazon ECR, whose repository is created with Boto3. Argo CD watches the manifest repo and syncs the cluster, and Terraform defines the EC2 instance.<br>
> **Why it’s interesting**&ensp;The cluster pulls its own desired state, so the deployment history *is* the git history.<br>
> [`cloud-native-monitoring-app-code`](https://github.com/Anup-Narkhede/cloud-native-monitoring-app-code) · [`manifest-repo`](https://github.com/Anup-Narkhede/manifest-repo)

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/exhibit-02-dark.svg">
  <a href="https://github.com/Anup-Narkhede/Pinger_App_K8S"><img src="assets/plates/exhibit-02-light.svg" width="100%" alt="Exhibit 02, Pinger: is it up, how fast, ask again forever. Animated radar with two sweeps, version one and version two, lighting up probed targets labelled with latencies and one timeout."></a>
</picture>

> **Problem**&ensp;Knowing whether a URL is up, and how fast it answers, all the time rather than only when someone checks.<br>
> **Engineering**&ensp;Three Node.js services: a frontend, a pinger that loops over URLs recording latency, response code and size, and a details service. Each is containerised and deployed to a local kind cluster with a control plane and three workers, and a build script loads the images straight into the cluster.<br>
> **Why it’s interesting**&ensp;Pinger v1 and v2 run side by side, the same shape as every canary rollout.<br>
> [`Pinger_App_K8S`](https://github.com/Anup-Narkhede/Pinger_App_K8S)

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/exhibit-03-dark.svg">
  <a href="https://github.com/Anup-Narkhede/terraform-project-an"><img src="assets/plates/exhibit-03-light.svg" width="100%" alt="Exhibit 03, Modular Terraform: infrastructure assembled from parts. Isometric module slabs; the lambda module is drawn solid as built, and api_gateway, ec2 and memorydb are dashed blueprints marked scaffold. An event travels to the Lambda and on to Slack, a plan line scans the modules, and an S3 state bucket shows a lock."></a>
</picture>

> **Problem**&ensp;One giant Terraform file can’t be reviewed or reused, and unlocked state invites collisions.<br>
> **Engineering**&ensp;Each service has its own module. The Lambda module is built: an IAM execution role, source packaged with `archive_file` and redeployed on hash change, and environment configuration. The Python handler routes user-removal events to a Slack notifier, which is still a stub. API Gateway, EC2 and MemoryDB modules are scaffolded next to it, drawn as blueprints above.<br>
> **Why it’s interesting**&ensp;State is encrypted in S3 with Terraform’s native `use_lockfile`, so there’s no DynamoDB lock table to babysit.<br>
> [`terraform-project-an`](https://github.com/Anup-Narkhede/terraform-project-an)

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/exhibit-04-dark.svg">
  <a href="https://github.com/Anup-Narkhede/Serverless-Web-Application"><img src="assets/plates/exhibit-04-light.svg" width="100%" alt="Exhibit 04, Serverless Web App: nothing to patch, one request path. Animated request travelling from a user through CloudFront and S3 for the static site, then Cognito, API Gateway and Lambda to DynamoDB for the API."></a>
</picture>

> **Problem**&ensp;A full web app with no servers to patch, scale or keep awake.<br>
> **Engineering**&ensp;Static hosting on S3 behind CloudFront, sign-in with Cognito, and an API Gateway → Lambda backend that writes to DynamoDB, observed with CloudWatch.<br>
> **Why it’s interesting**&ensp;Six managed services compose one request path, and the IAM boundaries between them are the real design work.<br>
> [`Serverless-Web-Application`](https://github.com/Anup-Narkhede/Serverless-Web-Application)

<sub>Also in the archive: [Boto3 automation scripts](https://github.com/Anup-Narkhede/Boto3-Python-SDK) for IAM, S3, EC2 and SQS · [AWS CLI shell projects](https://github.com/Anup-Narkhede/AWS-Projects) for ALB, Auto Scaling and EC2 · [Linux ops scripts](https://github.com/Anup-Narkhede/LinuxWorld) · [Docker + ECR + CloudFormation](https://github.com/Anup-Narkhede/Docker-Project-Mongo-Node-AWS-ECR-) · [Terraform labs](https://github.com/Anup-Narkhede/Terraform)</sub>

<br>
<a id="credentials"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/section-credentials-dark.svg">
  <img src="assets/plates/section-credentials-light.svg" width="100%" alt="Plate 05 — Credentials">
</picture>

<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/plates/seal-saa-dark.svg"><a href="https://www.credly.com/badges/a3973253-4e95-495b-ba1b-7624ca657d1f"><img src="assets/plates/seal-saa-light.svg" width="23%" alt="AWS Certified Solutions Architect – Associate (SAA), verified on Credly"></a></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/plates/seal-dva-dark.svg"><a href="https://www.credly.com/badges/f3fe5f9d-0427-4d52-8ffe-ceb9cf3baec3"><img src="assets/plates/seal-dva-light.svg" width="23%" alt="AWS Certified Developer – Associate (DVA), verified on Credly"></a></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/plates/seal-clf-dark.svg"><a href="https://www.credly.com/badges/7c20de9c-e554-49bb-b4cc-9921046c1198"><img src="assets/plates/seal-clf-light.svg" width="23%" alt="AWS Certified Cloud Practitioner (CLF), verified on Credly"></a></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/plates/seal-az900-dark.svg"><a href="https://www.credly.com/badges/f98694af-f545-40e4-950b-152a7faff3d4"><img src="assets/plates/seal-az900-light.svg" width="23%" alt="Microsoft Certified: Azure Fundamentals (AZ-900), verified on Credly"></a></picture>
</p>

<p align="center"><sub>Each seal links to its Credly verification.</sub></p>

<br>
<a id="signal"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/signal-dark.svg">
  <img src="assets/plates/signal-light.svg" width="100%" alt="Plate 06, Signal: GitHub contributions over the last twelve months drawn as a seismograph trace, with the yearly total, busiest week, longest streak and active weeks. Regenerated weekly by GitHub Actions.">
</picture>

**PL. 06 — Signal.** The last twelve months of contributions, drawn as a seismograph. A GitHub Action regenerates this plate every week from the GraphQL contributions calendar, with no third-party stats service involved.

<br>
<a id="open-channel"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plates/finale-dark.svg">
  <a href="https://www.linkedin.com/in/anup-narkhede-3291211ab/"><img src="assets/plates/finale-light.svg" width="100%" alt="Plate 07, Open Channel. The reconciliation loop from the title returns fully converged as a calm signal comes to rest inside it. Text: Let’s build something that runs itself. Open to conversations about cloud platforms, DevOps, SRE and AI-driven automation."></a>
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/anup-narkhede-3291211ab/"><b>LinkedIn</b></a> &nbsp;·&nbsp;
  <a href="https://anup-narkhede.github.io/Portfolio/"><b>Portfolio</b></a> &nbsp;·&nbsp;
  <a href="https://github.com/Anup-Narkhede?tab=repositories"><b>All repositories</b></a>
</p>

<p align="center"><sub><i>Colophon</i> — set in Archivo Expanded, Instrument Serif and JetBrains Mono (SIL OFL), embedded as per-plate subsets. Plates are generated by <a href="tools/README.md"><code>tools/build.py</code></a>. No templates were harmed.</sub></p>
