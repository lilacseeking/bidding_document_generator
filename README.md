# 先享后付（BNPL）产品技术方案架构文档（含设计图）

## II.A 架构哲学：领域驱动设计与微服务

### 系统微服务架构图
```mermaid
graph TD
  subgraph UserLayer[用户与渠道层]
    A1[Web/H5/App] --> G[API Gateway]
  end

  subgraph ServiceLayer[应用服务层（Spring Boot 微服务）]
    G --> B1[CreditDecisionService]
    G --> B2[AuthorizationService]
    G --> B3[FraudEngineService]
    G --> B4[LedgerCoreService]
    G --> B5[KYCService]
    G --> B6[ReconciliationService]
  end

  subgraph Infra[基础设施层]
    D1[(MySQL/PostgreSQL)]
    D2[(Redis Cluster)]
    D3[(Kafka)]
    D4[(CockroachDB)]
  end

  B1 --> D1
  B2 --> D3
  B3 --> D2
  B4 --> D4
  B6 --> D1

  subgraph Cloud[Kubernetes 环境]
    ServiceLayer
  end
```

---

## III. 领域驱动架构分解

### 领域上下文划分图（DDD Bounded Context）
```mermaid
graph LR
  Credit[CreditDecision 域]
授信与额度管理 --> Auth[Authorization 域]
交易授权
  Auth --> Risk[FraudRisk 域]
实时风险控制
  Auth --> Ledger[LedgerCore 域]
账务与分录管理
  Credit --> Ledger
  Identity[KYC/IdentityManagement 域]
身份与合规支持 --> Credit
  Servicing[Servicing 域]
还款与催收 --> Ledger
```

---

## V.A 终端用户端到端流程（从商户结账到清算）

### 用户结账到清算流程时序图
```mermaid
sequenceDiagram
  participant User as 用户
  participant Merchant as 商户系统
  participant Auth as AuthorizationService
  participant Credit as CreditDecisionService
  participant FES as FraudEngineService
  participant Ledger as LedgerCoreService
  participant PG as 支付网关

  User->>Merchant: 选择BNPL支付
  Merchant->>Auth: 创建授权请求
  Auth->>Credit: 请求授信额度
  Auth->>FES: 实时风控评分
  FES-->>Auth: 返回风险结果
  Credit-->>Auth: 返回授信额度
  Auth->>PG: 调用支付网关进行授权/捕获
  PG-->>Auth: 返回交易结果
  Auth->>Ledger: 创建贷款义务与分期账单
  Ledger-->>Auth: 确认入账
  Auth-->>Merchant: 返回交易成功
  Ledger-->>User: 生成账单通知
```

---

## VI.B 业务时序图：预授权风险评分与决策

```mermaid
sequenceDiagram
  participant Merchant as 商户网关
  participant Auth as AuthorizationService
  participant FES as FraudEngineService
  participant Credit as CreditDecisionService

  Merchant->>Auth: Authorize(OrderID, Amount, UserID)
  Auth->>Credit: 获取额度与信用评分
  Auth->>FES: 发送特征集并请求风险评分
  FES-->>Auth: 返回RiskScore + Decision
  Auth-->>Merchant: 授权批准或拒绝
```

---

## VI.C 聚合流程图：支付授权与账务更新

```mermaid
graph TD
  Start([开始：商户结账]) --> KYC{是否完成KYC?}
  KYC -- 否 --> KYCFlow[触发线上身份验证流程]
  KYC -- 是 --> CreditEval[混合信用评分评估]
  CreditEval --> RiskEval[实时风险评分]
  RiskEval --> Decision{通过?}
  Decision -- 否 --> Reject[拒绝交易并记录审计轨迹]
  Decision -- 是 --> Gateway[调用支付网关授权/捕获]
  Gateway --> LimitUpdate[更新授信额度]
  LimitUpdate --> Event[发布 TransactionSuccessEvent 至 Kafka]
  Event --> Ledger[LedgerCoreService 创建贷款义务]
  Ledger --> End([结束：商户确认收款])
```

---

## VII.A 信用卡核心系统集成策略

### 防腐层（ACL）架构图
```mermaid
graph TD
  Legacy[信用卡核心系统] --> ACL[Anti-Corruption Layer (SpringBoot)]
  ACL --> BNPL[BNPL微服务集群]
  BNPL --> Ledger[LedgerCoreService]
  BNPL --> Credit[CreditDecisionService]
  BNPL --> Auth[AuthorizationService]
```

---

## VII.B 支付网关集成策略

### 支付适配器模式图
```mermaid
graph LR
  Auth[AuthorizationService] --> Adapter[PaymentAdapter]
  Adapter --> PG[支付网关 API]
  PG --> Reconcile[ReconciliationService]
  Reconcile --> Ledger[LedgerCoreService]
```

---

## VII.C 清算与对账流程概览
```mermaid
sequenceDiagram
  participant PG as 支付网关
  participant Reconcile as ReconciliationService
  participant Ledger as LedgerCoreService

  PG->>Reconcile: 日终清算报告
  Reconcile->>Ledger: 核对账务分录
  Ledger-->>Reconcile: 返回差异报告
  Reconcile-->>PG: 调整与结算确认
```
